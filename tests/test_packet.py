import unittest
from pathlib import Path
from hyperbehcs_hermes.packet import parse_packet_text
from hyperbehcs_hermes.verifier import verify_packet, write_sidecars

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "packet.hbp"

class PacketTests(unittest.TestCase):
    def test_parse_example_rows(self):
        rows = parse_packet_text(EXAMPLE.read_text(encoding="utf-8"))
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0].fields["json"], "0")
        self.assertEqual(rows[0].fields["runtime"], "0")

    def test_missing_required_fails(self):
        row = parse_packet_text("HBPv1|pid=PID-X|json=0|runtime=0|promote=0\n")[0]
        self.assertIn("layer", row.missing_required())

    def test_sidecars_and_verify(self):
        write_sidecars(EXAMPLE)
        result = verify_packet(EXAMPLE)
        self.assertTrue(result.ok, result.errors)
        self.assertEqual(result.rows, 2)

if __name__ == "__main__":
    unittest.main()
