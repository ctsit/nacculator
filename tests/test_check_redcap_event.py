import unittest

from nacc.redcap2nacc import check_redcap_event


class option():
    lbd = False
    lbdsv = False
    ftld = False
    csf = False
    cv = False
    np = False
    np10 = False
    m = False
    ivp = False
    fvp = False


class TestRedcapEvent(unittest.TestCase):
    '''
    These tests are meant to ensure that the check_redcap_event function is
    properly distinguishing between REDCap events in an imported CSV of various
    records. Ideally, redcap2nacc should only be outputting PTIDs with the
    redcap_event_name specified by the options flag (-ivp, -ldb, et cetera) and
    skipping all others, leaving an output .txt file with no blank lines.
    '''

    def setUp(self):
        self.options = option()

    def test_for_ivp(self):
        '''
        Checks that the -ivp flag with no other options returns the correct
        visit (not LBD IVP or FTLD IVP).
        '''
        self.options.ivp = True
        record = {'redcap_event_name': 'initial_visit_year_arm_1',
                  'ivp_z1_complete': '', 'ivp_z1x_complete': '2', 
                  'ivp_a1_complete': '2'}
        result = check_redcap_event(self.options, record)
        self.assertTrue(result)

    def test_for_not_ivp(self):
        '''
        Checks that the initial_visit is not returned when the -ivp flag is not
        set.
        '''
        self.options.fvp = True
        record = {'redcap_event_name': 'initial_visit_year_arm_1',
                  'fvp_z1_complete': '', 'fvp_z1x_complete': '',
                  'fvp_a1_complete': '2'}
        result = check_redcap_event(self.options, record)
        self.assertFalse(result)

    def test_for_multiple_flags(self):
        '''
        Checks that options like -lbd -ivp are functional.
        '''
        self.options.ivp = True
        self.options.lbd = True
        record = {'redcap_event_name': 'initial_visit_year_arm_1',
                  'lbd_ivp_b1l_complete': '2'}
        result = check_redcap_event(self.options, record)
        self.assertTrue(result)

    def test_for_not_multiple_flags(self):
        '''
        Checks that -ivp alone is not returned with options like -lbd -ivp.
        '''
        self.options.ivp = True
        record = {'redcap_event_name': 'initial_visit_year_arm_1',
                  'ivp_z1_complete': '', 'ivp_z1x_complete': '',
                  'lbd_ivp_b1l_complete': '2', 'ivp_a1_complete': '2'}
        incorrect = check_redcap_event(self.options, record)

        self.options.lbd = True
        result = check_redcap_event(self.options, record)
        self.assertNotEqual(incorrect, result)

    def test_for_np_no_event(self):
        '''
        Checks that the -np flag's redcap_event_name is optional.
        This is because Neuropath data can come from separate REDCap projects
        dedicated to NP and BDS data only.
        redcap2nacc sets non-longitudinal NP events to "NP".
        '''
        self.options.np = True
        record = {'formver_11': '11'}
        result = check_redcap_event(self.options, record)
        self.assertNotEqual('NP', result)


if __name__ == "__main__":
    unittest.main()
