# Local Acer / Asolaria Proof Crosswalk

Public HyperBEHCS Hermes should show enough of the local Acer/Asolaria shape for people to understand the system without exporting private runtime, authority, secrets, inbox/outbox data, leases, or raw local files.

This document is a public-safe crosswalk. It maps local operational classes to public descriptor concepts.

## Boundary

Public may include:

- aggregate counts;
- conceptual class names;
- descriptor packet rows;
- proof categories;
- authority fields;
- fail-closed posture;
- docs explaining why local runtime is larger than public seed.

Public must not include:

- raw private runtime state;
- local auth material;
- provider keys;
- private inbox/outbox data;
- leases or live endpoint credentials;
- raw private/hidden/restricted/secret file contents;
- recursive device or USB inventory;
- active daemon control surfaces;
- exact private room contents.

## Crosswalk table

| Local Acer/Asolaria surface | Public descriptor concept | Public posture |
|---|---|---|
| 47 current connectors + 43 ASO mirror connectors | connector descriptor rows | describe only, execute closed |
| 59 local skills | skill descriptor rows | read public metadata, execution closed |
| 614 BEHCS tools / 242 hyperbehcs tools | tool descriptor rows | describe catalog, execution closed |
| 33 HyperHermes/Hermes tools | Hermes tool descriptor rows | describe catalog, execution closed |
| 10 MCP/WebMCP BEHCS tools | MCP/WebMCP descriptor rows | describe bridge, execute closed |
| 21 local src/behcs modules | module descriptor rows | proof/crosswalk only |
| 20 Hermes engines | engine descriptor rows | describe engine class, runtime closed |
| 24 helper slots | helper descriptor rows | route/dispatch closed |
| 15 plugins | plugin descriptor rows | describe plugin class, activation closed |
| 13 fabric layers | fabric descriptor rows | describe layer, mutation closed |
| 2 subagent runtimes | subagent runtime descriptors | dispatch/runtime closed |
| 167 upstream Hermes skills indexed | upstream skill index descriptors | metadata only |
| 411 GNN edges | graph proof descriptors | topology class only, no private node payload |
| 9 Hookwall patterns | hookwall descriptors | pattern class only, no live hook activation |
| 10K-room rotor/prism/room surfaces | room-surface descriptors | aggregate only, no private room contents |
| Local quant/substrate/daemon/core pieces | substrate descriptors | proof only, runtime closed |

## Packet implication

The local active system is deeper than public v0.2/v0.2.1, but the public repo now carries the grammar needed to describe it safely:

```text
local ability -> public descriptor row -> sidecars -> verifier -> chain check -> promotion gate
```

The public descriptor is not a runtime permission.

## Promotion implication

If a future release exposes any live bridge, it must be represented as a promotion receipt with scoped authority fields. Until then:

```text
tool_execute=0
skill_execute=0
mcp_execute=0
webmcp_execute=0
provider_call=0
memory_write=0
browser_control=0
shell=0
terminal=0
repo_publish=0
package_release=0
```

## Why this matters

Public users need more than a kernel; they need the shape of what the kernel governs. This crosswalk gives them that shape without exporting the private/local engine.
