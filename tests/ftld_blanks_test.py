import unittest

from nacc import redcap2nacc
from nacc.ftld.ivp.builder import build_uds3_ftld_ivp_form


class option():
    flag = 'ftld'
    iorf = 'ivp'
    csf = False
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
        ipacket = build_uds3_ftld_ivp_form(record)
        warnings = []

        warnings = redcap2nacc.check_blanks(ipacket, self.options)
        expected = ["'LANGA4' is '1' with length '1', but should be blank:"
                    " 'Blank if Question 4b A4SUB = 0 (No)'."]
        self.assertEqual(warnings, expected)

    def test_for_single_blanking_rule_returned(self):
        '''
        Have it make sure that only one error is returned from a list of
        rules when not working with special cases (special cases need a
        fix in a later feature branch)
        '''
        record = make_filled_form()
        record['ftdcppas'] = '2'
        record['ftdcppa'] = ''
        record['ftdpabvf'] = ''
        record['ftdppasl'] = '0'
        ipacket = build_uds3_ftld_ivp_form(record)
        warnings = []

        warnings = redcap2nacc.check_blanks(ipacket, self.options)
        expected = ["'FTDCPPAS' is '2' with length '1', but should be blank:"
                    " 'Blank if Question 1 FTDPPASL = 0 (No)'."]
        self.assertEqual(warnings, expected)

    def test_for_special_case_FTDCPC2F(self):
        '''
        One packet of questions should be left blank if FTDCPC2F has a value
        (anything between 95-98)
        '''
        record = make_filled_form()
        record['ftdcpc2f'] = '95'
        record['ftdhaird'] = '1'
        ipacket = build_uds3_ftld_ivp_form(record)
        warnings = []

        warnings = redcap2nacc.check_blanks(ipacket, self.options)
        expected = ("'FTDhAIRD' is '1' with length '1', but should be blank:"
                    " 'Blank if Question 0 FTDCPC2F = 95'.")
        self.assertEqual(warnings[0], expected)
        # Right now the test examines the fourth item in this list of errors
        # because "special_cases" returns every available error when it finds
        # that one rule is violated.

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
        ipacket = build_uds3_ftld_ivp_form(record)
        warnings = []

        warnings = redcap2nacc.check_blanks(ipacket, self.options)
        expected = ("'FTDMRIRF' is '0' with length '1', but should be blank: "
                    "'Blank if Question 2a, FTDMRIFA, = 0 (No) or 9"
                    " (Unknown)'.")
        self.assertEqual(warnings[2], expected)

    def test_for_special_case_FTDMRIOS(self):
        '''
        Have it make sure _blanking_rule_ftld_or2a works properly -
        This blanking rule has an extra condition added to the or2 rules
        (packet['FTDMRIOB'] != 1)
        '''
        record = make_filled_form()
        record['ftdmrios'] = '1'
        record['ftdmriob'] = '0'
        ipacket = build_uds3_ftld_ivp_form(record)
        warnings = []

        warnings = redcap2nacc.check_blanks(ipacket, self.options)
        # FTDMRIOS is a Char field with a length of 60 characters
        expected = ("'FTDMRIOS' is"
                    " '1                                                  "
                    "         ' with length '60', but should be blank:"
                    " 'Blank if Question 2a11 FTDMRIOB ne 1 (Yes)'.")
        self.assertEqual(warnings[3], expected)

    def test_for_FTDPABVF_0(self):
        '''
        Have it make sure _blanking_rule_for_others_left_blank is working by
        checking both 0 and False instances (it will skip if either of these
        is the case for two questions)
        '''
        record = make_filled_form()
        record['ftdpabvf'] = '9'
        record['ftdcppa'] = '0'
        ipacket = build_uds3_ftld_ivp_form(record)
        warnings = []

        warnings = redcap2nacc.check_blanks(ipacket, self.options)
        expected = ["'FTDPABVF' is '9' with length '1', but should be blank:"
                    " 'Blank if Question 12 FTDCPPA = 0 (No) '."]
        self.assertEqual(warnings, expected)

    def test_for_FTDPABVF_blank(self):
        record = make_filled_form()
        record['ftdpabvf'] = '9'
        record['ftdbvft'] = ''
        ipacket = build_uds3_ftld_ivp_form(record)
        warnings = []

        warnings = redcap2nacc.check_blanks(ipacket, self.options)
        expected = ["'FTDPABVF' is '9' with length '1', but should be blank:"
                    " 'Blank if Question 22 FTDBVFT = blank'."]
        self.assertEqual(warnings, expected)


def make_filled_form() -> dict:
    return {
        # Headers
        'ptid': '1',
        'adcid': '2',
        'visitmo': '1',
        'visitday': '1',
        'visityr': '2019',
        'visitnum': '1',
        'initials': '',
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
        # other variables in the builder:
        'langa1': '',
        'langa2': '',
        'a2sub': '',
        'a2not': '',
        'langa3': '',
        'a3sub': '',
        'a3not': '',
        'a4not': '',
        'langa5': '',
        'langb1': '',
        'b1sub': '',
        'b1not': '',
        'langb4': '',
        'langb5': '',
        'b5sub': '',
        'b5not': '',
        'langb6': '',
        'b6sub': '',
        'b6not': '',
        'langb7': '',
        'b7sub': '',
        'b7not': '',
        'langb8': '',
        'langb9': '',
        'langc2': '',
        'langd1': '',
        'langd2': '',
        'langa3a': '',
        'ftda3afs': '',
        'ftda3afr': '',
        'langb3f': '',
        'langb9f': '',
        'langc1f': '',
        'langc2f': '',
        'langc3f': '',
        'langc4f': '',
        'ftdc4fs': '',
        'ftdc4fr': '',
        'langc5f': '',
        'ftdc5fs': '',
        'ftdc5fr': '',
        'langc6f': '',
        'ftdc6fs': '',
        'ftdc6fr': '',
        'lange2f': '',
        'lange3f': '',
        'langcls': '',
        'clssub': '',
        'ftdrelco': '',
        'ftdsibby': '',
        'ftdchdby': '',
        'ftdstore': '',
        'ftdslear': '',
        'ftdcomme': '',
        'ftdltfas': '',
        'ftdlimb': '',
        'ftdbulb': '',
        'ftdgsev': '',
        'ftdgsevx': '',
        'ftdgtyp': '',
        'ftdgtypg': '',
        'ftdgtypx': '',
        'ftdppapo': '',
        'ftdppaiw': '',
        'ftdppasw': '',
        'ftdppapk': '',
        'ftdppags': '',
        'ftdppaeh': '',
        'ftdppacs': '',
        'ftdppass': '',
        'ftdppasr': '',
        'ftdppasd': '',
        'ftdbvdis': '',
        'ftdbvapa': '',
        'ftdbvlos': '',
        'ftdbvrit': '',
        'ftdbvhyp': '',
        'ftdbvneu': '',
        'ftdbvidl': '',
        'ftdemgpv': '',
        'ftdemgpy': '',
        'ftdemgmn': '',
        'ftdworrc': '',
        'ftdworrs': '',
        'ftdworrr': '',
        'ftdworic': '',
        'ftdworis': '',
        'ftdworir': '',
        'ftdworip': '',
        'ftdsemmt': '',
        'ftdsemaa': '',
        'ftdsemta': '',
        'ftdsemsu': '',
        'ftdanasw': '',
        'ftdanaow': '',
        'ftdanats': '',
        'ftdsenas': '',
        'ftdsenos': '',
        'ftdsensr': '',
        'ftdsenpr': '',
        'ftdnounc': '',
        'ftdverbc': '',
        'ftdratio': '',
        'ftdreaas': '',
        'ftdreaos': '',
        'ftdreasr': '',
        'ftdreapr': '',
        'ftdspit': '',
        'ftdnose': '',
        'ftdcoage': '',
        'ftdcry': '',
        'ftdcut': '',
        'ftdytrip': '',
        'ftdeatp': '',
        'ftdtella': '',
        'ftdopin': '',
        'ftdlaugh': '',
        'ftdshirt': '',
        'ftdkeepm': '',
        'ftdpickn': '',
        'ftdover': '',
        'ftdeatr': '',
        'ftdhairl': '',
        'ftdshirw': '',
        'ftdmove': '',
        'ftdhugs': '',
        'ftdloud': '',
        'ftdlost': '',
        'ftdsntot': '',
        'ftdsntbs': '',
        'ftdsntos': '',
        'ftdsnrat': '',
        'ftdself': '',
        'ftdbadly': '',
        'ftddepr': '',
        'ftdemotd': '',
        'ftdlself': '',
        'ftddisr': '',
        'ftdbelch': '',
        'ftdgigg': '',
        'ftdpriv': '',
        'ftdnegat': '',
        'ftdecomm': '',
        'ftdinapj': '',
        'ftdfaila': '',
        'ftdresis': '',
        'ftdinter': '',
        'ftdverba': '',
        'ftdphysi': '',
        'ftdtopic': '',
        'ftdproto': '',
        'ftdpreo': '',
        'ftdfini': '',
        'ftdacted': '',
        'ftdabs': '',
        'ftdfeedb': '',
        'ftdfrust': '',
        'ftdanxi': '',
        'ftdnervo': '',
        'ftdndiag': '',
        'ftdstimb': '',
        'ftdstime': '',
        'ftdobjec': '',
        'ftdcircu': '',
        'ftdperse': '',
        'ftdrepea': '',
        'ftdanecd': '',
        'ftddinit': '',
        'ftddelay': '',
        'ftdaddve': '',
        'ftdfluct': '',
        'ftdlostt': '',
        'ftdrepru': '',
        'ftdtrain': '',
        'ftddiscl': '',
        'ftdspont': '',
        'ftdsponr': '',
        'ftdstood': '',
        'ftdtouch': '',
        'ftddsoci': '',
        'ftdexagg': '',
        'ftdsbtot': '',
        'ftdsbcto': '',
        'ftdlengt': '',
        'ftdcpc4f': '',
        'ftdworku': '',
        'ftdmist': '',
        'ftdcrit': '',
        'ftdworr': '',
        'ftdbad': '',
        'ftdpoor': '',
        'ftdffear': '',
        'ftdbist': '',
        'ftdcpc5f': '',
        'ftdinsex': '',
        'ftdinfmo': '',
        'ftdinfyr': '',
        'ftdinfre': '',
        'ftdfeel': '',
        'ftddiff': '',
        'ftdsorr': '',
        'ftdside': '',
        'ftdadvan': '',
        'ftdimag': '',
        'ftdmisf': '',
        'ftdwaste': '',
        'ftdpity': '',
        'ftdqtouc': '',
        'ftdsides': '',
        'ftdsofth': '',
        'ftdupset': '',
        'ftdcriti': '',
        'ftdiriec': '',
        'ftdiript': '',
        'ftdcpc6f': '',
        'ftdalter': '',
        'ftdemot': '',
        'ftdacros': '',
        'ftdconv': '',
        'ftdintui': '',
        'ftdjoke': '',
        'ftdimagp': '',
        'ftdinapp': '',
        'ftdchbeh': '',
        'ftdadbeh': '',
        'ftdlying': '',
        'ftdgoodf': '',
        'ftdregul': '',
        'ftdsmscr': '',
        'ftdspscr': '',
        'ftdrsmst': '',
        'ftdsmri': '',
        'ftdsmmo': '',
        'ftdsmdy': '',
        'ftdsmyr': '',
        'ftdsmdic': '',
        'ftdsmdis': '',
        'ftdsmadn': '',
        'ftdsmadv': '',
        'ftdsmman': '',
        'ftdsmmao': '',
        'ftdsmmam': '',
        'ftdsmfs': '',
        'ftdsmfso': '',
        'ftdsmqu': '',
        'ftdfdgpt': '',
        'ftdfpmo': '',
        'ftdfpdy': '',
        'ftdfpyr': '',
        'ftdfddic': '',
        'ftdfddid': '',
        'ftdfdadn': '',
        'ftdfdadv': '',
        'ftdfdman': '',
        'ftdfdmao': '',
        'ftdfdmam': '',
        'ftdfdqu': '',
        'ftdamypt': '',
        'ftdammo': '',
        'ftdamdy': '',
        'ftdamyr': '',
        'ftdamdic': '',
        'ftdamdid': '',
        'ftdamlig': '',
        'ftdamlio': '',
        'ftdamadn': '',
        'ftdamadv': '',
        'ftdamman': '',
        'ftdammao': '',
        'ftdammam': '',
        'ftdamqu': '',
        'ftdother': '',
        'ftdotdop': '',
        'ftdotser': '',
        'ftdotcho': '',
        'ftdotano': '',
        'ftdotans': '',
        'ftdmrilf': '',
        'ftdmrirt': '',
        'ftdmrilt': '',
        'ftdmrirm': '',
        'ftdmrilm': '',
        'ftdmrirp': '',
        'ftdmrilp': '',
        'ftdmrirb': '',
        'ftdmrilb': '',
        'ftdfdgpe': '',
        'ftdfdgfh': '',
        'ftdfdgrf': '',
        'ftdfdglf': '',
        'ftdfdgrt': '',
        'ftdfdglt': '',
        'ftdfdgrm': '',
        'ftdfdglm': '',
        'ftdfdgrp': '',
        'ftdfdglp': '',
        'ftdfdgrb': '',
        'ftdfdglb': '',
        'ftdfdgoa': '',
        'ftdfdgos': '',
        'ftdamyp': '',
        'ftdamyvi': '',
        'ftdamyrf': '',
        'ftdamylf': '',
        'ftdamyrt': '',
        'ftdamylt': '',
        'ftdamyrm': '',
        'ftdamylm': '',
        'ftdamyrp': '',
        'ftdamylp': '',
        'ftdamyrb': '',
        'ftdamylb': '',
        'ftdamyoa': '',
        'ftdamyos': '',
        'ftdcbfsp': '',
        'ftdcbfvi': '',
        'ftdcbfrf': '',
        'ftdcbflf': '',
        'ftdcbfrt': '',
        'ftdcbflt': '',
        'ftdcbfrm': '',
        'ftdcbflm': '',
        'ftdcbfrp': '',
        'ftdcbflp': '',
        'ftdcbfrb': '',
        'ftdcbflb': '',
        'ftdcbfoa': '',
        'ftdcbfos': '',
        'ftdothi': '',
        'ftdothis': '',
    }


if __name__ == "__main__":
    unittest.main()
