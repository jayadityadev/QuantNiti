"""Shared request-validation helpers.

These helpers exist so API routes can reject malformed user input with a clear
4xx response instead of letting downstream pandas/lookup code raise a generic
500 (or silently substitute synthetic data).
"""

from datetime import date, datetime
from typing import Optional, Tuple

_DATE_FORMAT = "%Y-%m-%d"


def parse_date_param(value: Optional[str], field_name: str) -> Optional[date]:
    """Parse a ``YYYY-MM-DD`` query/body date, raising ``ValueError`` when invalid."""
    if value is None or str(value).strip() == "":
        return None
    text = str(value).strip()
    try:
        return datetime.strptime(text, _DATE_FORMAT).date()
    except ValueError as exc:
        raise ValueError(
            f"Invalid {field_name} '{value}'. Expected format YYYY-MM-DD."
        ) from exc


def validate_date_range(
    start_date: Optional[str], end_date: Optional[str]
) -> Tuple[Optional[date], Optional[date]]:
    """Validate and normalise an optional ``start_date``/``end_date`` pair."""
    start = parse_date_param(start_date, "start_date")
    end = parse_date_param(end_date, "end_date")
    if start is not None and end is not None and start > end:
        raise ValueError("start_date must be on or before end_date.")
    return start, end
