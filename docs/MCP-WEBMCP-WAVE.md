# MCP/WebMCP spindle-wave build plan

The public packet is `packs/waves/public_spindle_wave_mcp_webmcp.hbp`.

It is deliberately inert. It describes work lanes and acceptance receipts; it does not start an MCP server, open a WebMCP bridge, call a provider, control a browser, publish a repository, or release a package.

Gate sequence before any live bridge exists:

1. Verify packet sidecars.
2. Verify append-only chain.
3. Verify spindle topology.
4. Verify no tracked JSON hot path.
5. Verify all execution authority fields remain closed.
6. Add promotion receipts for a narrow adapter test scope.
7. Verify promotions before an adapter executes anything.
8. Append receipts back into packet form.

CLI gates:

```bash
python -m hyperbehcs_hermes.cli verify packs/waves/public_spindle_wave_mcp_webmcp.hbp
python -m hyperbehcs_hermes.cli verify-chain packs/waves/public_spindle_wave_mcp_webmcp.hbp
python -m hyperbehcs_hermes.cli wave verify packs/waves/public_spindle_wave_mcp_webmcp.hbp
```

Spindles:

- `SPINDLE-AUTHORITY-PROTOCOL`: packet grammar, authority gates, promotion receipts.
- `SPINDLE-MCP-CORE`: MCP descriptors, server boundary checks, receipt tests.
- `SPINDLE-WEBMCP-GATEWAY`: endpoint descriptors, browser boundary checks, web receipts.
- `SPINDLE-ADAPTERS`: Hermes Agent adapter, provider adapter, CLI adapter.
- `SPINDLE-CI-RELEASE`: CI verifier, docs verifier, public safety verifier.

What remains adapter-only until promotion: MCP tool calls, WebMCP bridge opening, provider/model calls, browser control, endpoint open, repo publishing, and package release.
