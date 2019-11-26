###############################################################################
# Copyright 2015-2019 University of Florida. All rights reserved.
# This file is part of UF CTS-IT's NACCulator project.
# Use of this source code is governed by the license found in the LICENSE file.
###############################################################################

import nacc.uds3

### BEGIN non-generated code
# WARNING: When generating new forms, do not overwrite this section
from datetime import date

# WARNING: When generating new forms, use CURRENT_YEAR instead of "2014"
# WARNING: When generating new forms, use CURRENT_YEAR-15 instead of "1999"
CURRENT_YEAR = date.today().year

### END non-generated code


def header_fields():
    fields = {}
    fields['ADCID'] = nacc.uds3.Field(name='ADCID', typename='Num', position=(1, 2), length=2, inclusive_range=('2', '43'), allowable_values=[], blanks=[])
    fields['PTID'] = nacc.uds3.Field(name='PTID', typename='Char', position=(4, 13), length=10, inclusive_range=None, allowable_values=[], blanks=[])
    fields['VISITMO'] = nacc.uds3.Field(name='VISITMO', typename='Num', position=(15, 16), length=2, inclusive_range=('1', '12'), allowable_values=[], blanks=[])
    fields['VISITDAY'] = nacc.uds3.Field(name='VISITDAY', typename='Num', position=(18, 19), length=2, inclusive_range=('1', '31'), allowable_values=[], blanks=[])
    fields['VISITYR'] = nacc.uds3.Field(name='VISITYR', typename='Num', position=(21, 24), length=4, inclusive_range=('2012', str(CURRENT_YEAR)), allowable_values=[], blanks=[])
    fields['CSFLPMO'] = nacc.uds3.Field(name='CSFLPMO', typename='Num', position=(26, 27), length=2, inclusive_range=('1', '12'), allowable_values=[], blanks=[])
    fields['CSFLPDY'] = nacc.uds3.Field(name='CSFLPDY', typename='Num', position=(29, 30), length=2, inclusive_range=('1', '31'), allowable_values=[], blanks=[])
    fields['CSFLPYR'] = nacc.uds3.Field(name='CSFLPYR', typename='Num', position=(32, 35), length=4, inclusive_range=('1980', '2019'), allowable_values=[], blanks=[])
    fields['CSFINIT'] = nacc.uds3.Field(name='CSFINIT', typename='Char', position=(37, 39), length=3, inclusive_range=None, allowable_values=[], blanks=[])
    return fields


class FormEE2(nacc.uds3.FieldBag):
    """ 
    Generated from Form eE2: https://www.alz.washington.edu/WEB/csfded.pdf
    """
    def __init__(self):
        self.fields = header_fields()
        self.fields['CSFABETA'] = nacc.uds3.Field(name='CSFABETA', typename='Num', position=(41, 48), length=8, inclusive_range=('1', '2000'), allowable_values=[], blanks=['Question 1a CSFABETA is an optional data field and may be left blank.'])
        self.fields['CSFABmo'] = nacc.uds3.Field(name='CSFABmo', typename='Num', position=(50, 51), length=2, inclusive_range=('1', '12'), allowable_values=[], blanks=['Blank if Question 1a CSFABETA = blank'])
        self.fields['CSFABDY'] = nacc.uds3.Field(name='CSFABDY', typename='Num', position=(53, 54), length=2, inclusive_range=('1', '31'), allowable_values=[], blanks=['Blank if Question 1a CSFABETA = blank'])
        self.fields['CSFABYr'] = nacc.uds3.Field(name='CSFABYr', typename='Num', position=(56, 59), length=4, inclusive_range=('1980', '2019'), allowable_values=[], blanks=['Blank if Question 1a CSFABETA = blank'])
        self.fields['CSFABmD'] = nacc.uds3.Field(name='CSFABmD', typename='Num', position=(61, 61), length=1, inclusive_range=None, allowable_values=['1', '2', '8'], blanks=['Blank if Question 1a CSFABETA = blank'])
        self.fields['CSFABmDX'] = nacc.uds3.Field(name='CSFABmDX', typename='Char', position=(63, 122), length=60, inclusive_range=None, allowable_values=[], blanks=['Blank if Question 1e CSFABmD ne 8 (Other)', 'Blank if Question 1a CSFABETA = blank'])
        self.fields['CSFPTAU'] = nacc.uds3.Field(name='CSFPTAU', typename='Num', position=(124, 129), length=6, inclusive_range=('1', '500'), allowable_values=[], blanks=['Question 2a CSFPTAU is an optional data field and may be left blank.'])
        self.fields['CSFPTmo'] = nacc.uds3.Field(name='CSFPTmo', typename='Num', position=(131, 132), length=2, inclusive_range=('1', '12'), allowable_values=[], blanks=['Blank if Question 2a CSFPTAU = blank'])
        self.fields['CSFPTDY'] = nacc.uds3.Field(name='CSFPTDY', typename='Num', position=(134, 135), length=2, inclusive_range=('1', '31'), allowable_values=[], blanks=['Blank if Question 2a CSFPTAU = blank'])
        self.fields['CSFPTYr'] = nacc.uds3.Field(name='CSFPTYr', typename='Num', position=(137, 140), length=4, inclusive_range=('1980', '2019'), allowable_values=[], blanks=['Blank if Question 2a CSFPTAU = blank'])
        self.fields['CSFPTmD'] = nacc.uds3.Field(name='CSFPTmD', typename='Num', position=(142, 142), length=1, inclusive_range=None, allowable_values=['1', '2', '8'], blanks=['Blank if Question 2a CSFPTAU = blank'])
        self.fields['CSFPTmDX'] = nacc.uds3.Field(name='CSFPTmDX', typename='Char', position=(144, 203), length=60, inclusive_range=None, allowable_values=[], blanks=['Blank if Question 2e CSFPTmD ne 8 (Other)', 'Blank if Question 2a CSFPTAU = blank'])
        self.fields['CSFTTAU'] = nacc.uds3.Field(name='CSFTTAU', typename='Num', position=(205, 211), length=7, inclusive_range=('1', '2500'), allowable_values=[], blanks=['Question 3a CSFTTAU is an optional data field and may be left blank.'])
        self.fields['CSFTTmo'] = nacc.uds3.Field(name='CSFTTmo', typename='Num', position=(213, 214), length=2, inclusive_range=('1', '12'), allowable_values=[], blanks=['Blank if Question 3a CSFTTAU = blank'])
        self.fields['CSFTTDY'] = nacc.uds3.Field(name='CSFTTDY', typename='Num', position=(216, 217), length=2, inclusive_range=('1', '31'), allowable_values=[], blanks=['Blank if Question 3a CSFTTAU = blank'])
        self.fields['CSFTTYr'] = nacc.uds3.Field(name='CSFTTYr', typename='Num', position=(219, 222), length=4, inclusive_range=('1980', '2019'), allowable_values=[], blanks=['Blank if Question 3a CSFTTAU = blank'])
        self.fields['CSFTTmD'] = nacc.uds3.Field(name='CSFTTmD', typename='Num', position=(224, 224), length=1, inclusive_range=None, allowable_values=['1', '2', '8'], blanks=['Blank if Question 3a CSFTTAU = blank'])
        self.fields['CSFTTmDX'] = nacc.uds3.Field(name='CSFTTmDX', typename='Char', position=(226, 285), length=60, inclusive_range=None, allowable_values=[], blanks=['Blank if Question 3e CSFTTmD ne 8 (Other)', 'Blank if Question 3a CSFTTAU = blank'])
