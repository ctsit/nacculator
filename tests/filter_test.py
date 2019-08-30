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
        with io.BytesIO(redcap_data) as data, \
                io.BytesIO("") as results, \
                io.BytesIO(subjects) as nacc_packet_file:

            filters.filter_clean_ptid_do(data, nacc_packet_file, results)

            # Reset the file position indicator so DictReader reads from the
            # beginning of the results "file".
            results.seek(0)
            reader = csv.DictReader(results)
            for row in reader:
                actual.append(row['ptid'])

        expected = ['110002', '110004']
        self.assertListEqual(actual, expected)


        
    def test_filter_fix_headers(self):
        '''
        `filter_fix_headers` should change REDCap headers to NACC headers.
        '''
        
        redcap_data = '''
ptid,redcap_event_name,formver,adcid,visitmo,visitday,visityr,visitnum,initials,header_complete
110001,initial_visit_year_arm_1,3,99,1,1,2019,001,ABC,2
110002,initial_visit_year_arm_1,3,99,1,1,2019,001,ABC,2
110003,followup_visit_yea_arm_1,3,99,1,1,2019,002,ABC,2
110004,followup_visit_yea_arm_1,3,99,1,1,2019,002,ABC,2
'''.strip()
        
        fix_header_dict = {
            'ptid' : 'PTID',
            'visitmo' : 'VisitMo',
            'adcid' : 'ADCid',
            'initials' : 'Initials'
        }

        actual = []
        with io.BytesIO(redcap_data) as data, \
                io.BytesIO("") as results:
                
            filters.filter_fix_headers_do(data, fix_header_dict, results)

        # Reset the file position indicator so DictReader reads from the
        # beginning of the results "file".
        
            results.seek(0)
            reader = csv.reader(results)
            actual = reader.next()
        expected = ['PTID','redcap_event_name','formver','ADCid','VisitMo','visitday','visityr','visitnum','Initials','header_complete']
        self.assertListEqual(actual, expected)

 
    def test_filter_replace_drug_id(self):
        '''
        `test_filter_replace_drug_id` should replace drug id in the record, and print the processed ptid and number of updated fields.
        '''

        redcap_data = '''
ptid,redcap_event_name,formver,adcid,visitmo,visitday,visityr,visitnum,initials,header_complete,fu_drugid_4,drugid_3
110001,initial_visit_year_arm_1,3,99,1,1,2019,001,ABC,2,000002,111111
110002,initial_visit_year_arm_1,3,99,1,1,2019,001,ABC,2,,222222
110003,followup_visit_yea_arm_1,3,99,1,1,2019,002,ABC,2,,222222
110004,followup_visit_yea_arm_1,3,99,1,1,2019,002,ABC,2,000001,
'''.strip()

        filter_out_1 = []
        filter_out_2 = []
        with io.BytesIO(redcap_data) as data, \
                io.BytesIO("") as results:

            filters.filter_replace_drug_id(data,'', results)

            # Reset the file position indicator so DictReader reads from the
            # beginning of the results "file".
            results.seek(0)
            reader = csv.DictReader(results)
            for row in reader:
                filter_out_1.append(row['fu_drugid_4'])
                filter_out_2.append(row['drugid_3'])

        expected = ['d00002', '', '', 'd00001']
        self.assertListEqual(filter_out_1, expected)
        expected = ['d11111', 'd22222', 'd22222', '']
        self.assertListEqual(filter_out_2, expected)