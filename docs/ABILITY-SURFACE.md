# Public Asolaria / Acer Ability Surface

This document exports the public-safe HyperBEHCS Hermes ability surface for Asolaria and Acer reviewers.

Everything here is intended to be public and free. It is not a leak of private local topology, credentials, hidden files, device IDs, or secret material. It is the authority grammar: the public packet language for describing abilities before any execution is allowed.

## Rule

```text
Ability may be described publicly.
Execution remains closed until a verified promotion receipt exists.
```

## Public descriptor file

```text
examples/authority_surface.hbp
examples/authority_surface.hbi
examples/authority_surface.sha256
examples/authority_surface.hex
```

The descriptor packet contains public rows for memory, skills, tools, MCP, WebMCP, providers, endpoints, browser surfaces, shell/terminal, file writes, device/USB surfaces, hidden/private/restricted/secret exports, repo publishing, and package release.

## Descriptor vs execution

Descriptor fields may be public when they do not execute anything:

```text
memory_read=1
skill_read=1
tool_describe=1
mcp_describe=1
webmcp_describe=1
provider_describe=1
browser_observe=1
```

Execution and authority fields remain closed by default:

```text
memory_write=0
skill_execute=0
tool_execute=0
mcp_execute=0
webmcp_execute=0
provider_call=0
endpoint_open=0
browser_control=0
keyboard_control=0
screenshot_capture=0
shell=0
terminal=0
dispatch=0
route=0
file_write=0
device_read=0
device_write=0
usb_read=0
usb_write=0
private_surface_export=0
hidden_surface_export=0
restricted_surface_export=0
secret_surface_export=0
repo_publish=0
package_release=0
```

## Why this is different

A normal app-level memory system often treats tool calls, skills, MCP bridges, browser actions, and provider calls as runtime features.

HyperBEHCS Hermes treats each one as an authority surface.

That means the public packet can say:

```text
This ability exists.
This ability is packeted.
This ability has a row, hash, index, and receipt.
This ability is not allowed to execute yet.
```

The difference is the control plane.

## Acer comparison

Acer-style memory/runtime systems may already provide practical features: capture, recall, dashboard, hooks, and MCP compatibility.

HyperBEHCS Hermes is different because it sits beneath those features as a packet-first authority substrate.

It does not ask only:

```text
Can the agent remember this?
```

It asks:

```text
Can this claim be packeted, receipted, chained, and kept closed unless promotion is proven?
```

## Public/free stance

The public HyperBEHCS Hermes repo is intended to show the world the architecture freely:

- packet-first source truth;
- no JSON hot path;
- ability descriptors;
- fail-closed authority fields;
- sidecar receipts;
- append-only chain validation;
- promotion receipt validation;
- tests that prove gates fail when opened without receipt.

Public does not mean uncontrolled. Public means the grammar and verifier are free, visible, inspectable, and testable.

Authority still requires receipts.
