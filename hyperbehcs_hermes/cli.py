from __future__ import annotations

import argparse
from pathlib import Path
from .indexer import build_index
from .packet import read_packet, sha256_bytes
from .verifier import verify_packet, write_sidecars


def cmd_status(args: argparse.Namespace) -> int:
    path = Path(args.packet)
    rows = read_packet(path)
    print("HYPERBEHCS_STATUS_BEGIN")
    print(f"PACKET={path}")
    print(f"ROWS={len(rows)}")
    print(f"SHA256={sha256_bytes(path.read_bytes())}")
    print("AUTHORITY_DEFAULT=runtime0 promote0 endpoint0 provider0 mcp0 usb_write0 device_write0")
    return 0


def cmd_build_index(args: argparse.Namespace) -> int:
    index = build_index(args.packet, write=True)
    print("HYPERBEHCS_INDEX_WRITE=PASS")
    print(f"HBI={index}")
    return 0


def cmd_sidecars(args: argparse.Namespace) -> int:
    write_sidecars(args.packet)
    print("HYPERBEHCS_SIDECARS_WRITE=PASS")
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    result = verify_packet(args.packet, require_closed=not args.allow_open)
    print("\n".join(result.receipt_lines()))
    return 0 if result.ok else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="hyperbehcs-hermes")
    sub = parser.add_subparsers(dest="command", required=True)
    status = sub.add_parser("status")
    status.add_argument("packet")
    status.set_defaults(func=cmd_status)
    index = sub.add_parser("build-index")
    index.add_argument("packet")
    index.set_defaults(func=cmd_build_index)
    sidecars = sub.add_parser("write-sidecars")
    sidecars.add_argument("packet")
    sidecars.set_defaults(func=cmd_sidecars)
    verify = sub.add_parser("verify")
    verify.add_argument("packet")
    verify.add_argument("--allow-open", action="store_true")
    verify.set_defaults(func=cmd_verify)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)

if __name__ == "__main__":
    raise SystemExit(main())
