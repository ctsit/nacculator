import unittest

from nacc.redcap2nacc import check_valid_visit_date
from datetime import date


class option():
    flag = 'ivp'
    iorf = False
    cv = False
    csf = False
    lbd = False
    tip = False
    tfp = False
    tfp3 = False
    ftld = False
    ivp = True
    fvp = False
    m = False
    np = False


class TestValidVisitdate(unittest.TestCase):
    '''
    These tests validate the "check_valid_visit_date" function in redcap2nacc
    by making sure that the visitdate is not beyond today's date.
    '''

    def setUp(self):
        self.options = option()

    def test_return_error_if_date_is_past_todays_date(self):
        record = make_filled_form()
        current_year = date.today().year
        record['visityr'] = str(current_year + 1)
        invalid_date = check_valid_visit_date(record, self.options)
        self.assertTrue(invalid_date)

    def test_do_not_return_error_if_date_is_before_todays_date(self):
        record = make_filled_form()
        valid_date = check_valid_visit_date(record, self.options)
        self.assertFalse(valid_date)


def make_filled_form() -> dict:
    return {
        # Header
        'ptid': '1',
        'adcid': '2',
        'visitmo': '1',
        'visitday': '1',
        'visityr': '2020',
        'visitnum': '1',
        'initials': ''
    }


if __name__ == "__main__":
    unittest.main()
