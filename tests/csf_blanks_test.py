import unittest

from nacc import redcap2nacc
from nacc.csf.builder import build_uds3_csf_form


class option():
    flag = 'csf'
    lbd = False
    ftld = False
    csf = True
    ivp = False
    fvp = False


class TestBlankRulesForCSF(unittest.TestCase):
    '''
    These tests are designed to run CSF data fields (generated below
    the tests here) through the check_blanks function for the CSF module.
    There are only two kinds of blanking rules:
    The rules for a group being blank if there is no available value for
    AB, PT, or TT assays, and the rules for specifying assay method.

    In the CSF module, I introduced logic in the blanking files for handling
    fields with rules like "blank if (previous question) = blank". This unit
    test is concerned with making sure this new function works properly,
    and only returns the rule that was violated (or returns both rules, if two
    have been violated).
    '''

    def setUp(self):
        self.options = option()

    def test_for_blank_form_when_CSFABETA(self):
        '''
        The whole set of questions should be left blank if CSFABETA is blank.
        '''
        record = make_filled_form()
        record['csfabeta'] = ''
        ipacket = build_uds3_csf_form(record)

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

    def test_for_single_error_CSFABmDX(self):
        ''' CSFABmDX is a field where you specify what "other"
            assay method was used. '''
        record = make_filled_form()
        record['csfabmd'] = '2'
        record['csfabmdx'] = 'test'
        ipacket = build_uds3_csf_form(record)
        warnings = []

        warnings = redcap2nacc.check_blanks(ipacket, self.options)
        expected = ["'CSFABmDX' is 'test                                      "
                    "                  ' with length '60', but should be"
                    " blank: 'Blank if Question 1e CSFABmD ne 8 (Other)'."]
        self.assertEqual(warnings, expected)

    def test_for_multiple_error_CSFABmDX(self):
        '''
        CSFABmDX must be left blank if CSFABmD is not "other," but also
        when CSFABETA is left blank.
        This is testing both rules at the same time.'''
        record = make_filled_form()
        record['csfabeta'] = ''
        record['csfabmo'] = ''
        record['csfabdy'] = ''
        record['csfabyr'] = ''
        record['csfabmd'] = '2'
        record['csfabmdx'] = 'test'
        ipacket = build_uds3_csf_form(record)
        warnings = []

        warnings = redcap2nacc.check_blanks(ipacket, self.options)
        expected = ["'CSFABmD' is '2' with length '1', but should be blank:"
                    " 'Blank if Question 1a CSFABETA = blank'.",
                    "'CSFABmDX' is 'test                                      "
                    "                  ' with length '60', but should be"
                    " blank: 'Blank if Question 1e CSFABmD ne 8 (Other)'.",
                    "'CSFABmDX' is 'test                                      "
                    "                  ' with length '60', but should be"
                    " blank: 'Blank if Question 1a CSFABETA = blank'."]
        # Since CSFABETA is blank, CSFABmD should technically also be blank,
        # so the first error is also returned.
        self.assertEqual(warnings, expected)


def make_filled_form() -> dict:
    return {
        # Headers
        'ptid': '1',
        'adcid': '',
        'visitmo': '',
        'visitday': '',
        'visityr': '',
        'csflpmo': '',
        'csflpdy': '',
        'csflpyr': '',
        'csfinit': '',

        # CSF Data
        'csfabeta': '20.00',
        'csfabmo': '1',
        'csfabdy': '12',
        'csfabyr': '1990',
        'csfabmd': '2',
        'csfabmdx': '',
        'csfptau': '',
        'csfptmo': '',
        'csfptdy': '',
        'csfptyr': '',
        'csfptmd': '',
        'csfptmdx': '',
        'csfttau': '',
        'csfttmo': '',
        'csfttdy': '',
        'csfttyr': '',
        'csfttmd': '',
        'csfttmdx': '',
    }


if __name__ == "__main__":
    unittest.main()
