from __future__ import annotations

import argparse
from pathlib import Path
from .authority import describe_authority_surface
from .indexer import build_index
from .packet import read_packet, sha256_bytes
from .verifier import verify_packet, write_sidecars
from .chain import verify_append_only_chain
from .promotion import verify_promotions
from .wave import validate_spindle_wave
from .wave_templates import mcp_webmcp_wave_text


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


def cmd_verify_chain(args: argparse.Namespace) -> int:
    rows = read_packet(args.packet)
    result = verify_append_only_chain(rows, strict=True)
    print("HYPERBEHCS_CHAIN_VERIFY_BEGIN")
    print(f"OK={str(result.ok).lower()}")
    print(f"ROWS={len(rows)}")
    for error in result.errors:
        print(f"ERROR={error}")
    return 0 if result.ok else 1


def cmd_verify_promotions(args: argparse.Namespace) -> int:
    rows = read_packet(args.packet)
    result = verify_promotions(rows)
    print("HYPERBEHCS_PROMOTION_VERIFY_BEGIN")
    print(f"OK={str(result.ok).lower()}")
    print(f"ROWS={len(rows)}")
    for error in result.errors:
        print(f"ERROR={error}")
    return 0 if result.ok else 1


def cmd_list_authority(args: argparse.Namespace) -> int:
    print("HYPERBEHCS_AUTHORITY_SURFACE_BEGIN")
    for item in describe_authority_surface():
        print("|".join([item.name, item.category, item.field, f"default={item.default}", item.description]))
    return 0


def cmd_list_packs(args: argparse.Namespace) -> int:
    root = Path(args.root)
    print("HYPERBEHCS_PUBLIC_PACKS_BEGIN")
    for path in sorted(root.glob("packs/*/*.hbp")):
        print(path.as_posix())
    return 0



def cmd_wave_verify(args: argparse.Namespace) -> int:
    rows = read_packet(args.packet)
    result = validate_spindle_wave(rows, require_closed=True)
    print("\n".join(result.receipt_lines()))
    return 0 if result.ok else 1


def cmd_wave_template(args: argparse.Namespace) -> int:
    if args.template != "mcp-webmcp":
        raise ValueError(f"unsupported wave template: {args.template}")
    text = mcp_webmcp_wave_text(wave_id=args.wave_id)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8", newline="\n")
        print("HYPERBEHCS_WAVE_TEMPLATE_WRITE=PASS")
        print(f"PACKET={args.out}")
    else:
        print(text, end="")
    return 0


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
    chain = sub.add_parser("verify-chain")
    chain.add_argument("packet")
    chain.set_defaults(func=cmd_verify_chain)
    promotions = sub.add_parser("verify-promotions")
    promotions.add_argument("packet")
    promotions.set_defaults(func=cmd_verify_promotions)
    authority = sub.add_parser("list-authority")
    authority.set_defaults(func=cmd_list_authority)
    packs = sub.add_parser("list-packs")
    packs.add_argument("--root", default=".")
    packs.set_defaults(func=cmd_list_packs)
    wave = sub.add_parser("wave")
    wave_sub = wave.add_subparsers(dest="wave_command", required=True)
    wave_verify = wave_sub.add_parser("verify")
    wave_verify.add_argument("packet")
    wave_verify.set_defaults(func=cmd_wave_verify)
    wave_template = wave_sub.add_parser("template")
    wave_template.add_argument("template", choices=["mcp-webmcp"])
    wave_template.add_argument("--wave-id", default="WAVE-MCP-WEBMCP-v1")
    wave_template.add_argument("--out")
    wave_template.set_defaults(func=cmd_wave_template)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)

if __name__ == "__main__":
    raise SystemExit(main())

