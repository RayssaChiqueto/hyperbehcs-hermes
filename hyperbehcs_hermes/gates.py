from __future__ import annotations

from .authority import LEGACY_CLOSED_FIELDS
from .packet import PacketRow


def authority_posture(row: PacketRow) -> str:
    opened = row.open_authority_fields()
    if opened:
        return "OPEN:" + ",".join(f"{key}={value}" for key, value in sorted(opened.items()))
    missing = [key for key in LEGACY_CLOSED_FIELDS if key not in row.fields]
    if missing:
        return "MISSING_CLOSED_FIELDS:" + ",".join(missing)
    return "FAIL_CLOSED"
