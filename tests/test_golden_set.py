"""Bring the 222 golden scenarios that already exist under pytest.

They were written, grouped and kept up to date, but nothing ran them: the only
runner (`scripts/run_chat_agent_eval.py`) speaks HTTP to a live server, so CI
never touched them. A scenario file nobody executes rots quietly — a malformed
case is skipped rather than reported, and the suite still looks green.

Two gates live here, both free of a database and free of a model:

  * integrity — every case is loadable, uniquely identified and uses assertion
    keys the runner actually implements
  * constraint extraction — the single-turn cases are replayed through the pure
    regex extractor, which today decides every expected key on its own

The half that needs a live agent (retrieval, ranking, wording, geo) still runs
through the HTTP runner against a real stack. That split is deliberate: this
file is a PR gate, not a substitute for the nightly run.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.services.search_criteria_service import extract_search_criteria

EVAL_DIR = Path(__file__).resolve().parents[1] / "eval"

# Keys `scripts/run_chat_agent_eval.py` knows how to check. A case using anything
# else is silently ignored by the runner, which is worse than failing.
SUPPORTED_EXPECT_KEYS = {
    "actions_min",
    "auth_required",
    "contains_any",
    "criteria_absent",
    "criteria_equals",
    "geo_grounded",
    "max_properties",
    "min_properties",
    "no_property_cards",
    "not_contains",
    "property_all",
    "response_non_empty",
    "round_trip_ms_lte",
    "search_pool_min",
}


def load(name: str) -> list[dict]:
    payload = json.loads((EVAL_DIR / name).read_text(encoding="utf-8"))
    return payload["scenarios"]


ACCEPTANCE = load("chat_agent_acceptance.json")
SCENARIOS = load("chat_scenarios.json")
MULTITURN = load("chat_agent_multiturn_extended.json")
ALL_CASES = ACCEPTANCE + SCENARIOS + MULTITURN


# ── Integrity ────────────────────────────────────────────────────────────────


def test_the_golden_set_has_not_shrunk():
    """A ratchet. Cases may be added; losing them should be deliberate."""
    assert len(ACCEPTANCE) >= 150
    assert len(SCENARIOS) >= 60
    assert len(MULTITURN) >= 12


def test_every_case_id_is_unique():
    """Duplicate ids make a failing case impossible to trace back."""
    ids = [case["id"] for case in ALL_CASES]
    duplicates = {name for name in ids if ids.count(name) > 1}

    assert not duplicates, f"duplicate scenario ids: {sorted(duplicates)}"


@pytest.mark.parametrize("case", ALL_CASES, ids=lambda case: case["id"])
def test_every_case_has_something_to_say_and_something_to_check(case):
    assert case.get("turns"), f"{case['id']} has no user turns"
    assert case.get("category"), f"{case['id']} is uncategorised"
    if case["category"] != "validation":
        # A blank turn is the whole point of a validation case (CHAT-004 sends
        # whitespace); anywhere else it means a case that cannot exercise anything.
        assert all(
            str(turn).strip() for turn in case["turns"]
        ), f"{case['id']} has an empty turn"
    assert (
        case.get("expect") or case.get("assertions") or case.get("expect_turns")
    ), f"{case['id']} asserts nothing, so it can never fail"


@pytest.mark.parametrize("case", ACCEPTANCE, ids=lambda case: case["id"])
def test_acceptance_cases_only_use_keys_the_runner_implements(case):
    unknown = set(case["expect"]) - SUPPORTED_EXPECT_KEYS

    assert not unknown, (
        f"{case['id']} expects {sorted(unknown)}, which the runner ignores — "
        "the case would pass without ever being checked"
    )


# ── Constraint extraction, replayed without a model ──────────────────────────

SINGLE_TURN_WITH_CRITERIA = [
    case
    for case in ACCEPTANCE
    if len(case["turns"]) == 1 and (case.get("expect") or {}).get("criteria_equals")
]


@pytest.mark.parametrize(
    "case", SINGLE_TURN_WITH_CRITERIA, ids=lambda case: case["id"]
)
def test_the_regex_extractor_never_contradicts_the_golden_answer(case):
    """The extractor may stay silent and leave a key to the model.

    What it must never do is decide a key and decide it wrongly — that is a
    regression the model cannot correct, because the regex result wins.
    """
    extracted, _ = extract_search_criteria(case["turns"][0])

    for key, expected in case["expect"]["criteria_equals"].items():
        actual = extracted.get(key)
        if actual in (None, "", []):
            continue  # left to the model; the nightly run covers it
        assert actual == expected, (
            f"{case['id']} {case['turns'][0]!r}: "
            f"criteria.{key} extracted as {actual!r}, golden answer is {expected!r}"
        )


def test_the_extractor_still_decides_the_bulk_of_the_golden_criteria():
    """A ratchet on coverage.

    Every expected key is regex-decided today. If a change pushes work onto the
    model, the nightly bill goes up and this PR gate goes blind — so the floor
    is set just under the current number rather than at zero.
    """
    decided = total = 0
    for case in SINGLE_TURN_WITH_CRITERIA:
        extracted, _ = extract_search_criteria(case["turns"][0])
        for key in case["expect"]["criteria_equals"]:
            total += 1
            if extracted.get(key) not in (None, "", []):
                decided += 1

    assert total >= 120, "the golden criteria set shrank"
    assert decided >= 120, (
        f"only {decided}/{total} golden criteria are decided without a model; "
        "extraction regressed onto the LLM"
    )
