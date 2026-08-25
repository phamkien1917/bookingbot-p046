#!/usr/bin/env python3
"""Run machine-readable chatbot acceptance scenarios against the public API.

Uses only the Python standard library so it can run without project imports.
Booking/cancellation scenarios are skipped unless --allow-side-effects is set.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import uuid
from http.cookiejar import CookieJar
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SUITE = ROOT / "eval" / "chat_agent_acceptance.json"


def normalize(value: Any) -> str:
    text = unicodedata.normalize("NFD", str(value).lower())
    return "".join(char for char in text if unicodedata.category(char) != "Mn").replace("đ", "d")


def nested_get(payload: Any, path: str) -> Any:
    current = payload
    for part in path.split("."):
        if not isinstance(current, dict):
            return None
        current = current.get(part)
    return current


class ApiClient:
    def __init__(self, base_url: str, timeout: float) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(CookieJar()))

    def request(self, method: str, path: str, body: Any = None, headers: dict[str, str] | None = None) -> tuple[int, Any, float]:
        data = None
        request_headers = dict(headers or {})
        if body is not None:
            if isinstance(body, bytes):
                data = body
            else:
                data = json.dumps(body, ensure_ascii=False).encode("utf-8")
                request_headers["Content-Type"] = "application/json"
        request = urllib.request.Request(
            f"{self.base_url}{path}",
            data=data,
            headers=request_headers,
            method=method,
        )
        started = time.perf_counter()
        try:
            with self.opener.open(request, timeout=self.timeout) as response:
                raw = response.read().decode("utf-8")
                payload = json.loads(raw) if raw else {}
                return response.status, payload, (time.perf_counter() - started) * 1000
        except urllib.error.HTTPError as exc:
            raw = exc.read().decode("utf-8", errors="replace")
            try:
                payload = json.loads(raw)
            except json.JSONDecodeError:
                payload = {"detail": raw}
            return exc.code, payload, (time.perf_counter() - started) * 1000

    def login(self, email: str, password: str) -> None:
        encoded = urllib.parse.urlencode({"username": email, "password": password}).encode("utf-8")
        status, payload, _ = self.request(
            "POST",
            "/auth/login",
            encoded,
            {"Content-Type": "application/x-www-form-urlencoded"},
        )
        if status != 200:
            raise RuntimeError(f"Login failed ({status}): {payload}")


def compare(actual: Any, operation: str, expected: Any) -> bool:
    if operation == "eq":
        return actual == expected
    if operation == "contains":
        return normalize(expected) in normalize(actual)
    if operation == "lte":
        return actual is not None and float(actual) <= float(expected)
    if operation == "gte":
        return actual is not None and float(actual) >= float(expected)
    if operation == "in":
        return actual in expected
    raise ValueError(f"Unsupported property operation: {operation}")


def evaluate(payload: dict[str, Any], status: int, elapsed_ms: float, expected: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    response_text = str(payload.get("response") or payload.get("detail") or "")
    normalized_response = normalize(response_text)
    properties = payload.get("properties") or []
    metadata = payload.get("metadata") or {}
    criteria = metadata.get("criteria") or {}

    if status != expected.get("status", 200):
        failures.append(f"HTTP {status}, expected {expected.get('status', 200)}")
    if expected.get("response_non_empty", True) and not response_text.strip():
        failures.append("empty response")
    if expected.get("contains_any") and not any(normalize(item) in normalized_response for item in expected["contains_any"]):
        failures.append(f"response lacks any of {expected['contains_any']}")
    for item in expected.get("contains_all", []):
        if normalize(item) not in normalized_response:
            failures.append(f"response lacks {item!r}")
    for item in expected.get("not_contains", []):
        if normalize(item) in normalized_response:
            failures.append(f"response unexpectedly contains {item!r}")

    count = len(properties)
    if count < expected.get("min_properties", 0):
        failures.append(f"property count {count} < {expected['min_properties']}")
    if "max_properties" in expected and count > expected["max_properties"]:
        failures.append(f"property count {count} > {expected['max_properties']}")
    if expected.get("no_property_cards") and properties:
        failures.append(f"expected no cards, got {count}")

    for key, value in expected.get("criteria_equals", {}).items():
        if criteria.get(key) != value:
            failures.append(f"criteria.{key}={criteria.get(key)!r}, expected {value!r}")
    for key in expected.get("criteria_absent", []):
        if key in criteria and criteria.get(key) not in (None, "", []):
            failures.append(f"criteria.{key} should be absent, got {criteria.get(key)!r}")

    for rule in expected.get("property_all", []):
        for index, prop in enumerate(properties, 1):
            actual = nested_get(prop, rule["path"])
            if not compare(actual, rule.get("op", "eq"), rule["value"]):
                failures.append(
                    f"property #{index} {rule['path']}={actual!r} failed "
                    f"{rule.get('op', 'eq')} {rule['value']!r}"
                )

    if len(payload.get("suggested_actions") or []) < expected.get("actions_min", 0):
        failures.append("not enough suggested actions")
    if expected.get("auth_required") is not None and bool(payload.get("auth_required")) != expected["auth_required"]:
        failures.append(f"auth_required={payload.get('auth_required')!r}")
    if expected.get("ai_mode_in") and payload.get("ai_mode") not in expected["ai_mode_in"]:
        failures.append(f"ai_mode={payload.get('ai_mode')!r}")
    if elapsed_ms > expected.get("round_trip_ms_lte", float("inf")):
        failures.append(f"round trip {elapsed_ms:.0f} ms exceeds {expected['round_trip_ms_lte']} ms")
    if len(metadata.get("search_result_refs") or []) < expected.get("search_pool_min", 0):
        failures.append("search result pool was not preserved")

    if expected.get("geo_grounded"):
        evidence_exists = any(
            prop.get("distance_evidence") or prop.get("nearby_evidence")
            for prop in properties
        )
        unavailable_is_explicit = any(
            phrase in normalized_response
            for phrase in ("chua the xac minh", "chua duoc xac minh", "chua xac minh", "geo service")
        )
        provider_check_is_explicit = any(
            phrase in normalized_response
            for phrase in ("google routes", "google places", "google maps")
        )
        if not evidence_exists and not unavailable_is_explicit and not provider_check_is_explicit:
            failures.append("geo result has neither provider evidence nor explicit unavailable notice")

        unsupported_measurement = re.search(
            r"\b\d+(?:[.,]\d+)?(?:\s*[-–]\s*\d+(?:[.,]\d+)?)?\s*(?:km|phut)\b",
            normalized_response,
        )
        unsupported_nearby = re.search(
            r"\b(?:vi tri|can|nha|bat dong san).{0,50}\bgan\s+"
            r"(?:benh vien|truong|dai hoc|sieu thi|cong vien)\b",
            normalized_response,
        )
        if not evidence_exists and (unsupported_measurement or unsupported_nearby):
            failures.append("geo response makes an unsupported distance/nearby claim")

    return failures


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(description="Run Nera chatbot agent acceptance scenarios")
    parser.add_argument("--suite", type=Path, default=DEFAULT_SUITE)
    parser.add_argument("--base-url", default=os.getenv("BOOKINGBOT_API_BASE", "http://127.0.0.1:8000/api/v1"))
    parser.add_argument("--category", action="append", default=[])
    parser.add_argument("--limit", type=int)
    parser.add_argument("--timeout", type=float, default=35)
    parser.add_argument("--allow-side-effects", action="store_true")
    parser.add_argument("--email", default=os.getenv("BOOKINGBOT_TEST_EMAIL", ""))
    parser.add_argument("--password", default=os.getenv("BOOKINGBOT_TEST_PASSWORD", ""))
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    suite = json.loads(args.suite.read_text(encoding="utf-8"))
    scenarios = suite["scenarios"]
    if args.category:
        scenarios = [item for item in scenarios if item["category"] in set(args.category)]
    if args.limit:
        scenarios = scenarios[:args.limit]

    client = ApiClient(args.base_url, args.timeout)
    authenticated = False
    results = []
    passed = failed = skipped = 0

    for scenario in scenarios:
        if scenario.get("side_effecting") and not args.allow_side_effects:
            print(f"SKIP {scenario['id']} side effect disabled")
            skipped += 1
            continue
        if scenario.get("authenticated") and not authenticated:
            if not args.email or not args.password:
                print(f"SKIP {scenario['id']} missing BOOKINGBOT_TEST_EMAIL/PASSWORD")
                skipped += 1
                continue
            client.login(args.email, args.password)
            authenticated = True

        session_id = str(uuid.uuid4())
        scenario_failures: list[str] = []
        turn_results = []
        expectations = scenario.get("expect_turns") or []
        for index, turn in enumerate(scenario["turns"]):
            message = turn if isinstance(turn, str) else turn["message"]
            request_body = {"message": message, "session_id": session_id}
            if isinstance(turn, dict):
                request_body.update(turn.get("request", {}))
            status, payload, elapsed_ms = client.request(
                "POST", "/chat", request_body, {"X-Session-ID": session_id}
            )
            expected = expectations[index] if index < len(expectations) else (
                scenario.get("expect", {}) if index == len(scenario["turns"]) - 1 else {"status": 200}
            )
            failures = evaluate(payload, status, elapsed_ms, expected)
            scenario_failures.extend(f"turn {index + 1}: {item}" for item in failures)
            turn_results.append({
                "turn": index + 1,
                "message": message,
                "status": status,
                "elapsed_ms": round(elapsed_ms),
                "failures": failures,
                "response": str(payload.get("response") or payload.get("detail") or "")[:500],
                "criteria": (payload.get("metadata") or {}).get("criteria") or {},
                "property_count": len(payload.get("properties") or []),
                "ai_mode": payload.get("ai_mode"),
            })

        if scenario_failures:
            failed += 1
            print(f"FAIL {scenario['id']} [{scenario['category']}]")
            for failure in scenario_failures:
                print(f"     - {failure}")
        else:
            passed += 1
            print(f"PASS {scenario['id']} [{scenario['category']}]")
        results.append({**scenario, "failures": scenario_failures, "turn_results": turn_results})

    summary = {"passed": passed, "failed": failed, "skipped": skipped, "total": passed + failed + skipped}
    print(f"\nSUMMARY: {passed} passed, {failed} failed, {skipped} skipped")
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(
            json.dumps({"summary": summary, "results": results}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"Report: {args.report}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
