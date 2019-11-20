import unittest

import nacc.uds3
from nacc import redcap2nacc
from nacc.ftld import packet


class option():
    flag = 'ftld'
    iorf = 'ivp'
    lbd = False
    ftld = True
    ivp = True
    fvp = False


class TestBlankRulesForFTLD(unittest.TestCase):
    '''
    These tests are designed to run ivp data fields (generated below
    the tests here) through the check_blanks function for the FTLD module.
    It is mostly concerned with making sure the "special cases" are functioning
    properly.
    '''

    def setUp(self):
        self.options = option()

    def test_for_filled_when_ruled_blank(self):
        # Have it look for the langa4 error to see that general blanking rules
        # are working (langa4 also comes before the variable (a4sub)
        # it's dependent on)
        record = make_filled_form()
        record['a4sub'] = '0'
        record['langa4'] = '1'
        ipacket = make_builder(record)
        warnings = []

        warnings = redcap2nacc.check_blanks(ipacket, self.options)
        expected = ["'LANGA4' is '1' with length '1', but should be blank:"
                    " 'Blank if Question 1 A4SUB = 0 (No)'."]
        self.assertEqual(warnings, expected)

    def test_for_single_blanking_rule_returned(self):
        '''
        Have it make sure that only one error is returned from a list of
        rules when not working with special cases (special cases need a
        fix in a later feature branch)
        '''
        record = make_filled_form()
        record['ftdcppas'] = '2'
        record['ftdppasl'] = '0'
        ipacket = make_builder(record)
        warnings = []

        warnings = redcap2nacc.check_blanks(ipacket, self.options)
        expected = ["'FTDCPPAS' is '2' with length '1', but should be blank:"
                    " 'Blank if Question 1 FTDPPASL = 0 (No)'."]
        self.assertEqual(warnings[0], expected[0]) 
        # An error about another variable is also returned, so we are only
        # looking at the first item on the list

    def test_for_special_case_FTDCPC2F(self):
        '''
        One packet of questions should be left blank if FTDCPC2F has a value
        (anything between 95-98)
        '''
        record = make_filled_form()
        record['ftdcpc2f'] = '95'
        record['ftdhaird'] = '1'
        ipacket = make_builder(record)
        warnings = []

        warnings = redcap2nacc.check_blanks(ipacket, self.options)
        expected = ["'FTDhAIRD' is '1' with length '1', but should be blank:"
                    " 'Blank if Question 0 FTDCPC2F = 95'."]
        self.assertEqual(warnings, expected)

    def test_for_special_case_or2(self):
        '''
        Have it make sure _blanking_rule_ftld_or2 works properly (and by
        extension or3, or4, and or5) - This blanking rule depends on either
        of two possible answers to questions, along with regular
        blanking rules
        '''
        record = make_filled_form()
        record['ftdmrirf'] = '0'
        record['ftdmrifa'] = '9'
        record['ftdmriob'] = ''
        ipacket = make_builder(record)
        warnings = []

        warnings = redcap2nacc.check_blanks(ipacket, self.options)
        expected = ["'FTDMRIRF' is '0' with length '1', but should be blank: "
                    "'Blank if Question 2a FTDMRIFA = 0 (No) or 9 (Unknown)'."]
        self.assertEqual(warnings, expected)

    def test_for_special_case_FTDMRIOS(self):
        '''
        Have it make sure _blanking_rule_ftld_or2a works properly -
        This blanking rule has an extra condition added to the or2 rules
        (packet['FTDMRIOB'] != 1)
        '''
        record = make_filled_form()
        record['ftdmrios'] = '1'
        record['ftdmriob'] = '0'
        ipacket = make_builder(record)
        warnings = []

        warnings = redcap2nacc.check_blanks(ipacket, self.options)
        # FTDMRIOS is a Char field with a length of 60 characters
        expected = ["'FTDMRIOS' is"
                    " '1                                                  "
                    "         ' with length '60', but should be blank:"
                    " 'Blank if Question 2a11 FTDMRIOB ne 1 (Yes)'."]
        self.assertEqual(warnings, expected)

    def test_for_special_case_FTDPABVF_0(self):
        '''
        Have it make sure _blanking_rule_for_others_left_blank is working by
        checking both 0 and False instances (it will skip if either of these
        is the case for two questions)
        '''
        record = make_filled_form()
        record['ftdpabvf'] = '9'
        record['ftdcppa'] = '0'
        ipacket = make_builder(record)
        warnings = []

        warnings = redcap2nacc.check_blanks(ipacket, self.options)
        expected = ["'FTDPABVF' is '9' with length '1', but should be blank:"
                    " 'Blank if Question 12 FTDCPPA = 0 (No) '."]
        self.assertEqual(warnings, expected)

    def test_for_special_case_FTDPABVF_blank(self):
        record = make_filled_form()
        record['ftdpabvf'] = '9'
        record['ftdbvft'] = ''
        ipacket = make_builder(record)
        warnings = []

        warnings = redcap2nacc.check_blanks(ipacket, self.options)
        expected = ["'FTDPABVF' is '9' with length '1', but should be blank:"
                    " 'Blank if Question 22 FTDBVFT = blank'."]
        self.assertEqual(warnings, expected)


def make_builder(record: dict) -> packet.Packet:
    ipacket = packet.Packet()
    form = Form()
    form.FTDIDIAG = record['ftdidiag']
    form.LANGA4 = record['langa4']
    form.FTDCPPAS = record['ftdcppas']
    form.FTDhAIRD = record['ftdhaird']
    form.FTDMRIRF = record['ftdmrirf']
    form.FTDSMRIO = record['ftdsmrio']
    form.FTDMRIOS = record['ftdmrios']
    form.FTDPABVF = record['ftdpabvf']
    form.A4SUB = record['a4sub']
    form.FTDPPASL = record['ftdppasl']
    form.FTDCPC2F = record['ftdcpc2f']
    form.FTDMRIFA = record['ftdmrifa']
    form.FTDMRIOB = record['ftdmriob']
    form.FTDCPPA = record['ftdcppa']
    form.FTDBVCLN = record['ftdbvcln']
    form.FTDBVFT = record['ftdbvft']
    ipacket.append(form)

    update_header(record, ipacket)

    return ipacket


def update_header(record: dict, packet: packet.Packet):
    for header in packet:
        header.PTID = record['ptid']


def make_filled_form() -> dict:
    return {
        'ptid': '1',
        # Begin variables to be tested
        'langa4': '',  # This is a general blanking rule not in special cases
        'ftdcppas': '',  # This is a general blanking rule with two rules
        'ftdhaird': '',
        'ftdmrirf': '',
        'ftdmrios': '',
        'ftdpabvf': '1',
        # End variables to be tested
        'ftdsmrio': '1',
        'ftdidiag': '1',
        'a4sub': '0',
        'ftdppasl': '1',
        'ftdcpc2f': '95',  # _blanking_rule_ftld_q_noanswer
        'ftdmrifa': '1',  # _blanking_rule_ftld_or2
        'ftdmriob': '1',  # _blanking_rule_ftld_or2a
        'ftdcppa': '1',  # _blanking_rule_for_others_left_blank "0" condition
        'ftdbvcln': '1',
        'ftdbvft': '3',  # _blanking_rule_for_others_left_blank "" condition
    }


def header_fields():
    fields = {}
    fields['PTID'] = nacc.uds3.Field(name='PTID', typename='Char', position=(1, 10), length=10, inclusive_range=None, allowable_values=[], blanks=[])
    return fields


class Form(nacc.uds3.FieldBag):
    def __init__(self):
        self.fields = header_fields()
        self.fields['FTDIDIAG'] = nacc.uds3.Field(name='FTDIDIAG', typename='Num', position=(45, 45), length=1, inclusive_range=(0, 1), allowable_values=['0', '1'], blanks=[])
        self.fields['A4SUB'] = nacc.uds3.Field(name='A4SUB', typename='Num', position=(12, 12), length=1, inclusive_range=(0, 1), allowable_values=['0', '1'], blanks=[])
        self.fields['LANGA4'] = nacc.uds3.Field(name='LANGA4', typename='Num', position=(14, 14), length=1, inclusive_range=(1, 2), allowable_values=['1', '2'], blanks=['Blank if Question 1 A4SUB = 0 (No)'])
        self.fields['FTDPPASL'] = nacc.uds3.Field(name='FTDPPASL', typename='Num', position=(16, 16), length=1, inclusive_range=(0, 1), allowable_values=['0', '1'], blanks=[])
        self.fields['FTDCPC2F'] = nacc.uds3.Field(name='FTDCPC2F', typename='Num', position=(18, 19), length=2, inclusive_range=None, allowable_values=['95', '96', '97', '98'], blanks=['Blank if form completed'])
        self.fields['FTDSMRIO'] = nacc.uds3.Field(name='FTDSMRIO', typename='Num', position=(47, 47), length=1, inclusive_range=(0, 1), allowable_values=['0', '1'], blanks=['Blank if Question 1 FTDIDIAG = 0 (No)'])
        self.fields['FTDMRIFA'] = nacc.uds3.Field(name='FTDMRIFA', typename='Num', position=(21, 21), length=1, inclusive_range=(0, 1), allowable_values=['0', '1', '9'], blanks=['Blank if Question 1 FTDIDIAG = 0 (No)', 'Blank if Question 2 FTDSMRIO = 0 (No)'])
        self.fields['FTDMRIOB'] = nacc.uds3.Field(name='FTDMRIOB', typename='Num', position=(23, 23), length=1, inclusive_range=(0, 1), allowable_values=['0', '1', '9'], blanks=['Blank if Question 1 FTDIDIAG = 0 (No)', 'Blank if Question 2 FTDSMRIO = 0 (No)', 'Blank if Question 2a FTDMRIFA = 0 (No) or 9 (Unknown)'])
        self.fields['FTDBVCLN'] = nacc.uds3.Field(name='FTDBVCLN', typename='Num', position=(71, 71), length=1, inclusive_range=(0, 1), allowable_values=['0', '1'], blanks=[])
        self.fields['FTDBVFT'] = nacc.uds3.Field(name='FTDBVFT', typename='Num', position=(25, 25), length=1, inclusive_range=(0, 3), allowable_values=['0', '1', '2', '3'], blanks=['Blank if Question 14 FTDBVCLN = 0 (No)'])
        self.fields['FTDCPPAS'] = nacc.uds3.Field(name='FTDCPPAS', typename='Num', position=(27, 27), length=1, inclusive_range=(1, 4), allowable_values=['1', '2', '3', '4'], blanks=['Blank if Question 1 FTDPPASL = 0 (No)', 'Blank if Question 12 FTDCPPA = 0 (No)'])
        self.fields['FTDhAIRD'] = nacc.uds3.Field(name='FTDhAIRD', typename='Num', position=(29, 29), length=1, inclusive_range=(0, 1), allowable_values=['0', '1'], blanks=['Blank if Question 0 FTDCPC2F = 95', 'Blank if Question 0 FTDCPC2F = 96', 'Blank if Question 0 FTDCPC2F = 97', 'Blank if Question 0 FTDCPC2F = 98', 'Blank if question not answered'])
        self.fields['FTDMRIRF'] = nacc.uds3.Field(name='FTDMRIRF', typename='Num', position=(31, 31), length=1, inclusive_range=(0, 1), allowable_values=['0', '1', '9'], blanks=['Blank if Question 1 FTDIDIAG = 0 (No)', 'Blank if Question 2 FTDSMRIO = 0 (No)', 'Blank if Question 2a FTDMRIFA = 0 (No) or 9 (Unknown)'])
        self.fields['FTDMRIOS'] = nacc.uds3.Field(name='FTDMRIOS', typename='Char', position=(33, 93), length=60, inclusive_range=None, allowable_values=[], blanks=['Blank if Question 1 FTDIDIAG = 0 (No)', 'Blank if Question 2 FTDSMRIO = 0 (No)', 'Blank if Question 2a FTDMRIFA = 0 (No) or 9 (Unknown)', 'Blank if Question 2a11 FTDMRIOB ne 1 (Yes)'])
        self.fields['FTDPABVF'] = nacc.uds3.Field(name='FTDPABVF', typename='Num', position=(95, 95), length=1, inclusive_range=(1, 5), allowable_values=['1', '2', '3', '4', '5', '9'], blanks=['Blank if Question 12 FTDCPPA = 0 (No) ', 'Blank if Question 12 FTDCPPA = blank', 'Blank if Question 22 FTDBVFT = 0 (Does not meet criteria)', 'Blank if Question 22 FTDBVFT = blank'])
        self.fields['FTDCPPA'] = nacc.uds3.Field(name='FTDCPPA', typename='Num', position=(97, 97), length=1, inclusive_range=(0, 1), allowable_values=['0', '1'], blanks=['Blank if Question 1 FTDPPASL = 0 (No)'])


if __name__ == "__main__":
    unittest.main()
