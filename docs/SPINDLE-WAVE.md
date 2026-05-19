# Spindle-wave workflow

Spindle-wave is the reusable HyperBEHCS Hermes workflow pattern for one main lane plus exactly three subagent lanes per spindle.

Core law:

```text
one spindle = one main + exactly three subagents
wave assignment is description, not dispatch
MCP/WebMCP are describe-only until separately promoted
packet rows are source truth
JSON is boundary-only/cold compatibility
```

A spindle-wave packet may describe agent responsibility, goals, acceptance receipts, and MCP/WebMCP build surfaces. It does not grant runtime, route, dispatch, shell, terminal, provider, endpoint, MCP execution, WebMCP execution, repo publish, or package release authority.

Verify the public MCP/WebMCP wave:

```bash
python -m hyperbehcs_hermes.cli wave verify packs/waves/public_spindle_wave_mcp_webmcp.hbp
python -m hyperbehcs_hermes.cli verify-chain packs/waves/public_spindle_wave_mcp_webmcp.hbp
```

Emit a deterministic template without executing it:

```bash
python -m hyperbehcs_hermes.cli wave template mcp-webmcp --wave-id WAVE-MCP-WEBMCP-v1
```

The template describes five spindles: authority/protocol, MCP core, WebMCP gateway, adapters, and CI/release. Each spindle has one `agent_slot=main` and exactly three subagents: `subagent-1`, `subagent-2`, and `subagent-3`.

A future adapter may read these rows and create live work only after a separate promotion receipt chain authorizes a narrow execution scope. The packet verifier remains the authority substrate; the adapter is not owner.
