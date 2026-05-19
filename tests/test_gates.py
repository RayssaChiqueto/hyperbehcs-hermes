import unittest
from hyperbehcs_hermes.gates import authority_posture
from hyperbehcs_hermes.packet import parse_packet_text

class GateTests(unittest.TestCase):
    def test_fail_closed_posture(self):
        row = parse_packet_text("HBPv1|layer=x|pid=PID-X|prof=p|supervisor=s|tuple=t|triple_quant=a/b/c|polar_quant=a/b|js_quant=j|turbo_quant=t|json=0|runtime=0|promote=0|endpoint=0|provider=0|mcp=0|usb_write=0|device_write=0|status=OK\n")[0]
        self.assertEqual(authority_posture(row), "FAIL_CLOSED")

    def test_open_runtime_detected(self):
        row = parse_packet_text("HBPv1|layer=x|pid=PID-X|prof=p|supervisor=s|tuple=t|triple_quant=a/b/c|polar_quant=a/b|js_quant=j|turbo_quant=t|json=0|runtime=1|promote=0|endpoint=0|provider=0|mcp=0|usb_write=0|device_write=0|status=OPEN\n")[0]
        self.assertIn("runtime=1", authority_posture(row))

if __name__ == "__main__":
    unittest.main()
