from __future__ import annotations

from pathlib import Path
from .packet import PacketRow, read_packet, row_sha256


def build_hbi_rows(rows: list[PacketRow]) -> list[str]:
    output: list[str] = []
    for idx, row in enumerate(rows, 1):
        byte_count = len((row.raw + "\n").encode("utf-8"))
        output.append(
            "|".join(
                [
                    "HBIv1",
                    f"row={idx}",
                    f"pid={row.pid}",
                    f"bytes={byte_count}",
                    f"sha256={row_sha256(row)}",
                    "json=0",
                    "runtime=0",
                    "promote=0",
                ]
            )
        )
    return output


def build_index(packet_path: str | Path, write: bool = True) -> Path:
    packet_path = Path(packet_path)
    rows = read_packet(packet_path)
    index_path = packet_path.with_suffix(".hbi")
    text = "\n".join(build_hbi_rows(rows)) + "\n"
    if write:
        index_path.write_text(text, encoding="utf-8", newline="\n")
    return index_path
