"""Shared text cleanup for property data pulled from crawled listings."""

from __future__ import annotations

import re

_JUNK_TITLE_PREFIX = re.compile(r"^\s*gi[oỏ]\s*h[aà]ng\s*m[oớ]i\s*\|\|\s*", re.IGNORECASE)


def clean_property_title(raw_title: str | None) -> str | None:
    """Drop crawler marketing noise (e.g. "Giỏ hàng mới ||") from the front of a title."""
    if not raw_title:
        return raw_title
    return _JUNK_TITLE_PREFIX.sub("", raw_title).strip()


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
