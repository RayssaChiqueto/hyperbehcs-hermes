# HyperBEHCS Hermes

HyperBEHCS Hermes is a standalone packet-first control-plane kernel for agent orchestration receipts, authority gates, and semantic routing.

Hermes Agent may host, read, or report HyperBEHCS packets through an adapter, but Hermes Agent does not own this project and is not required for the core verifier to work.

## Identity

The packet is source truth.

Hot path:
- `.hbp` packet rows
- `.hbi` packet indexes
- `.sha256` content receipts
- `.hex` byte receipts
- Markdown operator receipts

Cold compatibility only:
- JSON, external dashboards, APIs, or provider-specific transports

## What this does

- Parses HyperBEHCS packet rows.
- Builds `.hbi` indexes from `.hbp` packets.
- Verifies `.sha256` and `.hex` sidecars.
- Checks fail-closed authority gates.
- Provides a tiny CLI for read-only packet status.
- Provides an optional Hermes Agent adapter surface.

## What this does not do

- It does not grant runtime authority.
- It does not publish endpoints.
- It does not activate providers.
- It does not boot MCP/WebMCP.
- It does not write to USB/device surfaces.
- It does not scan raw private, hidden, secret, restricted, or stealth content.
- It does not make JSON source truth.

## Quick start

From this repository:

```text
python -m hyperbehcs_hermes.cli status examples/packet.hbp
python -m hyperbehcs_hermes.cli build-index examples/packet.hbp
python -m hyperbehcs_hermes.cli verify examples/packet.hbp
python -m unittest discover -s tests -v
```

Expected authority posture is fail-closed unless a packet explicitly carries a verified and operator-authorized promotion path. This starter release keeps `runtime=0`, `promote=0`, `endpoint=0`, `provider=0`, `mcp=0`, `usb_write=0`, and `device_write=0` in the examples.

## Project layout

```text
hyperbehcs-hermes/
  .github/workflows/      public CI: unit tests, packet verification, no tracked JSON
  adapters/hermes-agent/  optional adapter notes; not the kernel owner
  docs/                   authority and publishing boundary docs
  examples/               sample .hbp/.hbi/.sha256/.hex packet set
  hyperbehcs_hermes/      parser, indexer, verifier, gates, CLI
  indices/                packet index landing area
  packets/                packet landing area
  receipts/               bootstrap receipts
  tests/                  fail-closed unit tests
```

## Public preflight

```text
python -m unittest discover -s tests -v
python -m hyperbehcs_hermes.cli verify examples/packet.hbp
git ls-files '*.json'
```

The GitHub Actions workflow repeats these checks and fails if tracked JSON appears on the hot path.

See `docs/PUBLISHING.md` for the guarded GitHub publication flow.

## Boundary

This repository is public-safe by design: packets may describe authority, but cannot exercise authority. Any bridge to Hermes Agent, Asolaria, MCP, providers, endpoints, devices, or private filesystem surfaces must remain an adapter with explicit gates and receipts.
