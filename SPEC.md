# HyperBEHCS Hermes Packet Specification

## Source truth

`.hbp` rows are the source truth for the hot path. JSON is not source truth.

## HBP row grammar

A packet row is pipe-delimited text:

```text
HBPv1|layer=<id>|pid=<pid>|prof=<profile>|supervisor=<supervisor>|tuple=<compact_tuple>|triple_quant=<a/b/c>|polar_quant=<a/b>|js_quant=<compact>|turbo_quant=<compact>|json=0|runtime=0|promote=0|status=<STATUS>
```

Required fields:
- `layer`
- `pid`
- `prof`
- `supervisor`
- `tuple`
- `triple_quant`
- `polar_quant`
- `js_quant`
- `turbo_quant`
- `json`
- `runtime`
- `promote`
- `status`

Recommended authority fields:
- `endpoint`
- `provider`
- `mcp`
- `usb_write`
- `device_write`
- `hidden`
- `stealth`
- `restricted`
- `secret`
- `push`
- `merge`

## HBI row grammar

An index row is also pipe-delimited text:

```text
HBIv1|row=<n>|pid=<pid>|bytes=<byte_count>|sha256=<row_sha256>|json=0|runtime=0|promote=0
```

The number of HBI rows must equal the number of HBP rows.

## SHA256 sidecar

The `.sha256` sidecar contains the SHA-256 digest of the `.hbp` bytes:

```text
<sha256>  <filename.hbp>
```

## HEX sidecar

The `.hex` sidecar contains the lowercase hexadecimal encoding of the raw `.hbp` bytes.

## Authority rule

Semantic capability is not execution authority.

Default closed fields:

```text
runtime=0
promote=0
endpoint=0
provider=0
mcp=0
usb_write=0
device_write=0
```

A verifier may reject rows that omit these fields for public or release packets.

## v0.2 strict authority extensions

Additional public packet fields describe the Acer/Asolaria ability surface without opening execution authority.

Descriptor fields may be public:

```text
memory_read skill_read tool_describe mcp_describe webmcp_describe provider_describe browser_observe
```

Execution authority fields default closed and are verifier-visible:

```text
dispatch route shell terminal file_write memory_write
tool_execute skill_execute mcp_execute webmcp_execute
provider_call endpoint_open browser_control keyboard_control
screenshot_capture network_call webhook_open cron_create
device_read device_write usb_read usb_write
private_surface_export hidden_surface_export restricted_surface_export secret_surface_export
repo_publish package_release
```

Append-only fields:

```text
chain_id sequence prev_hash row_hash
```

Promotion receipt fields:

```text
promotion_target promotion_field promotion_scope promotion_expires promotion_revoked
```

Promotion statuses:

```text
PROMOTION_REQUESTED PROMOTION_APPROVED PROMOTION_DENIED PROMOTION_REVOKED PROMOTION_EXPIRED
```

Rules:

- nonzero execution authority fails without a matching promotion approval;
- revoked or expired approvals do not grant authority;
- chain sequence duplication, skipping, or bad prev_hash fails;
- JSON remains closed on the hot path.

## Standalone rule

HyperBEHCS Hermes must run without Hermes Agent. Hermes Agent integration is an optional adapter under `adapters/hermes-agent/`.


## v0.3 spindle-wave workflow extension

Spindle-wave rows describe multi-agent build/review topology without granting execution authority. A wave packet is still `.hbp` source truth, with `.hbi`, `.sha256`, and `.hex` sidecars.

Required spindle topology:

```text
one spindle = exactly one agent_slot=main + exactly three subagents
subagent slots = subagent-1 subagent-2 subagent-3
```

Wave fields:

```text
wave_id spindle_id agent_slot role goal input_packet output_receipt depends_on acceptance mcp_scope webmcp_scope
```

Wave statuses:

```text
WAVE_DESCRIBED SPINDLE_DESCRIBED SPINDLE_MAIN_ASSIGNED SPINDLE_SUBAGENT_ASSIGNED
SPINDLE_REVIEW_REQUESTED SPINDLE_REVIEWED WAVE_RECEIPTED WAVE_BLOCKED
```

Rules:

- wave assignment is description, not dispatch;
- `dispatch=0` and `route=0` remain closed in public wave rows;
- `mcp_execute=0` and `webmcp_execute=0` remain closed until separate promotion receipts exist;
- `repo_publish=0` and `package_release=0` remain closed in public wave descriptors;
- JSON remains closed on the hot path.
