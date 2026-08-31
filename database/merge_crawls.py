"""Merge crawl JSON files into one deduplicated list for generate_sql_from_json.py.

A nationwide pass and a city pass overlap, and the same listing must appear once.
Later files win so a fresher crawl of the same listing replaces the older record.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def merge(paths: list[Path]) -> list[dict]:
    merged: dict[str, dict] = {}
    for path in paths:
        records = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(records, list):
            raise ValueError(f"{path} must contain a list of normalized properties")
        for record in records:
            merged[str(record["property_id"])] = record
    return sorted(merged.values(), key=lambda item: str(item["property_id"]))


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if len(sys.argv) < 3:
        raise SystemExit("usage: merge_crawls.py OUTPUT INPUT [INPUT ...]")
    output = Path(sys.argv[1])
    inputs = [Path(argument) for argument in sys.argv[2:]]
    records = merge(inputs)
    output.write_text(
        json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Merged {sum(1 for _ in inputs)} file(s) into {output}: {len(records)} unique")


def demo() -> None:
    a = [{"property_id": "P_1", "price": 1}, {"property_id": "P_2", "price": 2}]
    b = [{"property_id": "P_2", "price": 99}, {"property_id": "P_3", "price": 3}]
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        first = Path(directory) / "a.json"
        second = Path(directory) / "b.json"
        first.write_text(json.dumps(a), encoding="utf-8")
        second.write_text(json.dumps(b), encoding="utf-8")
        result = merge([first, second])
    assert [item["property_id"] for item in result] == ["P_1", "P_2", "P_3"]
    assert result[1]["price"] == 99, "later file must win on a duplicate listing"
    print("demo ok")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo()
    else:
        main()
