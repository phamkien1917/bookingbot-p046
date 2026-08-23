"""Shared text cleanup for property data pulled from crawled listings."""

from __future__ import annotations

import re

_JUNK_TITLE_PREFIX = re.compile(r"^\s*gi[oỏ]\s*h[aà]ng\s*m[oớ]i\s*\|\|\s*", re.IGNORECASE)
_MISSING_SPACE_AFTER_COMMA = re.compile(r",(?!\s)")
_EXTRA_WHITESPACE = re.compile(r"\s+")


def _capitalize_word(word: str) -> str:
    """Capitalize a word's first letter, unless it looks like a code/acronym.

    Crawled titles mix real acronyms that must stay uppercase (PN, CĐT, HĐMB,
    KĐT) with plain lowercase words. A blunt ``str.title()`` mangles the
    acronyms (CĐT -> Cđt), so this only touches words that are not already
    all-uppercase and do not contain a digit (unit codes like "B10A", "i2").
    """
    core = re.sub(r"[^\wÀ-ỹ]", "", word)
    if not core or core.isupper() or any(ch.isdigit() for ch in core) or core[0].isupper():
        return word
    for i, ch in enumerate(word):
        if ch.isalpha():
            return word[:i] + ch.upper() + word[i + 1 :]
    return word


def _normalize_title_casing(title: str) -> str:
    """Fix "no space after comma" and capitalize plain lowercase words."""
    title = _MISSING_SPACE_AFTER_COMMA.sub(", ", title)
    title = _EXTRA_WHITESPACE.sub(" ", title).strip()
    return " ".join(_capitalize_word(word) for word in title.split(" "))


def clean_property_title(raw_title: str | None) -> str | None:
    """Drop crawler marketing noise and normalize casing/spacing on a property title."""
    if not raw_title:
        return raw_title
    title = _JUNK_TITLE_PREFIX.sub("", raw_title).strip()
    return _normalize_title_casing(title)


def build_full_address(
    address_line: str | None,
    ward: str | None,
    district: str | None,
    province: str | None,
) -> str:
    """Join address parts without repeating ward/district/province already present in address_line.

    Crawled ``address_line`` values are often already a full human-readable address
    (street + ward + district + province in one string), so appending the same
    ward/district/province again produces a visibly duplicated address.
    """
    if address_line:
        tail = ", ".join(filter(None, [ward, district, province]))
        if not tail or tail in address_line:
            return address_line
        return f"{address_line}, {tail}" if tail not in address_line else address_line
    return ", ".join(filter(None, [ward, district, province]))
