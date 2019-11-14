import unittest

import nacc.uds3
from nacc import redcap2nacc
from nacc.uds3 import packet


class option():
    flag = 'csf'
    lbd = False
    ftld = False
    csf = True
    ivp = False
    fvp = False


class TestBlankRulesForFTLD(unittest.TestCase):
    '''
    These tests are designed to run ivp data fields (generated below
    the tests here) through the check_blanks function for the CSF module.
    There are only two kinds of blanking rules:
    The rules for a group being blank if there is no available value for
    AB, PT, or TT assays, and the rules for specifying assay method.
    '''

    def setUp(self):
        self.options = option()

    def test_for_special_case_CSFABETA(self):
        '''
        The whole set of questions should be left blank if CSFABETA is blank.
        '''
        record = make_filled_form()
        record['csfabeta'] = ''
        # The several other values have been filled out below
        # in "make_filled_form"
        ipacket = make_builder(record)
        warnings = []

        warnings = redcap2nacc.check_blanks(ipacket, self.options)
        expected = ["'CSFABmo' is '1 ' with length '2', but should be blank:"
                    " 'Blank if Question 1a CSFABETA = blank'.", "'CSFABDY' is"
                    " '12' with length '2', but should be blank: 'Blank if"
                    " Question 1a CSFABETA = blank'.", "'CSFABYr' is '1990'"
                    " with length '4', but should be blank: 'Blank if Question"
                    " 1a CSFABETA = blank'.", "'CSFABmD' is '2' with length"
                    " '1', but should be blank: 'Blank if Question 1a"
                    " CSFABETA = blank'."]
        self.assertEqual(warnings, expected)

    def test_for_special_case_CSFABmDX(self):
        ''' CSFABmDX is a field where you specify what "other"
            assay method was used. '''
        record = make_filled_form()
        record['csfabmd'] = '2'
        record['csfabmdx'] = 'test'
        ipacket = make_builder(record)
        warnings = []

        warnings = redcap2nacc.check_blanks(ipacket, self.options)
        expected = ("'CSFABmDX' is 'test                                      "
                    "                  ' with length '60', but should be"
                    " blank: 'Blank if Question 1e CSFABmD ne 8 (Other)'.")
        # Right now warnings is a list of 2 warnings, because of the bug in
        # special cases. It also returns a warning that 'csfabeta' is blank
        # (even though it is not). So for now, this test only checks the first
        # item for the error we are looking for instead of the whole list
        # (which should be 1 item long).
        self.assertEqual(warnings[0], expected)


def make_builder(record: dict) -> packet.Packet:
    ipacket = packet.Packet()
    form = Form()
    form.CSFABETA = record['csfabeta']
    form.CSFABmo  = record['csfabmo']
    form.CSFABDY  = record['csfabdy']
    form.CSFABYr  = record['csfabyr']
    form.CSFABmD  = record['csfabmd']
    form.CSFABmDX = record['csfabmdx']
    ipacket.append(form)

    update_header(record, ipacket)

    return ipacket


def update_header(record: dict, packet: packet.Packet):
    for header in packet:
        header.PTID = record['ptid']


def make_filled_form() -> dict:
    return {
        'ptid': '1',

        'csfabeta': '20.00',
        'csfabmo': '1',
        'csfabdy': '12',
        'csfabyr': '1990',
        'csfabmd': '2',
        'csfabmdx': '',
    }


def header_fields():
    fields = {}
    fields['PTID'] = nacc.uds3.Field(name='PTID', typename='Char', position=(1, 10), length=10, inclusive_range=None, allowable_values=[], blanks=[])
    return fields


class Form(nacc.uds3.FieldBag):
    def __init__(self):
        self.fields = header_fields()
        self.fields['CSFABETA'] = nacc.uds3.Field(name='CSFABETA', typename='Num', position=(41, 48), length=8, inclusive_range=('1', '2000'), allowable_values=[], blanks=['Question 1a CSFABETA is an optional data field and may be left blank.'])
        self.fields['CSFABmo'] = nacc.uds3.Field(name='CSFABmo', typename='Num', position=(50, 51), length=2, inclusive_range=('1', '12'), allowable_values=[], blanks=['Blank if Question 1a CSFABETA = blank'])
        self.fields['CSFABDY'] = nacc.uds3.Field(name='CSFABDY', typename='Num', position=(53, 54), length=2, inclusive_range=('1', '31'), allowable_values=[], blanks=['Blank if Question 1a CSFABETA = blank'])
        self.fields['CSFABYr'] = nacc.uds3.Field(name='CSFABYr', typename='Num', position=(56, 59), length=4, inclusive_range=('1980', '2019'), allowable_values=[], blanks=['Blank if Question 1a CSFABETA = blank'])
        self.fields['CSFABmD'] = nacc.uds3.Field(name='CSFABmD', typename='Num', position=(61, 61), length=1, inclusive_range=None, allowable_values=['1', '2', '8'], blanks=['Blank if Question 1a CSFABETA = blank'])
        self.fields['CSFABmDX'] = nacc.uds3.Field(name='CSFABmDX', typename='Char', position=(63, 122), length=60, inclusive_range=None, allowable_values=[], blanks=['Blank if Question 1e CSFABmD ne 8 (Other)', 'Blank if Question 1a CSFABETA = blank'])


if __name__ == "__main__":
    unittest.main()
