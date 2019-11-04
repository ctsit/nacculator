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



class TestBlankRulesForFTLD(unittest.TestCase):

    def setUp(self):
        # Change the commented argument whenever you want to swap between ivp and fvp
        self.packet = ftld_ivp_builder.build_uds3_ftld_ivp_form
        # self.packet = ftld_fvp_builder.build_uds3_ftld_fvp_form
        self.options = option()
        self.fp = open('data.csv')

    def test_blanks_working(self):
        noerrors = redcap2nacc.check_blanks(self.packet,self.options)
        self.assertTrue(noerrors)











if __name__ == "__main__":
    unittest.main()