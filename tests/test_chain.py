import unittest
from pathlib import Path

from hyperbehcs_hermes.chain import verify_append_only_chain
from hyperbehcs_hermes.packet import parse_packet_text

ROOT = Path(__file__).resolve().parents[1]
SURFACE = ROOT / "examples" / "authority_surface.hbp"


class ChainTests(unittest.TestCase):
    def test_authority_surface_has_valid_append_only_chain(self):
        rows = parse_packet_text(SURFACE.read_text(encoding="utf-8"))
        result = verify_append_only_chain(rows)
        self.assertTrue(result.ok, result.errors)

    def test_wrong_previous_hash_fails(self):
        packet = "\n".join([
            "HBPv1|layer=chain|pid=PID-1|prof=p|supervisor=s|tuple=t|triple_quant=a/b/c|polar_quant=a/b|js_quant=j|turbo_quant=t|json=0|runtime=0|promote=0|status=CHAIN_ROOT|chain_id=C1|sequence=1|prev_hash=ROOT",
            "HBPv1|layer=chain|pid=PID-2|prof=p|supervisor=s|tuple=t|triple_quant=a/b/c|polar_quant=a/b|js_quant=j|turbo_quant=t|json=0|runtime=0|promote=0|status=CHAIN_LINK|chain_id=C1|sequence=2|prev_hash=BAD",
        ]) + "\n"
        result = verify_append_only_chain(parse_packet_text(packet))
        self.assertFalse(result.ok)
        self.assertTrue(any("prev_hash" in error for error in result.errors))

    def test_duplicate_sequence_fails(self):
        packet = "\n".join([
            "HBPv1|layer=chain|pid=PID-1|prof=p|supervisor=s|tuple=t|triple_quant=a/b/c|polar_quant=a/b|js_quant=j|turbo_quant=t|json=0|runtime=0|promote=0|status=CHAIN_ROOT|chain_id=C1|sequence=1|prev_hash=ROOT",
            "HBPv1|layer=chain|pid=PID-2|prof=p|supervisor=s|tuple=t|triple_quant=a/b/c|polar_quant=a/b|js_quant=j|turbo_quant=t|json=0|runtime=0|promote=0|status=CHAIN_LINK|chain_id=C1|sequence=1|prev_hash=BAD",
        ]) + "\n"
        result = verify_append_only_chain(parse_packet_text(packet))
        self.assertFalse(result.ok)
        self.assertTrue(any("sequence" in error for error in result.errors))


if __name__ == "__main__":
    unittest.main()
