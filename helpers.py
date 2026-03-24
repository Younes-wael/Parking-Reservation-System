# =========================
# Helpers
# =========================
from __future__ import annotations

import re
from datetime import date, timedelta


def normalize_spaces(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip())


def is_valid_reservation_number(s: str) -> bool:
    # Accepts alphanumeric + dash, 4–32 chars
    s = (s or "").strip()
    return bool(re.fullmatch(r"[A-Za-z0-9-]{4,32}", s))


def nights_between(check_in: date, check_out: date) -> int:
    return (check_out - check_in).days


def daterange(start: date, end: date) -> list[date]:
    """Inclusive range of dates."""
    if end < start:
        return []
    days = (end - start).days
    return [start + timedelta(days=i) for i in range(days + 1)]

