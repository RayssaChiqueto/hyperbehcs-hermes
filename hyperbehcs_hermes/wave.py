from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field

from .authority import AUTHORITY_FIELDS
from .packet import PacketRow

REQUIRED_AGENT_SLOTS = ("main", "subagent-1", "subagent-2", "subagent-3")
REQUIRED_SUBAGENT_SLOTS = ("subagent-1", "subagent-2", "subagent-3")
REQUIRED_WAVE_FIELDS = (
    "wave_id",
    "spindle_id",
    "agent_slot",
    "role",
    "goal",
    "input_packet",
    "output_receipt",
    "depends_on",
    "acceptance",
    "mcp_scope",
    "webmcp_scope",
)
WAVE_DESCRIPTOR_STATUSES = {
    "WAVE_DESCRIBED",
    "SPINDLE_DESCRIBED",
    "SPINDLE_MAIN_ASSIGNED",
    "SPINDLE_SUBAGENT_ASSIGNED",
    "SPINDLE_REVIEW_REQUESTED",
    "SPINDLE_REVIEWED",
    "WAVE_RECEIPTED",
    "WAVE_BLOCKED",
}


@dataclass(frozen=True)
class WaveAgentAssignment:
    row_number: int
    wave_id: str
    spindle_id: str
    agent_slot: str
    role: str
    goal: str
    pid: str


@dataclass
class SpindleTopology:
    wave_id: str
    spindle_id: str
    assignments: list[WaveAgentAssignment] = field(default_factory=list)

    @property
    def slots(self) -> list[str]:
        return [assignment.agent_slot for assignment in self.assignments]


@dataclass
class WaveValidationResult:
    ok: bool
    rows: int
    spindles: int
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def receipt_lines(self) -> list[str]:
        lines = [
            "HYPERBEHCS_WAVE_VERIFY_BEGIN",
            f"OK={str(self.ok).lower()}",
            f"ROWS={self.rows}",
            f"SPINDLES={self.spindles}",
            "TOPOLOGY=one-main-exactly-three-subagents",
            "AUTHORITY=fail-closed",
            "JSON_HOT_PATH=closed",
        ]
        lines.extend(f"ERROR={error}" for error in self.errors)
        lines.extend(f"WARNING={warning}" for warning in self.warnings)
        return lines


def rows_to_wave_assignments(rows: list[PacketRow]) -> list[WaveAgentAssignment]:
    assignments: list[WaveAgentAssignment] = []
    for idx, row in enumerate(rows, 1):
        fields = row.fields
        if fields.get("layer") != "spindle-wave":
            continue
        assignments.append(
            WaveAgentAssignment(
                row_number=idx,
                wave_id=fields.get("wave_id", ""),
                spindle_id=fields.get("spindle_id", ""),
                agent_slot=fields.get("agent_slot", ""),
                role=fields.get("role", ""),
                goal=fields.get("goal", ""),
                pid=row.pid,
            )
        )
    return assignments


def validate_spindle_wave(rows: list[PacketRow], require_closed: bool = True) -> WaveValidationResult:
    errors: list[str] = []
    warnings: list[str] = []
    assignments = rows_to_wave_assignments(rows)

    if not rows:
        errors.append("empty packet")
    if not assignments:
        errors.append("no spindle-wave rows found")

    for idx, row in enumerate(rows, 1):
        fields = row.fields
        if fields.get("layer") != "spindle-wave":
            errors.append(f"row {idx} layer must be spindle-wave")
        missing = row.missing_required()
        if missing:
            errors.append(f"row {idx} missing required fields: {','.join(missing)}")
        if fields.get("json") != "0":
            errors.append(f"row {idx} json hot path is not closed")
        if fields.get("runtime") != "0":
            errors.append(f"row {idx} runtime is not closed")
        if fields.get("promote") != "0":
            errors.append(f"row {idx} promote is not closed")
        status = fields.get("status", "")
        if status not in WAVE_DESCRIPTOR_STATUSES:
            errors.append(f"row {idx} unsupported wave status: {status}")
        for required in REQUIRED_WAVE_FIELDS:
            if not fields.get(required):
                errors.append(f"row {idx} missing wave field: {required}")
        if fields.get("mcp_scope") != "describe_only":
            errors.append(f"row {idx} mcp_scope must be describe_only")
        if fields.get("webmcp_scope") != "describe_only":
            errors.append(f"row {idx} webmcp_scope must be describe_only")
        missing_authority = [field for field in AUTHORITY_FIELDS if field not in fields]
        if missing_authority:
            errors.append(f"row {idx} missing closed authority fields: {','.join(missing_authority)}")
        if require_closed:
            opened = row.open_authority_fields()
            if opened:
                errors.append(f"row {idx} opens authority fields: {opened}")
        for field in AUTHORITY_FIELDS:
            value = fields.get(field)
            if value is not None and value not in {"0", "1"}:
                errors.append(f"row {idx} authority field {field} must be 0 or 1")

    grouped: dict[tuple[str, str], list[WaveAgentAssignment]] = defaultdict(list)
    for assignment in assignments:
        grouped[(assignment.wave_id, assignment.spindle_id)].append(assignment)

    for (wave_id, spindle_id), group in sorted(grouped.items()):
        label = f"wave {wave_id} spindle {spindle_id}"
        slots = [assignment.agent_slot for assignment in group]
        unknown = sorted(slot for slot in slots if slot not in REQUIRED_AGENT_SLOTS)
        if unknown:
            errors.append(f"{label} has unsupported slots: {','.join(unknown)}")
        main_count = slots.count("main")
        if main_count != 1:
            errors.append(f"{label} expected 1 main got {main_count}")
        subagent_count = sum(1 for slot in slots if slot in REQUIRED_SUBAGENT_SLOTS)
        if subagent_count != 3:
            errors.append(f"{label} expected 3 subagents got {subagent_count}")
        for slot in REQUIRED_AGENT_SLOTS:
            count = slots.count(slot)
            if count != 1:
                errors.append(f"{label} expected exactly one {slot} got {count}")

    return WaveValidationResult(not errors, len(rows), len(grouped), errors, warnings)


def wave_receipt_lines(result: WaveValidationResult) -> list[str]:
    return result.receipt_lines()
