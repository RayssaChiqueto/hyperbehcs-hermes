# Authority Boundary

HyperBEHCS Hermes distinguishes semantic routing capacity from execution authority.

A packet can describe a capability without granting it. A verifier can prove a packet is well-formed without promoting it into runtime.

Closed-by-default fields:

```text
runtime=0
promote=0
endpoint=0
provider=0
mcp=0
usb_write=0
device_write=0
```

Opening any of these requires a separate operator-authorized receipt chain. This starter repo intentionally contains no such promotion path.
