#!/usr/bin/env python3
"""Rebuild missing .ai-log entries from Claude Code transcripts.

The hook in .claude/settings.json only loads when Claude Code opens the project
folder itself. Sessions opened one level up (d:\\AITHUCCHIEN) never load it, and
its cwd is not a git working tree either, so log_hook.py would drop the events
anyway. Those sessions leave no trace in .ai-log even though the work happened.

Claude Code still writes a full transcript per session under
~/.claude/projects/<slug>/<session-id>.jsonl. This reads those transcripts and
emits the same records the live hook would have written.

Every emitted record carries backfilled=true and the transcript it came from, so
a reconstructed entry is never mistaken for one captured live. Timestamps come
from the transcript; nothing here is invented.

Sessions already present in .ai-log are skipped, so re-running is safe.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections.abc import Iterator
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

VN_TZ = timezone(timedelta(hours=7))
PROMPT_LIMIT = 1000
RESPONSE_LIMIT = 500


def git(cmd: str, cwd: Path) -> str:
    try:
        return subprocess.check_output(
            cmd, shell=True, text=True, cwd=cwd, stderr=subprocess.DEVNULL
        ).strip()
    except Exception:
        return ""


def to_vn(timestamp: str) -> str:
    """Transcript timestamps are UTC; the live hook writes Vietnam time."""
    if not timestamp:
        return ""
    try:
        parsed = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError:
        return ""
    return parsed.astimezone(VN_TZ).isoformat()


def read_jsonl(path: Path) -> Iterator[dict[str, Any]]:
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


def logged_watermarks(log_dir: Path) -> dict[str, datetime]:
    """Newest already-logged timestamp per session.

    Skipping a whole session was right while a session lasted one sitting. A
    session that stays open for days is only logged up to the point the hook
    last fired, so session-level skipping silently drops everything after it —
    one long session lost an entire day of work that way.
    """
    watermarks: dict[str, datetime] = {}
    for path in list(log_dir.glob("*.jsonl")) + list((log_dir / "archive").glob("*.jsonl")):
        for record in read_jsonl(path):
            session_id = record.get("session_id")
            stamp = parse_ts(record.get("ts", ""))
            if not session_id or stamp is None:
                continue
            if session_id not in watermarks or stamp > watermarks[session_id]:
                watermarks[session_id] = stamp
    return watermarks


def parse_ts(value: str) -> datetime | None:
    try:
        return datetime.fromisoformat(value)
    except (TypeError, ValueError):
        return None


def message_text(message: dict[str, Any]) -> str:
    content = message.get("content")
    if isinstance(content, str):
        return content
    if not isinstance(content, list):
        return ""
    return " ".join(
        block.get("text", "")
        for block in content
        if isinstance(block, dict) and block.get("type") == "text"
    )


def session_model(records: list[dict[str, Any]]) -> str:
    for record in records:
        if record.get("type") == "assistant":
            model = (record.get("message") or {}).get("model")
            if model:
                return str(model)
    return ""


def touches_repo(records: list[dict[str, Any]], repo: str) -> bool:
    """Only sessions that actually worked on this repo belong in its log."""
    for record in records:
        if repo in str(record.get("trackingPath", "")):
            return True
        if record.get("type") == "assistant":
            for block in (record.get("message") or {}).get("content", []) or []:
                if isinstance(block, dict) and block.get("type") == "tool_use":
                    if repo in json.dumps(block.get("input", {}), ensure_ascii=False):
                        return True
    return False


def build_entries(
    records: list[dict[str, Any]], transcript_name: str, base: dict[str, Any]
) -> list[dict[str, Any]]:
    model = session_model(records)
    # A tool result arrives in a later user message, keyed by the tool_use id.
    results: dict[str, str] = {}
    for record in records:
        message = record.get("message") or {}
        for block in message.get("content", []) or []:
            if isinstance(block, dict) and block.get("type") == "tool_result":
                results[block.get("tool_use_id", "")] = str(block.get("content", ""))[
                    :RESPONSE_LIMIT
                ]

    entries: list[dict[str, Any]] = []
    for record in records:
        timestamp = to_vn(record.get("timestamp", ""))
        if not timestamp:
            continue
        common = {
            **base,
            "ts": timestamp,
            "session_id": record.get("sessionId", ""),
            "model": model,
            "branch": record.get("gitBranch") or "",
            "backfilled": True,
            "backfill_source": transcript_name,
        }

        if record.get("type") == "user" and (record.get("origin") or {}).get("kind") == "human":
            text = message_text(record.get("message") or {}).strip()
            if not text:
                continue
            entries.append(
                {
                    **common,
                    "event": "UserPromptSubmit",
                    "prompt": text[:PROMPT_LIMIT],
                    "tool_name": "",
                    "tool_input": None,
                    "tool_response": "",
                }
            )
        elif record.get("type") == "assistant":
            for block in (record.get("message") or {}).get("content", []) or []:
                if not isinstance(block, dict) or block.get("type") != "tool_use":
                    continue
                entries.append(
                    {
                        **common,
                        "event": "PostToolUse",
                        "prompt": "",
                        "tool_name": block.get("name", ""),
                        "tool_input": block.get("input"),
                        "tool_response": results.get(block.get("id", ""), ""),
                    }
                )

    entries.sort(key=lambda entry: entry["ts"])
    return entries


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    repo_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--transcripts",
        type=Path,
        required=True,
        help="Directory of Claude Code session transcripts.",
    )
    parser.add_argument("--log-dir", type=Path, default=repo_root / ".ai-log")
    parser.add_argument("--repo", default=repo_root.name)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report what would be written without touching any file.",
    )
    args = parser.parse_args()

    base = {
        "tool": "claude",
        "repo": args.repo,
        "commit": "",
        "student": git("git config user.email", repo_root),
    }

    watermarks = logged_watermarks(args.log_dir)
    by_date: dict[str, list[dict[str, Any]]] = {}
    skipped: list[str] = []

    for transcript in sorted(args.transcripts.glob("*.jsonl")):
        records = list(read_jsonl(transcript))
        if not records:
            continue
        session_id = next((r.get("sessionId") for r in records if r.get("sessionId")), "")
        if not touches_repo(records, args.repo):
            skipped.append(f"{transcript.name[:8]} never touched {args.repo}")
            continue
        watermark = watermarks.get(session_id)
        fresh = 0
        for entry in build_entries(records, transcript.name, base):
            stamp = parse_ts(entry["ts"])
            if watermark and stamp is not None and stamp <= watermark:
                continue
            by_date.setdefault(entry["ts"][:10], []).append(entry)
            fresh += 1
        if watermark and not fresh:
            skipped.append(f"{transcript.name[:8]} already logged through {watermark:%Y-%m-%d %H:%M}")
        elif watermark:
            print(f"resume: {transcript.name[:8]} after {watermark:%Y-%m-%d %H:%M} -> {fresh} new")

    for note in skipped:
        print(f"skip: {note}")

    total = 0
    for date in sorted(by_date):
        entries = sorted(by_date[date], key=lambda entry: entry["ts"])
        prompts = sum(1 for e in entries if e["event"] == "UserPromptSubmit")
        print(f"{date}: {len(entries):5d} entries ({prompts} prompts)")
        total += len(entries)
        if args.dry_run:
            continue
        target = args.log_dir / "archive" / f"{date}.jsonl"
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("a", encoding="utf-8") as handle:
            for entry in entries:
                handle.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(f"{'would write' if args.dry_run else 'wrote'} {total} backfilled entries")


def demo() -> None:
    base = {"tool": "claude", "repo": "P-046", "commit": "", "student": "x@y.z"}
    records = [
        {
            "type": "user",
            "origin": {"kind": "human"},
            "sessionId": "s1",
            "timestamp": "2026-08-29T03:00:00.000Z",
            "gitBranch": "develop",
            "message": {"role": "user", "content": [{"type": "text", "text": "chao"}]},
        },
        {
            "type": "assistant",
            "sessionId": "s1",
            "timestamp": "2026-08-29T03:00:05.000Z",
            "message": {
                "model": "claude-opus-5",
                "content": [
                    {"type": "thinking", "thinking": "hidden"},
                    {"type": "tool_use", "id": "t1", "name": "Read", "input": {"file_path": "a.py"}},
                ],
            },
        },
        {
            "type": "user",
            "sessionId": "s1",
            "timestamp": "2026-08-29T03:00:06.000Z",
            "message": {"content": [{"type": "tool_result", "tool_use_id": "t1", "content": "ok"}]},
        },
    ]

    entries = build_entries(records, "s1.jsonl", base)

    assert len(entries) == 2, "one prompt plus one tool use"
    assert entries[0]["event"] == "UserPromptSubmit"
    assert entries[0]["prompt"] == "chao"
    assert entries[1]["event"] == "PostToolUse"
    assert entries[1]["tool_name"] == "Read"
    assert entries[1]["tool_response"] == "ok", "tool result is matched back by id"
    assert all(e["backfilled"] is True for e in entries), "every entry is marked"
    assert all(e["model"] == "claude-opus-5" for e in entries)
    # A tool_result carries no human origin, so it must not become a prompt.
    assert not any(e["prompt"] == "ok" for e in entries)
    # 03:00 UTC is 10:00 in Vietnam.
    assert entries[0]["ts"].startswith("2026-08-29T10:00:00"), entries[0]["ts"]
    assert to_vn("") == "" and to_vn("not-a-date") == ""
    print("demo ok")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo()
    else:
        main()
