# Quickstart

This is the fastest way to use HyperBEHCS Hermes after downloading it.

## 1. Clone

```bash
git clone https://github.com/RayssaChiqueto/hyperbehcs-hermes.git
cd hyperbehcs-hermes
```

## 2. Verify the starter packet

```bash
python -m hyperbehcs_hermes.cli verify examples/packet.hbp
```

Expected:

```text
HYPERBEHCS_VERIFY_BEGIN
OK=true
ROWS=2
```

## 3. Verify the public Asolaria/Acer ability surface

```bash
python -m hyperbehcs_hermes.cli verify examples/authority_surface.hbp
python -m hyperbehcs_hermes.cli verify-chain examples/authority_surface.hbp
```

Expected:

```text
OK=true
ROWS=32
```

## 4. Verify the public spindle-wave MCP/WebMCP plan

```bash
python -m hyperbehcs_hermes.cli verify packs/waves/public_spindle_wave_mcp_webmcp.hbp
python -m hyperbehcs_hermes.cli verify-chain packs/waves/public_spindle_wave_mcp_webmcp.hbp
python -m hyperbehcs_hermes.cli wave verify packs/waves/public_spindle_wave_mcp_webmcp.hbp
```

Expected:

```text
HYPERBEHCS_WAVE_VERIFY_BEGIN
OK=true
ROWS=20
SPINDLES=5
```

This plans/reviews MCP/WebMCP work lanes. It does not dispatch agents or open live bridges.

## 5. See the authority surface

```bash
python -m hyperbehcs_hermes.cli list-authority
```

This prints the public descriptor surface for memory, skills, tools, MCP, WebMCP, providers, browser, shell, terminal, file writes, devices, USB, private/hidden/restricted/secret exports, repo publishing, and package release.

## 6. See public packs

```bash
python -m hyperbehcs_hermes.cli list-packs
```

Public packs are under:

```text
packs/skills/
packs/tools/
packs/mcp/
packs/webmcp/
packs/providers/
packs/memory/
packs/browser/
packs/endpoints/
packs/hermes/
packs/local/
packs/proofs/
packs/waves/
```

## 7. Run the full test suite

```bash
python -m unittest discover -s tests -v
```

Expected:

```text
OK
```

## Meaning

If these commands pass, the downloaded repo is usable as a packet-first authority verifier and public descriptor pack.

It does not execute live tools. It proves the control plane first.

