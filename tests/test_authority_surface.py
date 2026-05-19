import unittest
from pathlib import Path

from hyperbehcs_hermes.authority import (
    AUTHORITY_FIELDS,
    DESCRIPTOR_STATUS,
    EXECUTION_FIELDS,
    describe_authority_surface,
)
from hyperbehcs_hermes.packet import parse_packet_text
from hyperbehcs_hermes.verifier import verify_packet

ROOT = Path(__file__).resolve().parents[1]
SURFACE = ROOT / "examples" / "authority_surface.hbp"


class AuthoritySurfaceTests(unittest.TestCase):
    def test_public_surface_contains_mcp_webmcp_tools_skills_and_providers(self):
        names = {item.name for item in describe_authority_surface()}
        for required in [
            "mcp_execute",
            "webmcp_execute",
            "tool_execute",
            "skill_execute",
            "provider_call",
            "browser_control",
            "memory_write",
            "secret_surface_export",
        ]:
            self.assertIn(required, names)

    def test_execution_fields_are_fail_closed_by_default(self):
        rows = parse_packet_text(SURFACE.read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(rows), 12)
        for row in rows:
            self.assertIn(row.fields["status"], DESCRIPTOR_STATUS)
            for field in EXECUTION_FIELDS:
                self.assertEqual(row.fields.get(field, "0"), "0", f"{row.pid} opened {field}")

    def test_authority_surface_example_verifies(self):
        result = verify_packet(SURFACE)
        self.assertTrue(result.ok, result.errors)

    def test_open_tool_skill_mcp_webmcp_provider_fields_fail_without_promotion(self):
        for field in ["tool_execute", "skill_execute", "mcp_execute", "webmcp_execute", "provider_call"]:
            packet = (
                "HBPv1|layer=test|pid=PID-OPEN|prof=p|supervisor=s|tuple=t|"
                "triple_quant=a/b/c|polar_quant=a/b|js_quant=j|turbo_quant=t|"
                f"json=0|runtime=0|promote=0|endpoint=0|provider=0|mcp=0|usb_write=0|device_write=0|{field}=1|status=OPEN\n"
            )
            row = parse_packet_text(packet)[0]
            opened = row.open_authority_fields()
            self.assertIn(field, opened)


if __name__ == "__main__":
    unittest.main()
