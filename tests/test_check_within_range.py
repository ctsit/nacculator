import unittest

import nacc.uds3


class TestWithinRange(unittest.TestCase):
    '''
    These tests are designed to run ivp data fields (generated below
    the tests here) through the Field class in the uds3.__init__ file.
    It is checking to ensure that the Field class catches errors in the
    "allowable_values" and "inclusive_range" variables.
    '''

    def test_for_Char_fields_skipping_range_check(self):
        '''
        Have it make sure that only Num fields are being checked for range
        '''
        racex = nacc.uds3.Field(name='RACEX', typename='Char', position=(136, 195), length=60, inclusive_range=None, allowable_values=[], blanks=[])

        racex.value = 'race'
        expected = 'race'
        self.assertEqual(racex.val, expected)

    def test_for_allowed_values_within_range(self):
        '''
        Ensure that the 'if self.allowable_values' statement returns expected
        errors
        '''
        reason = nacc.uds3.Field(name='REASON', typename='Num', position=(45, 45), length=1, inclusive_range=(1, 4), allowable_values=['4', '2', '1', '9'], blanks=[])

        with self.assertRaises(ValueError):
            reason.value = '10'

    def test_for_allowed_values_out_of_range(self):
        '''
        Ensure that the 'if self.allowable_values' statement does not return
        errors if a value is out of the inclusive_range but within
        allowable_values, such as a field that expects 1-3, but also allows 9
        (like 9 = Unknown)
        '''
        reason = nacc.uds3.Field(name='REASON', typename='Num', position=(45, 45), length=1, inclusive_range=(1, 4), allowable_values=['4', '2', '1', '9'], blanks=[])

        reason.value = '9'
        expected = '9'
        self.assertEqual(reason.val, expected)

    # value.setter cannot catch value errors where the value is technically
    # within the inclusive range, but not one of the allowable values (for
    # example, 'REASON' above has the range 1-4, but only allowable values of
    # 1, 2, and 4) because other fields have that option and SHOULDN'T return
    # errors (for example, a field that has the inclusive_range '1-12' but
    # also a survey error code '88' as the only entry in its allowable_values)

    def test_for_within_range_without_allowable_values(self):
        '''
        Ensure that the 'if no self.allowable_values' statement returns
        out-of-range errors when there is an inclusive_range but no specific
        allowable_values
        '''
        kids = nacc.uds3.Field(name='KIDS', typename='Num', position=(956, 957), length=2, inclusive_range=(0, 15), allowable_values=[], blanks=[])

        with self.assertRaises(ValueError):
            kids.value = '16'


if __name__ == "__main__":
    unittest.main()
