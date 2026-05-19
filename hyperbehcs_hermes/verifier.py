from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from .indexer import build_hbi_rows
from .packet import parse_packet_text, sha256_bytes

@dataclass
class VerificationResult:
    ok: bool
    rows: int
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def receipt_lines(self) -> list[str]:
        lines = [
            "HYPERBEHCS_VERIFY_BEGIN",
            f"OK={str(self.ok).lower()}",
            f"ROWS={self.rows}",
        ]
        lines.extend(f"ERROR={error}" for error in self.errors)
        lines.extend(f"WARNING={warning}" for warning in self.warnings)
        return lines


def verify_packet(packet_path: str | Path, require_closed: bool = True) -> VerificationResult:
    packet_path = Path(packet_path)
    errors: list[str] = []
    warnings: list[str] = []
    if packet_path.suffix != ".hbp":
        errors.append("packet path must end with .hbp")
    if not packet_path.exists():
        return VerificationResult(False, 0, [f"missing packet: {packet_path}"], warnings)

    raw = packet_path.read_bytes()
    text = raw.decode("utf-8")
    try:
        rows = parse_packet_text(text)
    except Exception as exc:
        return VerificationResult(False, 0, [f"parse failed: {exc}"], warnings)

    for idx, row in enumerate(rows, 1):
        missing = row.missing_required()
        if missing:
            errors.append(f"row {idx} missing required fields: {','.join(missing)}")
        if row.fields.get("json") != "0":
            errors.append(f"row {idx} json hot path is not closed")
        if require_closed:
            opened = row.open_authority_fields()
            if opened:
                errors.append(f"row {idx} opens authority fields: {opened}")

    hbi_path = packet_path.with_suffix(".hbi")
    if hbi_path.exists():
        expected = "\n".join(build_hbi_rows(rows)) + "\n"
        actual = hbi_path.read_text(encoding="utf-8")
        if actual != expected:
            errors.append("hbi sidecar mismatch")
    else:
        warnings.append("hbi sidecar missing")

    sha_path = packet_path.with_suffix(".sha256")
    digest = sha256_bytes(raw)
    if sha_path.exists():
        actual_digest = sha_path.read_text(encoding="utf-8").split()[0]
        if actual_digest != digest:
            errors.append("sha256 sidecar mismatch")
    else:
        warnings.append("sha256 sidecar missing")

    hex_path = packet_path.with_suffix(".hex")
    if hex_path.exists():
        if hex_path.read_text(encoding="ascii").strip() != raw.hex():
            errors.append("hex sidecar mismatch")
    else:
        warnings.append("hex sidecar missing")

    return VerificationResult(not errors, len(rows), errors, warnings)


def write_sidecars(packet_path: str | Path) -> None:
    packet_path = Path(packet_path)
    rows = parse_packet_text(packet_path.read_text(encoding="utf-8"))
    packet_path.with_suffix(".hbi").write_text("\n".join(build_hbi_rows(rows)) + "\n", encoding="utf-8", newline="\n")
    raw = packet_path.read_bytes()
    packet_path.with_suffix(".sha256").write_text(f"{sha256_bytes(raw)}  {packet_path.name}\n", encoding="utf-8", newline="\n")
    packet_path.with_suffix(".hex").write_text(raw.hex() + "\n", encoding="ascii", newline="\n")
