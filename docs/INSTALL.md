# Install HyperBEHCS Hermes

HyperBEHCS Hermes is designed so a normal person can download the repo and use it immediately.

## Requirements

- Python 3.10+
- Git

No runtime Python dependencies are required beyond the standard library.

## Clone

```bash
git clone https://github.com/RayssaChiqueto/hyperbehcs-hermes.git
cd hyperbehcs-hermes
```

## Run without installing

```bash
python -m hyperbehcs_hermes.cli status examples/packet.hbp
python -m hyperbehcs_hermes.cli verify examples/packet.hbp
python -m hyperbehcs_hermes.cli verify examples/authority_surface.hbp
python -m hyperbehcs_hermes.cli verify-chain examples/authority_surface.hbp
```

## Install locally

```bash
python -m pip install -e .
```

Then run:

```bash
hyperbehcs-hermes status examples/packet.hbp
hyperbehcs-hermes verify examples/authority_surface.hbp
hyperbehcs-hermes verify-chain examples/authority_surface.hbp
hyperbehcs-hermes list-authority
hyperbehcs-hermes list-packs
```

## Run tests

```bash
python -m unittest discover -s tests -v
```

Expected result:

```text
OK
```

## Verify every public pack

```bash
for f in packs/*/*.hbp; do
  python -m hyperbehcs_hermes.cli verify "$f"
  python -m hyperbehcs_hermes.cli verify-chain "$f"
done
```

## What you can use immediately

After clone, you can inspect and verify:

```text
examples/packet.hbp
examples/authority_surface.hbp
examples/promotion_request.hbp
examples/promotion_approved.hbp
examples/promotion_revoked.hbp
packs/skills/public_skill_descriptors.hbp
packs/tools/public_tool_descriptors.hbp
packs/mcp/public_mcp_descriptors.hbp
packs/webmcp/public_webmcp_descriptors.hbp
packs/providers/public_provider_descriptors.hbp
packs/memory/public_memory_descriptors.hbp
```

## What is intentionally not live by default

The public repo does not turn on shell, tools, MCP, WebMCP, providers, endpoints, browser control, device writes, USB writes, memory mutation, private export, or package release.

Those surfaces are described and tested. They remain closed until a valid promotion receipt exists.
