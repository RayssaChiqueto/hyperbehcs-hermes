from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import hashlib
from .authority import AUTHORITY_FIELDS

REQUIRED_FIELDS = (
    "layer",
    "pid",
    "prof",
    "supervisor",
    "tuple",
    "triple_quant",
    "polar_quant",
    "js_quant",
    "turbo_quant",
    "json",
    "runtime",
    "promote",
    "status",
)

DEFAULT_CLOSED_FIELDS = AUTHORITY_FIELDS

@dataclass(frozen=True)
class PacketRow:
    raw: str
    fields: dict[str, str]

    @property
    def pid(self) -> str:
        return self.fields.get("pid", "")

    def missing_required(self) -> list[str]:
        return [key for key in REQUIRED_FIELDS if key not in self.fields]

    def open_authority_fields(self) -> dict[str, str]:
        opened: dict[str, str] = {}
        for key in DEFAULT_CLOSED_FIELDS:
            value = self.fields.get(key)
            if value is not None and value != "0":
                opened[key] = value
        return opened


def parse_row(line: str) -> PacketRow:
    line = line.strip()
    if not line:
        raise ValueError("empty packet row")
    parts = line.split("|")
    if parts[0] != "HBPv1":
        raise ValueError(f"unsupported packet row prefix: {parts[0]!r}")
    fields: dict[str, str] = {}
    for part in parts[1:]:
        if "=" not in part:
            raise ValueError(f"packet field lacks '=': {part!r}")
        key, value = part.split("=", 1)
        if not key:
            raise ValueError("packet field has empty key")
        if key in fields:
            raise ValueError(f"duplicate packet field: {key}")
        fields[key] = value
    return PacketRow(raw=line, fields=fields)


def parse_packet_text(text: str) -> list[PacketRow]:
    return [parse_row(line) for line in text.splitlines() if line.strip()]


def read_packet(path: str | Path) -> list[PacketRow]:
    return parse_packet_text(Path(path).read_text(encoding="utf-8"))


def packet_bytes(path: str | Path) -> bytes:
    return Path(path).read_bytes()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def row_sha256(row: PacketRow) -> str:
    return sha256_bytes((row.raw + "\n").encode("utf-8"))
