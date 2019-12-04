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
110005,I,001,Certified
'''.strip()

        redcap_data = '''
ptid,redcap_event_name,formver,adcid,visitmo,visitday,visityr,visitnum,initials,header_complete
110001,initial_visit_year_arm_1,3,99,1,1,2019,001,ABC,2
110002,initial_visit_year_arm_1,3,99,1,1,2019,001,ABC,2
110003,followup_visit_yea_arm_1,3,99,1,1,2019,002,ABC,2
110004,followup_visit_yea_arm_1,3,99,1,1,2019,002,ABC,2
110005,initial_visit_year_arm_1,3,99,1,1,2019,001,ABC,2
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

    def test_filter_eliminate_empty_date(self):
        '''
        `filter_eliminate_empty_date` should remove data with
        no visit date.
        '''

        redcap_data = '''
ptid,redcap_event_name,formver,adcid,visitmo,visitday,visityr,visitnum,initials,header_complete
110001,initial_visit_year_arm_1,3,99,1,1,,001,ABC,2
110002,initial_visit_year_arm_1,3,99,1,1,2019,001,ABC,2
110003,followup_visit_yea_arm_1,3,99,,1,2019,002,ABC,2
110004,followup_visit_yea_arm_1,3,99,1,1,2019,002,ABC,2
'''.strip()

        actual = []
        with io.StringIO(redcap_data) as data, \
                io.StringIO("") as results:
            filters.filter_eliminate_empty_date(data, '', results)

            results.seek(0)
            reader = csv.DictReader(results)
            for row in reader:
                actual.append(row['ptid'])

        expected = ['110002', '110004']
        self.assertListEqual(actual, expected)

    def test_filter_remove_ptid(self):
        '''
        `filter_remove_ptid' should remove and keep ptid from
        meta file (nacculator_cfg.ini)
        '''
        filter_diction = {
            'ptid_format': '11\\d.*',
            'bad_ptid': '110002,110004',
            'good_ptid': '1600-A'
        }
        redcap_data = '''
ptid,redcap_event_name,formver,adcid,visitmo,visitday,visityr,visitnum,initials,header_complete
1600-A,initial_visit_year_arm_1,3,99,1,1,2019,001,ABC,2
110001,initial_visit_year_arm_1,3,99,1,1,2019,001,ABC,2
110002,initial_visit_year_arm_1,3,99,1,1,2019,001,ABC,2
110003,followup_visit_yea_arm_1,3,99,1,1,2019,002,ABC,2
110004,followup_visit_yea_arm_1,3,99,1,1,2019,002,ABC,2
'''.strip()

        actual = []
        with io.StringIO(redcap_data) as data, \
                io.StringIO("") as results:
            filters.filter_remove_ptid_do(data, filter_diction, results)

            results.seek(0)
            reader = csv.DictReader(results)
            for row in reader:
                actual.append(row['ptid'])

        expected = ['1600-A', '110001', '110003']
        self.assertListEqual(actual, expected)

    def test_filter_fix_vistdate(self):
        '''
        `filter_fix_visitdate` should turn string to int if
        filled and does nothing if blank.
        '''
        redcap_data = '''
ptid,redcap_event_name,formver,adcid,visitmo,visitday,visityr,visitnum,initials,header_complete
110001,initial_visit_year_arm_1,3,99,1,1,2019,,ABC,2
110002,initial_visit_year_arm_1,3,99,1,1,2019,001,ABC,2
110003,followup_visit_yea_arm_1,3,99,1,1,2019,,ABC,2
110004,followup_visit_yea_arm_1,3,99,1,1,2019,002,ABC,2
'''.strip()
        actual = []
        with io.StringIO(redcap_data) as data, \
                io.StringIO("") as results:
            filters.filter_fix_visitdate(data, '', results)

            results.seek(0)
            reader = csv.DictReader(results)
            for row in reader:
                actual.append(row['visitnum'])
        expected = ['', '1', '', '2']
        self.assertListEqual(actual, expected)

    def test_filter_fill_default(self):
        '''
        `filter_fill_default` should fill out blanks for
        a specific col with defualt.
        '''
        fill_default_values = {'adcid': 41, 'formver': 3}  # in filters.py

        redcap_data = '''
ptid,redcap_event_name,formver,adcid,visitmo,visitday,visityr,visitnum,initials,header_complete
110001,initial_visit_year_arm_1,,,1,1,2019,001,ABC,2
110002,initial_visit_year_arm_1,2,99,1,1,2019,001,ABC,2
110001,followup_visit_yea_arm_1,2,,1,1,2019,002,ABC,2
110002,followup_visit_yea_arm_1,,99,1,1,2019,002,ABC,2
'''.strip()
        actual_adcid = []
        actual_formver = []
        with io.StringIO(redcap_data) as data, \
                io.StringIO("") as results:
            filters.fill_value_of_fields(data, results, fill_default_values,
                                         defaultCheck=True)

            results.seek(0)
            reader = csv.DictReader(results)
            for row in reader:
                actual_adcid.append(row['adcid'])
                actual_formver.append(row['formver'])
        expected_adcid = ['41', '99', '41', '99']
        expected_formver = ['3', '2', '2', '3']
        self.assertEqual(actual_adcid, expected_adcid)
        self.assertEqual(actual_formver, expected_formver)

    def test_filter_update_field(self):
        '''
        `filter_fill_default` should update feild value if feild has value
        and leave blanks blank.
        '''

        fill_non_blank_values = {'adcid': '41'}

        redcap_data = '''
ptid,redcap_event_name,formver,adcid,visitmo,visitday,visityr,visitnum,initials,header_complete
110001,initial_visit_year_arm_1,3,,1,1,2019,001,ABC,2
110002,initial_visit_year_arm_1,3,2,1,1,2019,001,ABC,2
110001,followup_visit_yea_arm_1,3,,1,1,2019,002,ABC,2
110002,followup_visit_yea_arm_1,3,99,1,1,2019,002,ABC,2
'''.strip()
        actual = []
        with io.StringIO(redcap_data) as data, \
                io.StringIO("") as results:
            filters.fill_value_of_fields(data, results, fill_non_blank_values,
                                         blankCheck=True)

            results.seek(0)
            reader = csv.DictReader(results)
            for row in reader:
                actual.append(row['adcid'])
        expected = ['', '41', '', '41']
        self.assertEqual(actual, expected)

# Next 4 filters are sub filters of filter_extract_ptid
    def test_filter_csv_vnum(self):
        '''
        `filter_csv_vnum` should return records of matching input ptid
        and visit number.
        '''
        Ptid = '110001'
        visit_num = '1'
        redcap_data = '''
ptid,redcap_event_name,formver,adcid,visitmo,visitday,visityr,visitnum,initials,header_complete
110001,initial_visit_year_arm_1,3,99,1,1,2019,001,ABC,2
110002,initial_visit_year_arm_1,3,99,1,1,2019,001,ABC,2
110001,followup_visit_yea_arm_1,3,99,1,1,2019,002,ABC,2
110002,followup_visit_yea_arm_1,3,99,1,1,2019,002,ABC,2
110001,followup_visit_yea_arm_1,3,99,1,1,2019,001,ABC,2
110001,followup_visit_yea_arm_1,3,99,1,1,2019,002,ABC,2
'''.strip()
        actual = []
        with io.StringIO(redcap_data) as data, \
                io.StringIO("") as results:

            reader = csv.DictReader(data)
            output = csv.DictWriter(results, None)
            filters.write_headers(reader, output)
            filtered = filter(lambda row: filters.filter_csv_vnum(Ptid, visit_num, row), reader)
            output.writerows(filtered)
            results.seek(0)
            reader = csv.DictReader(results)
            for row in reader:
                actual.append(row['ptid'])
        expected = ['110001', '110001']
        self.assertListEqual(actual, expected)

    def test_filter_csv_all(self):
        '''
        `filter_csv_all` should return records of mathcing
        ptid, visit number and vistit type
        '''
        Ptid = '110001'
        visit_num = '1'
        visit_type = 'initial_visit_year_arm_1'
        redcap_data = '''
ptid,redcap_event_name,formver,adcid,visitmo,visitday,visityr,visitnum,initials,header_complete
110001,initial_visit_year_arm_1,3,99,1,1,2019,001,ABC,2
110002,initial_visit_year_arm_1,3,99,1,1,2019,001,ABC,2
110001,followup_visit_yea_arm_1,3,99,1,1,2019,002,ABC,2
110002,followup_visit_yea_arm_1,3,99,1,1,2019,002,ABC,2
110001,initial_visit_year_arm_1,3,99,1,1,2019,001,ABC,2
'''.strip()
        actual = []
        with io.StringIO(redcap_data) as data, \
                io.StringIO("") as results:

            reader = csv.DictReader(data)
            output = csv.DictWriter(results, None)
            filters.write_headers(reader, output)
            filtered = filter(lambda row: filters.filter_csv_all(Ptid, visit_num, visit_type, row), reader)
            output.writerows(filtered)
            results.seek(0)
            reader = csv.DictReader(results)
            for row in reader:
                actual.append(row['ptid'])
        expected = ['110001', '110001']
        self.assertListEqual(actual, expected)

    def test_filter_vtype(self):
        '''
        `filter_csv_vtype` should return records of mathcing
        ptid and vistit type
        '''
        Ptid = '110002'
        visit_type = 'initial_visit_year_arm_1'
        redcap_data = '''
ptid,redcap_event_name,formver,adcid,visitmo,visitday,visityr,visitnum,initials,header_complete
110001,initial_visit_year_arm_1,3,99,1,1,2019,001,ABC,2
110002,initial_visit_year_arm_1,3,99,1,1,2019,001,ABC,2
110001,followup_visit_yea_arm_1,3,99,1,1,2019,002,ABC,2
110002,followup_visit_yea_arm_1,3,99,1,1,2019,002,ABC,2
110002,initial_visit_year_arm_1,3,99,1,1,2019,002,ABC,2
'''.strip()
        actual = []
        with io.StringIO(redcap_data) as data, \
                io.StringIO("") as results:

            reader = csv.DictReader(data)
            output = csv.DictWriter(results, None)
            filters.write_headers(reader, output)
            filtered = filter(lambda row: filters.filter_csv_vtype(Ptid, visit_type, row), reader)
            output.writerows(filtered)
            results.seek(0)
            reader = csv.DictReader(results)
            for row in reader:
                actual.append(row['ptid'])
        expected = ['110002', '110002']
        self.assertListEqual(actual, expected)

    def test_filter_ptid(self):
        '''
        `filter_csv_ptid` should return records of mathcing
        ptid.
        '''
        Ptid = '110001'
        redcap_data = '''
ptid,redcap_event_name,formver,adcid,visitmo,visitday,visityr,visitnum,initials,header_complete
110001,initial_visit_year_arm_1,3,99,1,1,2019,001,ABC,2
110002,initial_visit_year_arm_1,3,99,1,1,2019,001,ABC,2
110001,followup_visit_yea_arm_1,3,99,1,1,2019,002,ABC,2
110002,followup_visit_yea_arm_1,3,99,1,1,2019,002,ABC,2
110001,in_person_home_visit,3,99,1,1,2019,002,ABC,2
'''.strip()
        actual = []
        with io.StringIO(redcap_data) as data, \
                io.StringIO("") as results:
            reader = csv.DictReader(data)
            output = csv.DictWriter(results, None)
            filters.write_headers(reader, output)
            filtered = filter(lambda row: filters.filter_csv_ptid(Ptid, row), reader)
            output.writerows(filtered)
            results.seek(0)
            reader = csv.DictReader(results)
            for row in reader:
                actual.append(row['ptid'])
        expected = ['110001', '110001', '110001']
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
        with io.StringIO(redcap_data) as data, \
                io.StringIO("") as results:
                
            filters.filter_fix_headers_do(data, fix_header_dict, results)

        # Reset the file position indicator so DictReader reads from the
        # beginning of the results "file".
        
            results.seek(0)
            reader = csv.reader(results)
            actual = next(reader)
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
        with io.StringIO(redcap_data) as data, \
                io.StringIO("") as results:

            filters.filter_replace_drug_id(data,'', results)

            # Reset the file position indicator so DictReader reads from the
            # beginning of the results "file".
            results.seek(0)
            reader = csv.DictReader(results)
            for row in reader:
                filter_out_1.append(row['fu_drugid_4'])
                filter_out_2.append(row['drugid_3'])

        expected_1 = ['d00002', '', '', 'd00001']
        self.assertListEqual(filter_out_1, expected_1)
        expected_2 = ['d11111', 'd22222', 'd22222', '']
        self.assertListEqual(filter_out_2, expected_2)