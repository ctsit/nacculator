import unittest

from nacc.uds3 import packet as ivp_packet
from nacc.uds3.ivp import builder


class TestCLS(unittest.TestCase):

    def test_cls_blank_not_added_to_ivp(self):
        """Don't add blank CLS form to IVP."""
        packet = ivp_packet.Packet()
        record = make_blank_record()
        record['hispanic'] = '1'  # Subject is Hispanic/Latino.

        builder.add_cls(record, packet)
        self.assertEqual(len(packet), 0, "Expected packet to be empty")

    def test_cls_not_added_if_not_hispanic(self):
        """
        Do not add Form CLS if the subject is not Hispanic/Latino.

        https://www.alz.washington.edu/NONMEMBER/UDS/DOCS/VER3/CLS/CLS_en.pdf
        """
        packet = ivp_packet.Packet()
        record = make_blank_record()
        record['hispanic'] = '0'  # Subject is not Hispanic/Latino.

        builder.add_cls(record, packet)
        self.assertEqual(len(packet), 0, "Expected packet to be empty")

    def test_cls_added_when_filled(self):
        """Add filled CLS form to IVP."""
        packet = ivp_packet.Packet()
        record = make_filled_record()

        builder.add_cls(record, packet)
        self.assertEqual(len(packet), 1, "Expected packet to have CLS")

    def test_partial_cls_raises_error(self):
        """Partially completed CLS should raise an exception."""
        packet = ivp_packet.Packet()
        record = make_filled_record()
        record['eng_preferred_language'] = ' '  # Make form partially complete.

        with self.assertRaises(Exception):
            builder.add_cls(record, packet)

    def test_cls_proficiency_must_be_100(self):
        """Language proficiency percentages must sum to 100."""
        packet = ivp_packet.Packet()
        record = make_filled_record()
        record['eng_percentage_english'] = '20'
        record['eng_percentage_spanish'] = '9001'

        with self.assertRaises(Exception):
            builder.add_cls(record, packet)

    def test_check_cls_date(self):
        """
        Having a CLS with a visit date before June 1, 2017 raises an exception.
        """
        packet = ivp_packet.Packet()
        record = make_filled_record()
        record['visityr'] = '2016'

        with self.assertRaises(Exception):
            builder.add_cls(record, packet)

    def test_cls_form_marked_complete(self):
        """If the completed CLS form is not marked complete, raise."""
        packet = ivp_packet.Packet()
        record = make_filled_record()
        record['form_cls_linguistic_history_of_subject_complete'] = '0 or 1'

        with self.assertRaises(Exception):
            builder.add_cls(record, packet)


def make_blank_record():
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
        'hispanic': '',  # This is from Form A1
        'visityr': '',
        'visitmo': '',
        'form_cls_linguistic_history_of_subject_complete': '',
    }


def make_filled_record():
    return {
        'eng_preferred_language': '1',
        'eng_years_speak_spanish': '1',
        'eng_years_speak_english': '1',
        'eng_percentage_spanish': '50',
        'eng_percentage_english': '50',
        'eng_proficiency_spanish': '1',
        'eng_proficiency_read_spanish': '1',
        'eng_proficiency_write_spanish': '1',
        'eng_proficiency_oral_spanish': '1',
        'eng_proficiency_speak_english': '1',
        'eng_proficiency_read_english': '1',
        'eng_proficiency_write_english': '1',
        'eng_proficiency_oral_english': '1',
        'hispanic': '1',
        'visityr': '2018',
        'visitmo': '11',
        'form_cls_linguistic_history_of_subject_complete': '2',
    }


if __name__ == "__main__":
    unittest.main()
