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
        with io.BytesIO(redcap_data) as data, \
                io.BytesIO("") as results:
            filters.filter_eliminate_empty_date(data, '', results)

            # Reset the file position indicator so DictReader reads from the
            # beginning of the results "file".
            results.seek(0)
            reader = csv.DictReader(results)
            for row in reader:
                actual.append(row['ptid'])

        expected = ['110002', '110004']
        self.assertListEqual(actual, expected)

    @unittest.skip('Dictionary format wrong')
    def test_filter_remove_ptid(self):
        # TODO:also add the good ptid test as well
        '''
        `filter_remove_ptid' shopuld remove ptid from
        meta file (nacculator_cfg.ini)
        '''
        # problem making the dictionary right.
        filter_remove_ptid = '''
        ptid_format|bad_ptid|good_ptid
        11\d.*|110002,110004||
        '''.strip('|')

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
                io.BytesIO(filter_remove_ptid) as config:
            filters.filter_remove_ptid(data, config, results)

            # Reset the file position indicator so DictReader reads from the
            # beginning of the results "file".
            results.seek(0)
            reader = csv.DictReader(results)
            for row in reader:
                actual.append(row['ptid'])

        expected = ['110001', '110003']
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
        with io.BytesIO(redcap_data) as data, \
                io.BytesIO("") as results:
            filters.filter_fix_visitdate(data, '', results)
            # Reset the file position indicator so DictReader reads from the
            # beginning of the results "file".
            results.seek(0)
            reader = csv.DictReader(results)
            for row in reader:
                actual.append(row['visitnum'])
        expected = ['', '1', '', '2']
        self.assertListEqual(actual, expected)

    @unittest.skip('is already tested in filter_extract_ptid.')
    def test_filter_csv_vnum(self):
        '''
        `filter_csv_vnum` should return record of the input ptid
        and visit number given
        '''

        redcap_data = '''
ptid,redcap_event_name,formver,adcid,visitmo,visitday,visityr,visitnum,initials,header_complete
110001,initial_visit_year_arm_1,3,99,1,1,2019,001,ABC,2
110002,initial_visit_year_arm_1,3,99,1,1,2019,001,ABC,2
110001,followup_visit_yea_arm_1,3,99,1,1,2019,002,ABC,2
110002,followup_visit_yea_arm_1,3,99,1,1,2019,002,ABC,2
'''.strip()
        actual = []
        with io.BytesIO(redcap_data) as data, \
                io.BytesIO("") as results:

            # simulate other filters here### unneeded becuse in
            # filter_extract_ptid
            reader = csv.DictReader(data)
            output = csv.DictWriter(results, None)
            filters.write_headers(reader, output)
            for record in reader:
                if filters.filter_csv_vnum('110001', '002', record) is not None:
                    output.writerow(record)
            ##########
            results.seek(0)
            reader = csv.DictReader(results)
            for row in reader:
                actual.append(row['ptid'])
        expected = ['11001']
        self.assertListEqual(actual, expected)


    def test_filter_fill_default(self):
        '''
        `filter_fill_default` should...
        '''