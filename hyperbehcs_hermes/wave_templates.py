from __future__ import annotations

from .authority import AUTHORITY_FIELDS
from .chain import chain_row_hash
from .packet import parse_row

CLOSED_AUTHORITY = {field: "0" for field in AUTHORITY_FIELDS}
DESCRIBE_ONLY = {
    "memory_read": "1",
    "skill_read": "1",
    "tool_describe": "1",
    "mcp_describe": "1",
    "webmcp_describe": "1",
    "provider_describe": "1",
    "browser_observe": "1",
}

SPINDLES = (
    ("SPINDLE-AUTHORITY-PROTOCOL", "architect-protocol", "packet-grammar", "authority-gates", "promotion-receipts"),
    ("SPINDLE-MCP-CORE", "mcp-architect", "tool-descriptor-mapper", "server-boundary-verifier", "receipt-test-writer"),
    ("SPINDLE-WEBMCP-GATEWAY", "webmcp-architect", "endpoint-descriptor-mapper", "browser-boundary-verifier", "web-receipt-test-writer"),
    ("SPINDLE-ADAPTERS", "adapter-architect", "hermes-agent-adapter", "provider-adapter", "cli-adapter"),
    ("SPINDLE-CI-RELEASE", "release-architect", "ci-verifier", "docs-verifier", "public-safety-verifier"),
)
SLOTS = ("main", "subagent-1", "subagent-2", "subagent-3")


def _row(fields: dict[str, str]) -> str:
    ordered = ["HBPv1"]
    ordered.extend(f"{key}={value}" for key, value in fields.items())
    return "|".join(ordered)


def mcp_webmcp_wave_rows(wave_id: str = "WAVE-MCP-WEBMCP-v1", chain_id: str = "PUBLIC-SPINDLE-WAVE-MCP-WEBMCP-v1") -> list[str]:
    rows: list[str] = []
    prev_hash = "ROOT"
    sequence = 1
    for spindle_id, main_role, sub1_role, sub2_role, sub3_role in SPINDLES:
        for slot, role in zip(SLOTS, (main_role, sub1_role, sub2_role, sub3_role)):
            status = "SPINDLE_MAIN_ASSIGNED" if slot == "main" else "SPINDLE_SUBAGENT_ASSIGNED"
            pid = f"PID-HBH-{wave_id}-{spindle_id}-{slot}".replace("_", "-")
            fields = {
                "layer": "spindle-wave",
                "pid": pid,
                "prof": "public-wave-descriptor",
                "supervisor": "fail-closed-public",
                "tuple": f"{wave_id}:{spindle_id}:{slot}:{role}",
                "triple_quant": "wave/spindle/receipt",
                "polar_quant": "describe/execute",
                "js_quant": "johnson-slithechen-public",
                "turbo_quant": "packet-first",
                "json": "0",
                "runtime": "0",
                "promote": "0",
                "status": status,
                "chain_id": chain_id,
                "sequence": str(sequence),
                "prev_hash": prev_hash,
                "wave_id": wave_id,
                "spindle_id": spindle_id,
                "agent_slot": slot,
                "role": role,
                "goal": f"build-full-mcp-webmcp-{role}",
                "input_packet": "NONE" if sequence == 1 else "PREVIOUS",
                "output_receipt": f"RECEIPT-{spindle_id}-{slot}",
                "depends_on": "NONE" if slot == "main" else f"{spindle_id}-main",
                "acceptance": "packet-first-fail-closed-review",
                "mcp_scope": "describe_only",
                "webmcp_scope": "describe_only",
                **CLOSED_AUTHORITY,
                **DESCRIBE_ONLY,
            }
            row = _row(fields)
            rows.append(row)
            prev_hash = chain_row_hash(parse_row(row))
            sequence += 1
    return rows


def mcp_webmcp_wave_text(wave_id: str = "WAVE-MCP-WEBMCP-v1") -> str:
    return "\n".join(mcp_webmcp_wave_rows(wave_id=wave_id)) + "\n"
