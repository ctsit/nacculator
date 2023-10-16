import unittest

from nacc import redcap2nacc
from nacc.ftld.ivp.builder import build_ftld_ivp_form


class option():
    flag = 'tfp'
    iorf = False
    cv = False
    csf = False
    lbd = False
    lbdsv = False
    tip = False
    tfp = True
    tfp3 = False
    ftld = False
    ivp = False
    fvp = False
    np = False
    np10 = False
    m = False


class TestTFPEventNameDetection(unittest.TestCase):
    '''
    These tests ensure that the cascading try/catch statements in redcap2nacc
    can find the Z1X form in different input csvs, since there are several
    options for what it can be called. The function should also return helpful
    error messages.
    '''

    def setUp(self):
        self.options = option()

    def test_tfp_standard_flag(self):
        '''
        Test the logic that looks for the Z1X form when the -tfp flag is
        selected. Uses the 1FloridaADRC Z1X field "tvp_z1x_checklist_complete"
        '''
        record = {'redcap_event_name': 'followup_arm_1', 'tvp_z1x_checklist_complete': '2'}

        actual = redcap2nacc.check_redcap_event(self.options, record)
        self.assertTrue(actual)

    def test_tfp_final_flag(self):
        '''
        Test the cascading try/except logic down to the field
        "tele_z1x_complete"
        '''
        record = {'redcap_event_name': 'followup_arm_1', 'tele_z1x_complete': '2'}

        actual = redcap2nacc.check_redcap_event(self.options, record)
        self.assertTrue(actual)

    def test_tfp_no_flag(self):
        '''
        Test that the function returns false when the event name check fails.
        '''
        record = {'redcap_event_name': 'followup_arm_1', 'z1x_complete': '2'}

        actual = redcap2nacc.check_redcap_event(self.options, record)
        self.assertFalse(actual)


if __name__ == "__main__":
    unittest.main()
