import unittest

from nacc.redcap2nacc import check_valid_visit_date
from datetime import date


class TestValidVisitdate(unittest.TestCase):

    def test_return_error_if_date_is_past_todays_date(self):
        record = make_filled_form()
        current_year = date.today().year
        record['visityr'] = str(current_year + 1)
        invalid_date = check_valid_visit_date(record)
        self.assertTrue(invalid_date)

    def test_do_not_return_error_if_date_is_before_todays_date(self):
        record = make_filled_form()
        valid_date = check_valid_visit_date(record)
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
