import csv
import io
import os
import tempfile
import unittest

from nacc.uds3 import filters

class TestFilters(unittest.TestCase):

    def test_ptid_not_current_in_NACC(self):
        ''' Visits already in NACC's Current db should be filtered '''
        subj_list, subj_list_name = make_subj_list()
        config, config_name = make_config(subj_list_name)
        data = make_data_file()
        output_file = io.BytesIO()

        with open(subj_list_name, 'a') as subj_f:
            sbj_writer = csv.writer(subj_f, delimiter=',')
            sbj_writer.writerow(['110001', 'I', '001', 'Current'])
            sbj_writer.writerow(['110002', 'I', '001', 'Working'])
            sbj_writer.writerow(['110003', 'F', '002', 'Current'])
            sbj_writer.writerow(['110004', 'F', '002', 'Working'])

        data_writer = csv.writer(data, delimiter=',', quotechar='"')
        data_writer.writerow(['110001', 'initial_visit_year_arm_1', '3',
                              '99', '1', '1', '2019', '001', 'ABC', '2'])
        data_writer.writerow(['110002', 'initial_visit_year_arm_1', '3',
                              '99', '1', '1', '2019', '001', 'ABC', '2'])
        data_writer.writerow(['110003', 'followup_visit_yea_arm_1', '3', 
                              '99', '1', '1', '2019', '002', 'ABC', '2'])
        data_writer.writerow(['110004', 'followup_visit_yea_arm_1', '3',
                              '99', '1', '1', '2019', '002', 'ABC', '2'])
        data.seek(0)

        try:
            filters.filter_clean_ptid(data, config_name, output_file)
            surviving_ids = []
            expected_ids = ['110002', '110004']
            output_file.seek(0)
            output_reader = csv.DictReader(output_file)
            for row in output_reader:
                surviving_ids.append(row['ptid'])
            self.assertListEqual(surviving_ids, expected_ids)
        finally:
            os.close(subj_list)
            os.remove(subj_list_name)
            os.close(config)
            os.remove(config_name)


def make_subj_list():
    ''' This csv mimics the one pulled from the NACC website.
        It shows which visits are in the Current or Working directory.'''
    subj_list, subj_list_name = tempfile.mkstemp(suffix='.csv')
    with open(subj_list_name, "w") as f:
        writer= csv.writer(f, delimiter=',')
        writer.writerow(['Patient ID', 'Packet type', 'Visit Num', 'Status'])
    return subj_list, subj_list_name


def make_config(subj_list_name=None):
    config, config_name = tempfile.mkstemp()
    with open(config_name, 'w') as conf_f:
        conf_f.write('[DEFAULT]\n')
        conf_f.write('\n[filter_clean_ptid]\n')
        conf_f.write('filepath: ' + subj_list_name + '\n')
        conf_f.write('\n[filter_remove_ptid]\n')
        conf_f.write('ptid_format: 11\d.*\n')
    return config, config_name


def make_data_file():
    data = io.BytesIO()
    writer = csv.writer(data, delimiter=',', quotechar='"')
    writer.writerow(['ptid','redcap_event_name','formver',
                     'adcid','visitmo','visitday','visityr',
                     'visitnum','initials','header_complete'])
    return data
