# Publishing the Usable Stuff Around HyperBEHCS Hermes

HyperBEHCS Hermes is the packet/verifier kernel. For people to actually use it, the public repo also needs the usable surrounding material: descriptors, examples, adapters, docs, tests, and eventually import/export bridges.

This document names that boundary clearly.

## What the kernel is

HyperBEHCS Hermes core:

```text
.hbp packet rows
.hbi indexes
.sha256 receipts
.hex byte mirrors
authority fields
append-only chain verifier
promotion verifier
CLI
CI tests
```

That proves the source-truth and authority layer.

## What users also need

To use it, Asolaria, Acer, and outside builders need public packs around the kernel:

```text
ability surface packs
skill descriptor packs
tool descriptor packs
MCP descriptor packs
WebMCP descriptor packs
provider descriptor packs
memory descriptor packs
promotion receipt examples
adapter templates
operator docs
example workflows
```

These should be public and free too, as long as they are descriptor-safe and do not expose secrets, credentials, private paths, raw hidden content, or uncontrolled runtime authority.

## Descriptor packs vs live authority

A descriptor pack can be public:

```text
This tool exists.
This skill exists.
This MCP bridge category exists.
This WebMCP route category exists.
This provider class exists.
This memory surface exists.
This ability is read-only or execute-capable.
This execution field defaults closed.
```

A live authority grant still requires receipt validation:

```text
This exact pid may open this exact field under this exact scope until this expiry.
```

## Public pack roadmap

1. `examples/authority_surface.hbp`

   Already added. This is the public Asolaria/Acer ability surface.

2. `packs/skills/*.hbp`

   Public skill descriptors: what a skill is, what it reads, what it may execute, and which fields remain closed.

3. `packs/tools/*.hbp`

   Public tool descriptors: browser, file, shell, terminal, web, GitHub, cron, memory, etc., each separated into describe/read/execute authority.

4. `packs/mcp/*.hbp`

   MCP server/tool descriptors without live credentials or endpoint activation.

5. `packs/webmcp/*.hbp`

   WebMCP bridge descriptors without opening browser/network authority by default.

6. `packs/providers/*.hbp`

   Provider/model descriptors without API keys or active calls.

7. `packs/memory/*.hbp`

   Memory tier descriptors: working, episodic, semantic, procedural, public canon, local private, gated private.

8. `templates/adapter-*`

   Adapter templates for importing/exporting descriptors from real tools while keeping runtime authority closed.

## Rule for publishing everything

Publish the grammar, descriptors, tests, examples, templates, and verifier.

Do not publish:

- credentials;
- API keys;
- private file contents;
- raw secret/hidden/restricted data;
- local device IDs that identify private hardware;
- live endpoint URLs with auth;
- uncontrolled runtime grants.

The world gets the system. Authority still requires receipts.
