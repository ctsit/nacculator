import unittest
import csv
import re
import sys
import argparse

from nacc import redcap2nacc
from nacc.ftld import blanks
from nacc.ftld.ivp import builder as ftld_ivp_builder
from nacc.ftld.fvp import builder as ftld_fvp_builder


class option():
    flag = 'ftld'
    iorf = 'ivp'
    lbd = False
    ftld = True
    ivp = True
    fvp = False

class TestBlankRulesForFTLD(unittest.TestCase):


    # The index numbers get so large because check_blanks is appending EVERY rule in the field to each warning. Is there a way for the blanks program to only return the specific rule that was violated?

    ''' 
    These tests are designed to take ivp data from the ftld_ivp_unittest_sample.csv file in "test_data_for_nacculator" on Samantha's computer. It is just to see if the custom blanking rules in the (currently new) FTLD module are working correctly.
    '''

    def setUp(self):
        fp = open('data.csv')
        reader = csv.DictReader(fp)
        for record in reader:
            self.packet = ftld_ivp_builder.build_uds3_ftld_ivp_form(record)
        self.options = option()


    def test_blanks_working(self):
        discovered = redcap2nacc.check_blanks(self.packet,self.options)
        self.assertIsNotNone(discovered)


    def test_for_filled_when_ruled_blank(self):
        # Have it look for the langa4 error in ptid 1 (without returning an error in ptid 2)
        fp = open('data.csv')
        reader = csv.DictReader(fp)
        for record in reader:
            self.packet = ftld_ivp_builder.build_uds3_ftld_ivp_form(record)
            warnings = redcap2nacc.check_blanks(self.packet,self.options)
            if record['ptid']=='1':
                self.assertEqual(warnings[0], "'LANGA4' is '1' with length '1', but should be blank: 'Blank if Question 4b A4SUB = 0 (No)'.")
            elif record['ptid']=='2':
                self.assertEqual(warnings,[])
            else: raise ValueError("Test \'filled when ruled blank\' isn't right bud")
        fp.close()


    def test_for_special_case_FTDCPC2F(self):
        # One packet of questions should be left blank if FTDCPC2F has a value (anything between 95-98)
        fp = open('data.csv')
        reader = csv.DictReader(fp)
        for record in reader:
            self.packet = ftld_ivp_builder.build_uds3_ftld_ivp_form(record)
            warnings = redcap2nacc.check_blanks(self.packet,self.options)
            if record['ptid']=='1':
                self.assertEqual(warnings[6], "'FTDhAIRD' is '1' with length '1', but should be blank: 'Blank if Question 0 FTDCPC2F = 95'.")
            elif record['ptid']=='2':
                self.assertEqual(warnings,[])
            else: raise ValueError("Test \'FTDCPC2F\' isn't right bud")
        fp.close()


    def test_for_special_case_or2(self):
        # Have it make sure _blanking_rule_ftld_or2 works properly (and by extension or3, or4, and or5) - This blanking rule depends on either of two possible answers to questions, along with regular blanking rules
        fp = open('data.csv')
        reader = csv.DictReader(fp)
        for record in reader:
            self.packet = ftld_ivp_builder.build_uds3_ftld_ivp_form(record)
            warnings = redcap2nacc.check_blanks(self.packet,self.options)
            if record['ptid']=='1':
                self.assertEqual(warnings[105], "'FTDMRIRF' is '0' with length '1', but should be blank: 'Blank if Question 1 FTDIDIAG = 0 (No)'.")
            elif record['ptid']=='2':
                self.assertEqual(warnings,[])
            else: raise ValueError("Test \'or2\' isn't right bud")
        fp.close()


    def test_for_special_case_FTDMRIOS(self):
        # Have it make sure _blanking_rule_ftld_or2a works properly (and by extension or3a, or4a, and or5a) - This blanking rule has an extra condition added to the or2 rules (packet['FTDMRIOB'] != 1)
        fp = open('data.csv')
        reader = csv.DictReader(fp)
        for record in reader:
            self.packet = ftld_ivp_builder.build_uds3_ftld_ivp_form(record)
            warnings = redcap2nacc.check_blanks(self.packet,self.options)
            if record['ptid']=='1':
                self.assertEqual(warnings[135], "'FTDMRIOS' is '1                                                           ' with length '60', but should be blank: 'Blank if Question 2a11 FTDMRIOB ne 1 (Yes)'.")
            elif record['ptid']=='2':
                self.assertEqual(warnings,[])
            else: raise ValueError("Test \'or2a\' isn't right bud")
        fp.close()


    def test_for_special_case_FTDPABVF(self):
        # Have it make sure _blanking_rule_for_others_left_blank is working by checking both 0 and False instances (it will skip if either of these is the case for two questions)
        fp = open('data.csv')
        reader = csv.DictReader(fp)
        for record in reader:
            self.packet = ftld_ivp_builder.build_uds3_ftld_ivp_form(record)
            warnings = redcap2nacc.check_blanks(self.packet,self.options)
            if record['ptid']=='1':
                self.assertEqual(warnings[2], "'FTDPABVF' is '9' with length '1', but should be blank: 'Blank if Question 12 FTDCPPA = 0 (No) '.")
                self.assertEqual(warnings[5], "'FTDPABVF' is '9' with length '1', but should be blank: 'Blank if Question 22 FTDBVFT = blank'.")
            elif record['ptid']=='2':
                self.assertEqual(warnings,[])
            else: raise ValueError("Test \'FTDPABVF\' isn't right bud")
        fp.close()



if __name__ == "__main__":
    unittest.main()