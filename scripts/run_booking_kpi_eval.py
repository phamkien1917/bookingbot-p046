"""Validate booking funnel/reminder/no-show analytics against the live API."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
from http.cookiejar import CookieJar


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--email", default=os.getenv("BOOKINGBOT_ADMIN_EMAIL", ""))
    parser.add_argument("--password", default=os.getenv("BOOKINGBOT_ADMIN_PASSWORD", ""))
    args = parser.parse_args()
    if not args.email or not args.password:
        print("Set BOOKINGBOT_ADMIN_EMAIL and BOOKINGBOT_ADMIN_PASSWORD", file=sys.stderr)
        return 2

    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(CookieJar()))
    login_data = urllib.parse.urlencode({"username": args.email, "password": args.password}).encode()
    with opener.open(f"{args.base_url}/api/v1/auth/login", login_data, timeout=20):
        pass
    with opener.open(f"{args.base_url}/api/v1/admin/analytics", timeout=20) as response:
        payload = json.load(response)

    failures: list[str] = []
    funnel = payload.get("conversion_funnel", {})
    reminder = payload.get("reminder_performance", {})
    for key in ("request_to_confirmed_rate", "appointment_completion_rate", "no_show_rate"):
        value = funnel.get(key)
        if not isinstance(value, (int, float)) or not 0 <= value <= 100:
            failures.append(f"invalid funnel metric {key}={value!r}")
    for key in ("delivery_success_rate", "reminded_no_show_rate"):
        value = reminder.get(key)
        if not isinstance(value, (int, float)) or not 0 <= value <= 100:
            failures.append(f"invalid reminder metric {key}={value!r}")
    if reminder.get("sent", 0) > reminder.get("scheduled", 0):
        failures.append("sent reminders exceed scheduled reminders")
    if funnel.get("no_show", 0) > funnel.get("appointments", 0):
        failures.append("no-shows exceed appointments")

    print(json.dumps({"passed": not failures, "failures": failures, "analytics": payload}, ensure_ascii=False, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
