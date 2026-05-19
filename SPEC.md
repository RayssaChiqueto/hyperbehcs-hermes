# HyperBEHCS Hermes Packet Specification v0.1

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

## Standalone rule

HyperBEHCS Hermes must run without Hermes Agent. Hermes Agent integration is an optional adapter under `adapters/hermes-agent/`.
