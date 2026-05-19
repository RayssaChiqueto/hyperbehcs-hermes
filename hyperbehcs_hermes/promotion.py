from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

from .authority import AUTHORITY_FIELDS, PROMOTION_STATUS
from .packet import PacketRow


@dataclass
class PromotionResult:
    ok: bool
    errors: list[str] = field(default_factory=list)


def _is_expired(value: str | None) -> bool:
    if not value or value == "never":
        return False
    try:
        if value.endswith("Z"):
            value = value[:-1] + "+00:00"
        expires = datetime.fromisoformat(value)
        if expires.tzinfo is None:
            expires = expires.replace(tzinfo=timezone.utc)
        return expires < datetime.now(timezone.utc)
    except ValueError:
        return True


def approved_promotions(rows: list[PacketRow]) -> set[tuple[str, str]]:
    approvals: set[tuple[str, str]] = set()
    for row in rows:
        if row.fields.get("status") != "PROMOTION_APPROVED":
            continue
        target = row.fields.get("promotion_target")
        field = row.fields.get("promotion_field")
        if not target or not field:
            continue
        if row.fields.get("promotion_revoked", "0") != "0":
            continue
        if _is_expired(row.fields.get("promotion_expires")):
            continue
        approvals.add((target, field))
    return approvals


def verify_promotions(rows: list[PacketRow]) -> PromotionResult:
    errors: list[str] = []
    approvals = approved_promotions(rows)

    for idx, row in enumerate(rows, 1):
        status = row.fields.get("status", "")
        if status in PROMOTION_STATUS:
            if status == "PROMOTION_APPROVED":
                if row.fields.get("promotion_revoked", "0") != "0":
                    errors.append(f"row {idx} approved promotion is revoked")
                if _is_expired(row.fields.get("promotion_expires")):
                    errors.append(f"row {idx} approved promotion is expired or malformed")
                for required in ("promotion_target", "promotion_field", "promotion_scope"):
                    if required not in row.fields:
                        errors.append(f"row {idx} promotion missing {required}")
            continue

        opened = row.open_authority_fields()
        for field, value in sorted(opened.items()):
            if field == "json":
                errors.append(f"row {idx} json hot path opened without approved promotion")
                continue
            if (row.pid, field) not in approvals:
                errors.append(f"row {idx} {row.pid} opens {field}={value} without approved promotion")

    return PromotionResult(not errors, errors)
