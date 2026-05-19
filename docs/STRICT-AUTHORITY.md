# Strict Authority Verification

HyperBEHCS Hermes v0.2 strict-authority work adds public verifier machinery for three things:

1. expanded authority fields;
2. append-only packet chains;
3. promotion receipts.

## Expanded authority fields

The verifier recognizes a larger authority surface than the v0.1 bootstrap gates.

Starter/legacy fields:

```text
json runtime promote endpoint provider mcp usb_write device_write
```

Strict authority fields:

```text
dispatch route shell terminal file_write memory_write
tool_execute skill_execute mcp_execute webmcp_execute
provider_call endpoint_open browser_control keyboard_control
screenshot_capture network_call webhook_open cron_create
device_read device_write usb_read usb_write
private_surface_export hidden_surface_export restricted_surface_export secret_surface_export
repo_publish package_release
```

A nonzero value in these fields is treated as opened authority.

## Append-only chain

Rows can carry:

```text
chain_id=<public chain id>
sequence=<integer>
prev_hash=<ROOT or previous canonical row hash>
```

The chain verifier fails when:

- sequence is missing in strict mode;
- chain_id is missing in strict mode;
- prev_hash is missing in strict mode;
- first row does not use prev_hash=ROOT;
- sequence numbers skip or duplicate;
- prev_hash does not equal the previous row hash for that chain;
- declared row_hash exists but does not match canonical row hash.

## Promotion receipts

A row may request, approve, deny, revoke, or expire authority using statuses:

```text
PROMOTION_REQUESTED
PROMOTION_APPROVED
PROMOTION_DENIED
PROMOTION_REVOKED
PROMOTION_EXPIRED
```

A promotion approval carries:

```text
promotion_target=<pid>
promotion_field=<authority field>
promotion_scope=<scope>
promotion_expires=<never or ISO timestamp>
promotion_revoked=0
```

The promotion verifier fails when an authority field opens without a matching, unexpired, non-revoked approval for the exact packet pid and field.

## Current safety boundary

This release exports the public grammar and tests. It does not open live tools, MCP, WebMCP, providers, endpoints, shell, browser control, devices, USB, private exports, or package release.

That is the point: Asolaria and Acer can inspect the ability surface without receiving uncontrolled runtime authority.
