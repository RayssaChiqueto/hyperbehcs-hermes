import unittest
from hyperbehcs_hermes.packet import parse_packet_text
from hyperbehcs_hermes.promotion import verify_promotions

BASE = "HBPv1|layer=authority|prof=p|supervisor=s|tuple=t|triple_quant=a/b/c|polar_quant=a/b|js_quant=j|turbo_quant=t|json=0|runtime=0|promote=0|endpoint=0|provider=0|mcp=0|usb_write=0|device_write=0"


class PromotionTests(unittest.TestCase):
    def test_open_authority_without_promotion_fails(self):
        packet = BASE + "|pid=PID-ABILITY|status=AUTHORITY_DESCRIBED|tool_execute=1\n"
        result = verify_promotions(parse_packet_text(packet))
        self.assertFalse(result.ok)
        self.assertTrue(any("without approved promotion" in error for error in result.errors))

    def test_matching_approved_promotion_allows_scoped_field(self):
        packet = "\n".join([
            BASE + "|pid=PID-ABILITY|status=AUTHORITY_DESCRIBED|tool_execute=1|chain_id=C1|sequence=1|prev_hash=ROOT",
            BASE + "|pid=PID-PROMO|status=PROMOTION_APPROVED|promotion_target=PID-ABILITY|promotion_field=tool_execute|promotion_scope=public-descriptor|promotion_expires=never|promotion_revoked=0|chain_id=C1|sequence=2|prev_hash=AUTO",
        ]) + "\n"
        result = verify_promotions(parse_packet_text(packet))
        self.assertTrue(result.ok, result.errors)

    def test_wrong_field_promotion_fails(self):
        packet = "\n".join([
            BASE + "|pid=PID-ABILITY|status=AUTHORITY_DESCRIBED|skill_execute=1",
            BASE + "|pid=PID-PROMO|status=PROMOTION_APPROVED|promotion_target=PID-ABILITY|promotion_field=tool_execute|promotion_scope=public-descriptor|promotion_expires=never|promotion_revoked=0",
        ]) + "\n"
        result = verify_promotions(parse_packet_text(packet))
        self.assertFalse(result.ok)
        self.assertTrue(any("skill_execute" in error for error in result.errors))

    def test_revoked_promotion_fails(self):
        packet = "\n".join([
            BASE + "|pid=PID-ABILITY|status=AUTHORITY_DESCRIBED|mcp_execute=1",
            BASE + "|pid=PID-PROMO|status=PROMOTION_APPROVED|promotion_target=PID-ABILITY|promotion_field=mcp_execute|promotion_scope=public-descriptor|promotion_expires=never|promotion_revoked=1",
        ]) + "\n"
        result = verify_promotions(parse_packet_text(packet))
        self.assertFalse(result.ok)
        self.assertTrue(any("revoked" in error for error in result.errors))


if __name__ == "__main__":
    unittest.main()
