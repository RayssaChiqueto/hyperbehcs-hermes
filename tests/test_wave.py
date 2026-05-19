import unittest
from pathlib import Path

from hyperbehcs_hermes.chain import verify_append_only_chain
from hyperbehcs_hermes.packet import parse_packet_text
from hyperbehcs_hermes.verifier import verify_packet
from hyperbehcs_hermes.wave import validate_spindle_wave
from hyperbehcs_hermes.wave_templates import mcp_webmcp_wave_text

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "packs" / "waves" / "public_spindle_wave_mcp_webmcp.hbp"


class WaveTests(unittest.TestCase):
    def rows(self):
        return parse_packet_text(mcp_webmcp_wave_text())

    def test_valid_wave_has_one_main_and_exactly_three_subagents_per_spindle(self):
        result = validate_spindle_wave(self.rows())
        self.assertTrue(result.ok, result.errors)
        self.assertEqual(result.spindles, 5)

    def test_wave_rejects_missing_main(self):
        rows = [row for row in self.rows() if not (row.fields["spindle_id"] == "SPINDLE-MCP-CORE" and row.fields["agent_slot"] == "main")]
        result = validate_spindle_wave(rows)
        self.assertFalse(result.ok)
        self.assertTrue(any("expected 1 main got 0" in error for error in result.errors))

    def test_wave_rejects_duplicate_main(self):
        rows = self.rows()
        rows.append(rows[0])
        result = validate_spindle_wave(rows)
        self.assertFalse(result.ok)
        self.assertTrue(any("expected 1 main got 2" in error for error in result.errors))

    def test_wave_rejects_missing_subagent(self):
        rows = [row for row in self.rows() if not (row.fields["spindle_id"] == "SPINDLE-MCP-CORE" and row.fields["agent_slot"] == "subagent-3")]
        result = validate_spindle_wave(rows)
        self.assertFalse(result.ok)
        self.assertTrue(any("expected 3 subagents got 2" in error for error in result.errors))

    def test_wave_rejects_open_execution_fields(self):
        for field in ("dispatch", "route", "runtime", "file_write", "tool_execute", "mcp_execute", "webmcp_execute", "provider_call"):
            with self.subTest(field=field):
                text = mcp_webmcp_wave_text().replace(f"{field}=0", f"{field}=1", 1)
                result = validate_spindle_wave(parse_packet_text(text))
                self.assertFalse(result.ok)
                self.assertTrue(any(field in error for error in result.errors), result.errors)

    def test_wave_rejects_json_hot_path(self):
        text = mcp_webmcp_wave_text().replace("json=0", "json=1", 1)
        result = validate_spindle_wave(parse_packet_text(text))
        self.assertFalse(result.ok)
        self.assertTrue(any("json hot path" in error for error in result.errors))

    def test_wave_rejects_missing_required_wave_fields(self):
        for field in ("input_packet", "output_receipt", "depends_on", "acceptance", "mcp_scope", "webmcp_scope"):
            with self.subTest(field=field):
                text = mcp_webmcp_wave_text().replace(f"|{field}=", "|removed_field=", 1)
                result = validate_spindle_wave(parse_packet_text(text))
                self.assertFalse(result.ok)
                self.assertTrue(any(field in error for error in result.errors), result.errors)

    def test_wave_rejects_non_describe_scopes_and_wrong_layer(self):
        text = mcp_webmcp_wave_text().replace("mcp_scope=describe_only", "mcp_scope=execute", 1)
        result = validate_spindle_wave(parse_packet_text(text))
        self.assertFalse(result.ok)
        self.assertTrue(any("mcp_scope" in error for error in result.errors))
        text = mcp_webmcp_wave_text().replace("webmcp_scope=describe_only", "webmcp_scope=execute", 1)
        result = validate_spindle_wave(parse_packet_text(text))
        self.assertFalse(result.ok)
        self.assertTrue(any("webmcp_scope" in error for error in result.errors))
        text = mcp_webmcp_wave_text().replace("layer=spindle-wave", "layer=other", 1)
        result = validate_spindle_wave(parse_packet_text(text))
        self.assertFalse(result.ok)
        self.assertTrue(any("layer" in error for error in result.errors))

    def test_wave_rejects_missing_closed_authority_field(self):
        text = mcp_webmcp_wave_text().replace("|tool_execute=0", "", 1)
        result = validate_spindle_wave(parse_packet_text(text))
        self.assertFalse(result.ok)
        self.assertTrue(any("tool_execute" in error for error in result.errors))

    def test_duplicate_packet_fields_fail_parse(self):
        first = mcp_webmcp_wave_text().splitlines()[0] + "|json=0\n"
        with self.assertRaises(ValueError):
            parse_packet_text(first)

    def test_public_pack_verifies_packet_chain_and_wave(self):
        self.assertTrue(verify_packet(PACK).ok)
        rows = parse_packet_text(PACK.read_text(encoding="utf-8"))
        self.assertTrue(verify_append_only_chain(rows).ok)
        self.assertTrue(validate_spindle_wave(rows).ok)


if __name__ == "__main__":
    unittest.main()
