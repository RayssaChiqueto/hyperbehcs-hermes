from __future__ import annotations

from dataclasses import dataclass, field
import hashlib

from .packet import PacketRow


@dataclass
class ChainResult:
    ok: bool
    errors: list[str] = field(default_factory=list)


def canonical_row_text(row: PacketRow) -> str:
    parts = ["HBPv1"]
    for key, value in row.fields.items():
        if key == "row_hash":
            continue
        parts.append(f"{key}={value}")
    return "|".join(parts)


def chain_row_hash(row: PacketRow) -> str:
    return hashlib.sha256((canonical_row_text(row) + "\n").encode("utf-8")).hexdigest()


def verify_append_only_chain(rows: list[PacketRow], strict: bool = True) -> ChainResult:
    errors: list[str] = []
    if not rows:
        return ChainResult(False, ["empty chain"])

    seen_sequences: set[tuple[str, int]] = set()
    previous_hash_by_chain: dict[str, str] = {}
    previous_sequence_by_chain: dict[str, int] = {}

    for idx, row in enumerate(rows, 1):
        chain_id = row.fields.get("chain_id")
        sequence_text = row.fields.get("sequence")
        prev_hash = row.fields.get("prev_hash")
        if not chain_id or not sequence_text or not prev_hash:
            if strict:
                errors.append(f"row {idx} missing chain_id/sequence/prev_hash")
            continue
        try:
            sequence = int(sequence_text)
        except ValueError:
            errors.append(f"row {idx} sequence is not an integer")
            continue
        key = (chain_id, sequence)
        if key in seen_sequences:
            errors.append(f"row {idx} duplicate sequence {sequence} in chain {chain_id}")
        seen_sequences.add(key)

        if chain_id not in previous_hash_by_chain:
            if sequence != 1:
                errors.append(f"row {idx} first sequence for chain {chain_id} must be 1")
            if prev_hash != "ROOT":
                errors.append(f"row {idx} chain root prev_hash must be ROOT")
        else:
            expected_sequence = previous_sequence_by_chain[chain_id] + 1
            if sequence != expected_sequence:
                errors.append(f"row {idx} sequence {sequence} expected {expected_sequence} in chain {chain_id}")
            expected_prev = previous_hash_by_chain[chain_id]
            if prev_hash != expected_prev:
                errors.append(f"row {idx} prev_hash mismatch: expected {expected_prev} got {prev_hash}")

        actual_hash = chain_row_hash(row)
        declared_hash = row.fields.get("row_hash")
        if declared_hash and declared_hash != actual_hash:
            errors.append(f"row {idx} row_hash mismatch")
        previous_hash_by_chain[chain_id] = actual_hash
        previous_sequence_by_chain[chain_id] = sequence

    return ChainResult(not errors, errors)
