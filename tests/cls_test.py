import unittest
from io import StringIO

from nacc.uds3 import clsform
from nacc.uds3 import packet
from nacc.uds3.fvp import forms as fvp_forms
from nacc.uds3.ivp import forms as ivp_forms


class TestCLS(unittest.TestCase):

    def test_cls_blank_not_added_to_ivp(self):
        """Don't add blank CLS form to IVP."""
        record = make_blank_record()
        record['hispanic'] = '1'  # Subject is Hispanic/Latino.

        ipacket = packet.Packet()
        clsform.add_cls(record, ipacket, ivp_forms)
        self.assertEqual(len(ipacket), 0, "Expected packet to be empty")

        fpacket = packet.Packet()
        clsform.add_cls(record, fpacket, fvp_forms)
        self.assertEqual(len(fpacket), 0, "Expected packet to be empty")

    def test_cls_not_added_if_not_hispanic(self):
        """
        Do not add Form CLS if the subject is not Hispanic/Latino.

        https://www.alz.washington.edu/NONMEMBER/UDS/DOCS/VER3/CLS/CLS_en.pdf
        """
        record = make_blank_record()
        record['hispanic'] = '0'  # Subject is not Hispanic/Latino.

        ipacket = packet.Packet()
        clsform.add_cls(record, ipacket, ivp_forms)
        self.assertEqual(len(ipacket), 0, "Expected packet to be empty")

        fpacket = packet.Packet()
        clsform.add_cls(record, fpacket, fvp_forms)
        self.assertEqual(len(fpacket), 0, "Expected packet to be empty")

    def test_cls_added_when_filled(self):
        """Add filled CLS form to IVP and FVP."""
        record = make_filled_record()

        ipacket = packet.Packet()
        clsform.add_cls(record, ipacket, ivp_forms)
        self.assertEqual(len(ipacket), 1, "Expected packet to have CLS")

        fpacket = packet.Packet()
        clsform.add_cls(record, fpacket, fvp_forms)
        self.assertEqual(len(fpacket), 1, "Expected packet to have CLS")

    def test_partial_cls_has_warning(self):
        """Partially completed CLS should create a warning."""    
        record = make_filled_record()   
        record['eng_preferred_language'] = ' '  # Make form partially complete. 

        ipacket = packet.Packet()
        itrap = StringIO()
        clsform.add_cls(record, ipacket, ivp_forms, itrap)
        assert itrap.getvalue() == "[WARNING] CLS form is incomplete for PTID: unknown\n"
        itrap.close()

        fpacket = packet.Packet()
        ftrap = StringIO()
        clsform.add_cls(record, fpacket, fvp_forms, ftrap)
        assert ftrap.getvalue() == "[WARNING] CLS form is incomplete for PTID: unknown\n"
        ftrap.close()

    def test_cls_proficiency_not_100_has_warning(self):    
        """If language proficiency percentages do not add to 100, create a warning.""" 
        record = make_filled_record()   
        record['eng_percentage_english'] = '20' 
        record['eng_percentage_spanish'] = '9001'   

        ipacket = packet.Packet()
        itrap = StringIO()
        clsform.add_cls(record, ipacket, ivp_forms, itrap)
        assert itrap.getvalue() == "[WARNING] language proficiency percentages do not equal 100 for PTID : unknown\n"
        itrap.close()

        fpacket = packet.Packet()
        ftrap = StringIO()
        clsform.add_cls(record, ipacket, ivp_forms, ftrap)
        assert ftrap.getvalue() == "[WARNING] language proficiency percentages do not equal 100 for PTID : unknown\n"
        ftrap.close()

    def test_check_cls_date(self):
        """
        Having a CLS with a visit date before June 1, 2017 raises an exception.
        """
        record = make_filled_record()
        record['visityr'] = '2016'

        ipacket = packet.Packet()
        with self.assertRaises(Exception):
            clsform.add_cls(record, ipacket, ivp_forms)

        fpacket = packet.Packet()
        with self.assertRaises(Exception):
            clsform.add_cls(record, fpacket, fvp_forms)

    def test_cls_form_marked_complete(self):
        """If the completed CLS form is not marked complete, raise."""
        record = make_filled_record()
        record['form_cls_linguistic_history_of_subject_complete'] = '0 or 1'

        ipacket = packet.Packet()
        with self.assertRaises(Exception):
            clsform.add_cls(record, ipacket, ivp_forms)

        fpacket = packet.Packet()
        with self.assertRaises(Exception):
            clsform.add_cls(record, fpacket, fvp_forms)

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
        'hispanic': '1',    # This is from Form A1
        'visityr': '2018',
        'visitmo': '11',
        'form_cls_linguistic_history_of_subject_complete': '2',
    }


if __name__ == "__main__":
    unittest.main()
