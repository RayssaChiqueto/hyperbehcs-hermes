# HyperBEHCS Hermes

HyperBEHCS Hermes is a standalone packet-first control-plane kernel for agent orchestration receipts, authority gates, semantic routing, and future MCP/WebMCP/tool-skill adapters.

It is not a normal memory app. It is not a JSON-first agent wrapper. It is not a dashboard pretending to be a kernel.

HyperBEHCS Hermes makes the packet the source truth.

Hermes Agent may host, read, or report HyperBEHCS packets through an adapter, but Hermes Agent does not own this project and is not required for the core verifier to work.

## One-line identity

HyperBEHCS Hermes is the public seed of a BEHCS/HyperBEHCS packet kernel: `.hbp` packets, `.hbi` indexes, `.sha256` receipts, `.hex` byte mirrors, fail-closed authority gates, and adapter boundaries for tools, skills, MCP, WebMCP, providers, memory, and agent runtimes.

## Why this exists

Most agent-memory systems solve the question:

> How do I help an AI coding agent remember what happened?

HyperBEHCS Hermes solves a deeper question:

> How do I let an agent remember, route, reason, and connect tools without accidentally granting authority?

That difference matters.

Agent memory by itself is useful, but memory can become dangerous when it is connected to tools, endpoints, MCP servers, browsers, shell commands, provider keys, file systems, USB/device surfaces, or hidden/private data. HyperBEHCS Hermes is built around the rule that semantic capability is not execution authority.

A packet can describe a capability. That does not mean the capability is allowed to run.

A packet can describe a tool. That does not mean the tool may execute.

A packet can describe an MCP/WebMCP bridge. That does not mean the bridge may open.

A packet can describe a memory. That does not mean it may mutate canon, leak secrets, or promote itself into runtime.

## Quickstart: download and use

```bash
git clone https://github.com/RayssaChiqueto/hyperbehcs-hermes.git
cd hyperbehcs-hermes
python -m hyperbehcs_hermes.cli verify examples/packet.hbp
python -m hyperbehcs_hermes.cli verify examples/authority_surface.hbp
python -m hyperbehcs_hermes.cli verify-chain examples/authority_surface.hbp
python -m hyperbehcs_hermes.cli list-authority
python -m hyperbehcs_hermes.cli list-packs
```

Optional local install:

```bash
python -m pip install -e .
hyperbehcs-hermes verify examples/authority_surface.hbp
hyperbehcs-hermes list-authority
```

Use docs:

```text
docs/INSTALL.md
docs/QUICKSTART.md
docs/PUBLISH-THE-STUFF.md
docs/LOCAL-PROOF-CROSSWALK.md
```

## Core law

```text
The packet is source truth.
JSON is not source truth.
Capability is not authority.
Memory is not permission.
Adapter is not owner.
Fail closed before promotion.
```

## Hot path

Native HyperBEHCS Hermes artifacts:

```text
.hbp     packet rows / source truth
.hbi     packet indexes
.sha256  content receipts
.hex     byte receipts / compact mirror
.md      operator-readable receipts and docs
```

Cold compatibility only:

```text
external APIs
provider transports
MCP / WebMCP JSON-RPC boundaries
browser dashboards
third-party tools
legacy import/export formats
```

If an outside system forces JSON, JSON belongs at the boundary adapter only. It must not become the HyperBEHCS Hermes brain.

## What this public release does

This release is a public-safe authority grammar and descriptor-pack seed. It currently:

- Parses HyperBEHCS packet rows.
- Builds `.hbi` indexes from `.hbp` packets.
- Verifies `.sha256` sidecars.
- Verifies `.hex` sidecars.
- Detects open authority fields.
- Enforces `json=0` for packet hot path rows.
- Keeps example packets fail-closed.
- Provides an installable Python CLI for packet status, verification, chain checks, promotion checks, authority listing, and pack listing.
- Includes six public descriptor packs for skills, tools, MCP, WebMCP, providers, and memory.
- Includes a 32-row public authority surface for Asolaria/Acer review.
- Includes append-only chain verification.
- Includes promotion receipt verification.
- Provides optional Hermes Agent adapter notes without making Hermes Agent the owner.
- Runs public CI on GitHub Actions.
- Enforces no tracked JSON files in CI.
- Includes basic public-safety content needles in CI.

## What this public release does not do yet

This release intentionally does not grant authority or open live bridges. It does not include the complete private/local runtime.

It does not yet:

- Grant runtime authority.
- Publish endpoints.
- Activate providers.
- Boot MCP/WebMCP.
- Execute tools.
- Execute skills.
- Write to USB/device surfaces.
- Scan raw private, hidden, secret, restricted, or stealth content.
- Validate a full cosign/quorum promotion chain.
- Provide a production memory viewer.
- Replace Hermes Agent, Claude Code, Cursor, Gemini CLI, or other agent runtimes.

That boundary is intentional. The seed must be safe before the bridge becomes live.

## Is this better than normal agent memory systems?

It depends on what is being compared.

For plug-and-play convenience today, a mature memory app may have more product features: viewer, server, embeddings, REST, team sharing, lifecycle hooks, and packaged install.

For Asolaria/HyperBEHCS authority design, HyperBEHCS Hermes is better because it starts underneath the app layer. It treats memory, tools, skills, MCP, WebMCP, and provider access as authority-bearing surfaces that must be packeted, receipted, indexed, and gated.

The difference is not just implementation language or storage engine. The difference is posture.

Typical agent memory system:

```text
agent event -> memory store -> search/retrieve -> inject context
```

HyperBEHCS Hermes:

```text
agent/tool/memory claim -> packet -> index -> receipt -> authority gate -> adapter boundary -> optional runtime
```

The important question is not only "can the agent remember?"

The important question is:

```text
Can the system prove what was remembered, where it came from, whether it was allowed to promote, and which authority surfaces stayed closed?
```

HyperBEHCS Hermes is designed around that proof path.

## Comparison: HyperBEHCS Hermes vs app-level agent memory

| Axis | App-level agent memory | HyperBEHCS Hermes |
| --- | --- | --- |
| Primary goal | Help agents remember sessions | Packetize memory/capability under authority gates |
| Source truth | Database rows, events, API objects | `.hbp` packet rows |
| Index | Search/vector/KG index | `.hbi` packet index, future semantic indexes as adapters |
| Integrity | App database consistency | `.sha256` and `.hex` receipts |
| Default posture | Capture and retrieve | Fail closed |
| Tool relation | Tool calls become memory events | Tool capability is described separately from authority to execute |
| MCP relation | MCP often acts as live tool surface | MCP/WebMCP must be adapter-gated and receipted |
| JSON relation | Common internal and wire format | Boundary compatibility only, not source truth |
| Forgetting | May decay or evict stale memories | Decay may rank retrieval, but canon should not be silently erased |
| Governance | Usually user/app policy | Packet authority, promotion receipts, future cosign/quorum chain |
| Best use | Practical agent memory product | Control-plane substrate for agent memory, tools, skills, and runtime gates |

## Comparison: HyperBEHCS Hermes vs Acer-style memory/runtime versions

This repository should not be framed as "the same thing with another name." It is different in layer, authority model, and failure posture.

Acer-style agent memory/runtime stacks are useful when they provide:

- agent session capture;
- lifecycle hooks;
- memory recall;
- tool history;
- repo context;
- vector or keyword search;
- MCP-compatible tool surfaces;
- web or local dashboards;
- practical operator UX.

HyperBEHCS Hermes is different because it is not trying to be only a memory product. It is a packet-first authority substrate that can sit below those capabilities.

Where HyperBEHCS Hermes is stronger:

1. Source-truth discipline

   The native object is the packet, not a database row or JSON event blob.

2. Authority separation

   A skill, tool, MCP bridge, provider, browser, endpoint, or memory can be described without being allowed to execute.

3. Fail-closed defaults

   Public packets keep runtime and promotion closed unless an explicit verified path exists.

4. Receipt-first verification

   Packet bytes, indexes, and mirrors are verified directly.

5. Adapter containment

   Hermes Agent, MCP, WebMCP, providers, dashboards, and third-party runtimes are adapters, not owners.

6. No JSON hot path

   JSON can exist only where external systems require it. It does not become the core truth format.

7. Asolaria compatibility

   The project aligns with BEHCS/HyperBEHCS lanes, packet receipts, operator gates, and future OS-on-metal governance boundaries.

Where Acer-style/mature memory versions may currently be ahead:

1. Finished UX

   They may already have dashboards, memory browsing, and one-command installation.

2. Live hooks

   They may already capture Claude/Cursor/Gemini/tool events automatically.

3. Search stack

   They may already include BM25, embeddings, vector stores, or knowledge graphs.

4. MCP server features

   They may already expose many MCP tools.

5. Team sharing

   They may already synchronize state across users or agents.

The correct conclusion:

```text
Acer-style memory systems may be more complete as applications today.
HyperBEHCS Hermes is stronger as the authority-safe packet substrate those applications should be gated by.
```

## Abilities model

HyperBEHCS Hermes treats abilities as packet-described capabilities that are inert until authority is proven.

Examples of ability classes:

```text
memory_read
memory_write
skill_read
skill_execute
tool_describe
tool_execute
mcp_describe
mcp_execute
webmcp_describe
webmcp_execute
provider_describe
provider_call
endpoint_describe
endpoint_publish
browser_observe
browser_control
file_read
file_write
shell_execute
device_read
device_write
usb_read
usb_write
private_surface_export
hidden_surface_export
restricted_surface_export
secret_surface_export
repo_publish
release_publish
```

The important distinction:

```text
describe != execute
observe != mutate
index != promote
remember != authorize
```

A future strict authority packet can say:

```text
ability=tool_execute|runtime=0|promote=0|status=DESCRIBED_ONLY
```

That means the tool exists semantically, but cannot run.

## Skills model

Skills are procedural knowledge. In many agent systems, a skill can become a direct path to action. HyperBEHCS Hermes treats skills as a gated class.

A skill may be:

```text
SKILL_OBSERVED
SKILL_INDEXED
SKILL_RECOMMENDED
SKILL_PLANNED
SKILL_AUTHORIZED
SKILL_EXECUTED
SKILL_RECEIPTED
SKILL_REVOKED
```

The public seed only supports the safe side of this model: packets can describe skill and adapter boundaries, while runtime authority stays closed.

Future skill packets should distinguish:

```text
skill_read=1       safe to read procedure
skill_plan=1       safe to include in plan
skill_execute=0    not allowed to execute yet
skill_mutate=0     not allowed to edit skill yet
promote=0          not promoted to runtime
```

## Tools model

Tools are authority surfaces. A shell tool, browser tool, file-write tool, GitHub tool, device tool, or provider tool can change the world.

HyperBEHCS Hermes therefore treats tools as two separate things:

1. Tool semantics

   What the tool is, what it can do, what input it expects, what output it returns.

2. Tool authority

   Whether this packet, agent, operator, or runtime is allowed to invoke it now.

This prevents a common failure mode:

```text
The agent knows a tool exists, therefore it uses it.
```

HyperBEHCS Hermes wants:

```text
The agent knows a tool exists, but the packet proves whether invocation is authorized.
```

## MCP and WebMCP model

MCP and WebMCP are powerful because they hydrate tools into an agent runtime. That also makes them dangerous if they are treated as plain convenience plumbing.

HyperBEHCS Hermes treats MCP/WebMCP as adapter surfaces.

MCP/WebMCP may be described by packets, but they do not become authority by existing.

Default public posture:

```text
mcp=0
webmcp=0
runtime=0
promote=0
endpoint=0
provider=0
```

Future live posture requires a promotion receipt chain.

Safe lifecycle:

```text
MCP_DESCRIBED -> MCP_INDEXED -> MCP_POLICY_CHECKED -> MCP_AUTHORIZED -> MCP_STARTED -> MCP_RECEIPTED
```

Unsafe lifecycle rejected:

```text
MCP_FOUND -> MCP_STARTED
```

WebMCP gets the same treatment, with extra caution around browser/network boundaries:

```text
webmcp_describe=1
webmcp_execute=0
browser_control=0
network_publish=0
secret_surface_export=0
```

## Memory model

HyperBEHCS Hermes can support the familiar memory tiers:

```text
working
 episodic
 semantic
 procedural
```

But it should not copy app-level forgetting blindly.

In a packet-first authority system, decay should affect retrieval priority, not canonical truth.

Recommended future model:

```text
working.hbp      hot context, short operational window
episodic.hbp     session/event receipts
semantic.hbp     distilled facts and relations
procedural.hbp   reusable procedures/skills
memory.hbi       packet index
memory.sha256    receipt
memory.hex       byte mirror
```

Decay policy:

```text
decay_rank may decrease
retrieval_priority may decrease
canonical receipt remains
operator-authorized delete/revoke required for removal
```

This is a major difference from systems that automatically evict stale memories. HyperBEHCS Hermes can rank stale memories lower without silently destroying canon.

## Authority fields

The current public verifier checks the v0.2 strict authority field set. Descriptor/read fields can be public; execution/write/control/export/release fields fail closed unless a matching promotion receipt exists.

```text
json
runtime
promote
endpoint
provider
mcp
usb_write
device_write
```

Additional strict fields include:

```text
dispatch
route
shell
tool
browser
keyboard
screenshot
network
webhook
cron
memory_write
skill_execute
provider_call
mcp_execute
webmcp_execute
file_write
private_surface_export
hidden_surface_export
restricted_surface_export
secret_surface_export
repo_publish
package_release
```

## Current packet example

```text
HBPv1|layer=example|pid=PID-HBH-EXAMPLE-KERNEL|prof=example_kernel_prof|supervisor=SUP-HYPERHERMES-OPERATOR|tuple=example:packet_kernel:standalone|triple_quant=packet/index/authority|polar_quant=standalone/runtime_denied|js_quant=example_tuple|turbo_quant=minimal_hot_path|json=0|runtime=0|promote=0|endpoint=0|provider=0|mcp=0|usb_write=0|device_write=0|status=EXAMPLE_FAIL_CLOSED
```

This row describes a packet kernel example. It does not grant runtime.

## CLI quick start

From this repository:

```text
python -m hyperbehcs_hermes.cli status examples/packet.hbp
python -m hyperbehcs_hermes.cli build-index examples/packet.hbp
python -m hyperbehcs_hermes.cli verify examples/packet.hbp
python -m unittest discover -s tests -v
```

Expected result:

```text
HYPERBEHCS_VERIFY_BEGIN
OK=true
ROWS=2
```

## Public preflight

Before publishing or recommending this repository:

```text
python -m unittest discover -s tests -v
python -m hyperbehcs_hermes.cli verify examples/packet.hbp
python -m hyperbehcs_hermes.cli verify examples/authority_surface.hbp
python -m hyperbehcs_hermes.cli verify-chain examples/authority_surface.hbp
python -m hyperbehcs_hermes.cli list-authority
python -m hyperbehcs_hermes.cli list-packs
for f in packs/*/*.hbp; do
  python -m hyperbehcs_hermes.cli verify "$f"
  python -m hyperbehcs_hermes.cli verify-chain "$f"
done
git ls-files '*.json'
```

Expected:

```text
tests pass
packet verifier OK=true
tracked JSON count is 0
```

GitHub Actions repeats these checks and fails if tracked JSON appears on the hot path.

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

## v0.2 strict-authority public surface

The repository now includes the public Asolaria/Acer ability surface as packet descriptors and tests.

Public descriptor artifacts:

```text
examples/authority_surface.hbp
examples/authority_surface.hbi
examples/authority_surface.sha256
examples/authority_surface.hex
```

Promotion receipt examples:

```text
examples/promotion_request.hbp
examples/promotion_approved.hbp
examples/promotion_revoked.hbp
```

Implementation modules:

```text
hyperbehcs_hermes/authority.py
hyperbehcs_hermes/chain.py
hyperbehcs_hermes/promotion.py
```

Tests:

```text
tests/test_authority_surface.py
tests/test_chain.py
tests/test_promotion.py
```

Docs:

```text
docs/ABILITY-SURFACE.md
docs/STRICT-AUTHORITY.md
docs/PUBLISH-THE-STUFF.md
docs/LOCAL-PROOF-CROSSWALK.md
docs/V0.2.1-HARDENING.md
docs/V0.2.2-DESCRIPTOR-EXPANSION.md
```

Public descriptor packs:

```text
packs/skills/public_skill_descriptors.hbp
packs/tools/public_tool_descriptors.hbp
packs/mcp/public_mcp_descriptors.hbp
packs/webmcp/public_webmcp_descriptors.hbp
packs/providers/public_provider_descriptors.hbp
packs/memory/public_memory_descriptors.hbp
packs/local/public_local_crosswalk_descriptors.hbp
packs/hermes/public_hermes_goal_descriptors.hbp
packs/browser/public_browser_descriptors.hbp
packs/endpoints/public_endpoint_descriptors.hbp
packs/proofs/public_proof_receipt_descriptors.hbp
```

This makes the difference visible to Asolaria and Acer:

- abilities are public descriptors;
- skills are separate read/execute authority surfaces;
- tools are separate describe/execute authority surfaces;
- MCP is separate describe/execute authority;
- WebMCP is separate describe/execute authority;
- providers are separate describe/call authority;
- browser observe is separate from browser control, screenshot capture, and keyboard control;
- endpoint describe is separate from endpoint open, network call, and webhook open;
- proof/receipt descriptors are separate from promotion authority;
- memory read is separate from memory write;
- device/USB/private/hidden/restricted/secret exports are explicit closed fields;
- append-only row chains can be verified;
- promotion receipts can be validated;
- opening an authority field without a matching approval fails tests.

The grammar is public and free. The execution authority remains receipt-gated.

## Current maturity label

This repository is currently:

```text
v0.2.2-descriptor-expansion: public strict-authority grammar, installable CLI, CI pack verification, local proof crosswalk seed, and expanded Hermes/browser/endpoint/proof descriptor packs
```

It is not yet:

```text
final strict authority-chain verifier
full memory server
live MCP/WebMCP runtime
provider gateway
agent OS
```

That is not a weakness. It is the correct public seed boundary.

## Recommended next milestone

Target:

```text
v0.3.0-public-proof-crosswalk
```

Minimum scope:

- Add promotion packet types.
- Add revoke and expire packet types.
- Add authority taxonomy fields.
- Add `prev_hash`, `row_hash`, `chain_id`, and `sequence` validation.
- Add append-only chain tests.
- Add cosign/quorum packet model.
- Add forbidden-combination tests.
- Add skill/tool/MCP/WebMCP authority tests.
- Add broader public-safety and history scans.
- Keep tracked JSON count at 0.

## Boundary statement for Acer / reviewers

Use this wording when sharing the repository:

```text
HyperBEHCS Hermes is a packet-first authority substrate, not just an agent memory app. It is different from normal memory systems because memory, tools, skills, MCP, WebMCP, providers, endpoints, and device surfaces are represented as packeted capability claims that remain fail-closed until separately authorized. The current public release is the CI-green seed kernel: parser, indexer, sidecar verifier, no-JSON hot path, and fail-closed gate detection. Future releases extend this into strict promotion/cosign/chain verification.
```

## Public-safe boundary

This repository is public-safe by design: packets may describe authority, but cannot exercise authority. Any bridge to Hermes Agent, Asolaria, MCP, WebMCP, providers, endpoints, devices, browsers, file systems, or private surfaces must remain an adapter with explicit gates and receipts.

## Final distinction

App-level memory says:

```text
Remember this for the agent.
```

HyperBEHCS Hermes says:

```text
Packet this claim, receipt it, index it, keep authority closed, and only promote through a verified boundary.
```

That is why it is different.
