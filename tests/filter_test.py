import csv
import io
import unittest

from nacc.uds3 import filters


class TestFilters(unittest.TestCase):

    def test_filter_clean_ptid_removes_visits_in_nacc_current(self):
        '''
        `filter_clean_ptid` should remove visit data that is already in NACC's
        Current database.
        '''

        subjects = '''
Patient ID,Packet type,Visit Num,Status
110001,I,001,Current
110002,I,001,Working
110003,F,002,Current
110004,F,002,Working
'''.strip()

        redcap_data = '''
ptid,redcap_event_name,formver,adcid,visitmo,visitday,visityr,visitnum,initials,header_complete
110001,initial_visit_year_arm_1,3,99,1,1,2019,001,ABC,2
110002,initial_visit_year_arm_1,3,99,1,1,2019,001,ABC,2
110003,followup_visit_yea_arm_1,3,99,1,1,2019,002,ABC,2
110004,followup_visit_yea_arm_1,3,99,1,1,2019,002,ABC,2
'''.strip()

        actual = []
        with io.StringIO(redcap_data) as data, \
                io.StringIO("") as results, \
                io.StringIO(subjects) as nacc_packet_file:

            filters.filter_clean_ptid_do(data, nacc_packet_file, results)

            # Reset the file position indicator so DictReader reads from the
            # beginning of the results "file".
            results.seek(0)
            reader = csv.DictReader(results)
            for row in reader:
                actual.append(row['ptid'])

        expected = ['110002', '110004']
        self.assertListEqual(actual, expected)
