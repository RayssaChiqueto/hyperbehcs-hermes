# Publishing HyperBEHCS Hermes

This repository is designed to be public-safe before it is pushed to GitHub.

## Target repository

Preferred remote:

```text
https://github.com/RayssaChiqueto/hyperbehcs-hermes.git
```

## Preflight

Run from the repository root:

```text
python -m unittest discover -s tests -v
python -m hyperbehcs_hermes.cli verify examples/packet.hbp
git status --short --branch
git ls-files '*.json'
git grep -nE 'USB\\VID_|GITHUB_TOKEN|BEGIN (RSA|OPENSSH|PRIVATE) KEY|password=' -- . ':!docs/PUBLISHING.md'
```

Expected:

```text
unit tests pass
packet verify returns OK=true
git status is clean before push
tracked JSON files = 0
public-safe needle scan returns no matches outside this document
```

## Create remote with GitHub web UI

1. Open `https://github.com/new` while signed in as `RayssaChiqueto`.
2. Repository name: `hyperbehcs-hermes`.
3. Description: `Packet-first HyperBEHCS Hermes control-plane kernel`.
4. Visibility: public, unless the operator explicitly chooses private.
5. Do not add README, .gitignore, or license in the GitHub UI; this local repo already has the source tree.
6. Create repository.

## Attach and push

```text
git remote add origin https://github.com/RayssaChiqueto/hyperbehcs-hermes.git
git push -u origin main
git push origin v0.1.0-local
```

If `origin` already exists, verify it first:

```text
git remote -v
git remote set-url origin https://github.com/RayssaChiqueto/hyperbehcs-hermes.git
```

## Authority boundary

Publishing this repository does not activate runtime authority, providers, MCP/WebMCP, endpoints, USB/device writes, or private filesystem scans. GitHub is a source distribution surface only.
