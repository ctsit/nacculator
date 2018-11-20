import unittest

from nacc.uds3 import packet as ivp_packet
from nacc.uds3.ivp import builder


class TestCLS(unittest.TestCase):

    def test_cls_blank_not_added_to_ivp(self):
        """Don't add blank CLS form to IVP."""
        packet = ivp_packet.Packet()
        record = make_record()

        builder.add_cls(record, packet)
        self.assertEqual(len(packet), 0)

    def test_cls_not_added_if_not_hispanic(self):
        """
        Do not add Form CLS if the subject is not Hispanic/Latino.

        https://www.alz.washington.edu/NONMEMBER/UDS/DOCS/VER3/CLS/CLS_en.pdf
        """
        packet = ivp_packet.Packet()
        record = make_record()
        record['hispanic'] = '0'  # Subject is not Hispanic/Latino.

        builder.add_cls(record, packet)
        self.assertEqual(len(packet), 0)


def make_record():
    return {
        'eng_preferred_language': '',
        'eng_years_speak_spanish': '',
        'eng_years_speak_english': '',
        'eng_percentage_spanish': '',
        'eng_percentage_english': '',
        'eng_proficiency_spanish': '',
        'eng_proficiency_read_spanish': '',
        'eng_proficiency_write_spanish': '',
        'eng_proficiency_oral_spanish': '',
        'eng_proficiency_speak_english': '',
        'eng_proficiency_read_english': '',
        'eng_proficiency_write_english': '',
        'eng_proficiency_oral_english': '',
        'clslang': '0',   # This is from Form Z1X
        'hispanic': '1',  # This is from Form A1
    }


if __name__ == "__main__":
    unittest.main()
