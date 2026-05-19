# Hermes Agent Adapter

This adapter is optional.

Hermes Agent may read HyperBEHCS Hermes packets, run the verifier, summarize receipts, or schedule descriptor-only continuation jobs. The adapter must not make Hermes Agent the owner of packet truth.

Adapter boundary:
- no runtime grant by default
- no provider activation by default
- no MCP/WebMCP boot by default
- no endpoint publication by default
- no USB/device writes by default
- no raw private filesystem ingestion

Suggested Hermes skill trigger:

Use when working with HyperBEHCS Hermes packets, sidecars, receipts, or authority gates. Load the standalone repo verifier first; treat JSON as cold compatibility only.
