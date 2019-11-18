import unittest

import nacc.uds3
from nacc.uds3 import Field
from nacc import redcap2nacc
from nacc.uds3 import packet


class option():
    iorf = 'ivp'
    lbd = False
    ftld = False
    ivp = True
    fvp = False


class TestWithinRange(unittest.TestCase):
    '''
    These tests are designed to run ivp data fields (generated below
    the tests here) through the Field class in the uds3.__init__ file.
    It is checking to ensure that the Field class catches errors in the
    "allowable_values" and "inclusive_range" variables.
    '''

    def setUp(self):
        self.options = option()

    def test_for_Field_variables_entered(self):
        ''' Have it check that the Field class is picking up our input '''
        record = make_filled_form()
        record['reason'] = '1'
        ipacket = make_builder(record)
        item = Form.field.REASON

        result = Field(item)
        expected = []  # The expected output will be different... no output?
        self.assertEqual(result, expected)

    def test_for_Char_fields_skipping_range_check(self):
        '''
        Have it make sure that only Num fields are being checked for range
        '''
        record = make_filled_form()
        record['racex'] = 'race'
        ipacket = make_builder(record)
        item = Form.field.RACEX

        result = Field(item)
        expected = []
        self.assertEqual(result, expected)

    def test_for_allowed_values_within_range(self):
        '''
        Ensure that the 'if self.allowable_values' statement returns expected
        errors
        '''
        record = make_filled_form()
        record['reason'] = '1'
        ipacket = make_builder(record)
        item = Form.field.REASON

        with self.assertRaises(ValueError):
            result = Field(item)

    def test_for_allowed_values_out_of_range(self):
        '''
        Ensure that the 'if self.allowable_values' statement does not return
        errors if a value is out of the inclusive_range but within
        allowable_values, such as a field that expects 1-3, but also allows 9
        (like 9 = Unknown)
        '''
        record = make_filled_form()
        record['reason'] = '9'
        ipacket = make_builder(record)
        item = Form.field.REASON

        result = Field(item)
        expected = []
        self.assertEqual(item, expected)

    def test_for_forbidden_values_within_range(self):
        '''
        Ensure that values that are within the allowed range, but not part
        of allowable_values, return an error
        '''
        record = make_filled_form()
        record['reason'] = '3'
        ipacket = make_builder(record)
        item = Form.field.REASON

        with self.assertRaises(ValueError):
            result = Field(item)

    def test_for_within_range_without_allowable_values(self):
        '''
        Ensure that the 'if no self.allowable_values' statement returns
        out-of-range errors when there is an inclusive_range but no specific
        allowable_values
        '''
        record = make_filled_form()
        record['kids'] = '16'
        ipacket = make_builder(record)
        item = Form.field.KIDS

        with self.assertRaises(ValueError):
            result = Field(item)


def make_builder(record: dict) -> packet.Packet:
    ipacket = packet.Packet()
    form = Form()
    form.RACEX = record['racex']
    form.REASON = record['reason']
    form.KIDS = record['kids']
    ipacket.append(form)

    update_header(record, ipacket)

    return ipacket


def update_header(record: dict, packet: packet.Packet):
    for header in packet:
        header.PTID = record['ptid']


def make_filled_form() -> dict:
    return {
        'ptid': '1',
        'racex': '',
        'reason': '',
        'kids': '',
    }


def header_fields():
    fields = {}
    fields['PTID'] = nacc.uds3.Field(name='PTID', typename='Char', position=(1, 10), length=10, inclusive_range=None, allowable_values=[], blanks=[])
    return fields


class Form(nacc.uds3.FieldBag):
    def __init__(self):
        self.fields = header_fields()
        self.fields['RACEX'] = nacc.uds3.Field(name='RACEX', typename='Char', position=(136, 195), length=60, inclusive_range=None, allowable_values=[], blanks=[])
        self.fields['REASON'] = nacc.uds3.Field(name='REASON', typename='Num', position=(45, 45), length=1, inclusive_range=(1, 4), allowable_values=['4', '2', '1', '9'], blanks=[])
        self.fields['KIDS'] = nacc.uds3.Field(name='KIDS', typename='Num', position=(956, 957), length=2, inclusive_range=(0, 15), allowable_values=[], blanks=[])


if __name__ == "__main__":
    unittest.main()
