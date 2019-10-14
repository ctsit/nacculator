#!/usr/bin/env python3

###############################################################################
# Copyright 2015-2016 University of Florida. All rights reserved.
# This file is part of UF CTS-IT's NACCulator project.
# Use of this source code is governed by the license found in the LICENSE file.
###############################################################################
import nacc.uds3

### BEGIN non-generated code
# WARNING: When generating new forms, do not overwrite this section
from datetime import date

# WARNING: When generating new forms, use CURRENT_YEAR instead of "CURRENT_YEAR"
# WARNING: When generating new forms, use CURRENT_YEAR-15 instead of "1999"
CURRENT_YEAR = date.today().year

### END non-generated code







class FVP_FormB1L(nacc.uds3.Field):
    def __init__(self):
        self.fields = header_fields()
        self.fields['LBSSALiV'] = nacc.uds3.Field(name='LBSSALiV', typename='Num', position=(45, 45), length=1, inclusive_range=(0, 1), allowable_values=['0', '1', '9'], blanks=[])
        self.fields['LBSSWALL'] = nacc.uds3.Field(name='LBSSWALL', typename='Num', position=(47, 47), length=1, inclusive_range=(0, 1), allowable_values=['0', '1', '9'], blanks=[])
        self.fields['LBSiNSeX'] = nacc.uds3.Field(name='LBSiNSeX', typename='Num', position=(49, 49), length=1, inclusive_range=(0, 1), allowable_values=['0', '1', '9'], blanks=[])
        self.fields['LBSPrSeX'] = nacc.uds3.Field(name='LBSPrSeX', typename='Num', position=(51, 51), length=1, inclusive_range=(0, 1), allowable_values=['0', '1', '9'], blanks=[])
        self.fields['LBSWeiGH'] = nacc.uds3.Field(name='LBSWeiGH', typename='Num', position=(53, 53), length=1, inclusive_range=(0, 1), allowable_values=['0', '1', '9'], blanks=[])
        self.fields['LBSSMeLL'] = nacc.uds3.Field(name='LBSSMeLL', typename='Num', position=(55, 55), length=1, inclusive_range=(0, 1), allowable_values=['0', '1', '9'], blanks=[])
        self.fields['LBSSWeAt'] = nacc.uds3.Field(name='LBSSWeAt', typename='Num', position=(57, 57), length=1, inclusive_range=(0, 1), allowable_values=['0', '1', '9'], blanks=[])
        self.fields['LBStoLCD'] = nacc.uds3.Field(name='LBStoLCD', typename='Num', position=(59, 59), length=1, inclusive_range=(0, 1), allowable_values=['0', '1', '9'], blanks=[])
        self.fields['LBStoLHt'] = nacc.uds3.Field(name='LBStoLHt', typename='Num', position=(61, 61), length=1, inclusive_range=(0, 1), allowable_values=['0', '1', '9'], blanks=[])
        self.fields['LBSDBViS'] = nacc.uds3.Field(name='LBSDBViS', typename='Num', position=(63, 63), length=1, inclusive_range=(0, 1), allowable_values=['0', '1', '9'], blanks=[])
        self.fields['LBSCoNSt'] = nacc.uds3.Field(name='LBSCoNSt', typename='Num', position=(65, 65), length=1, inclusive_range=(0, 1), allowable_values=['0', '1'], blanks=[])
        self.fields['LBSHDStL'] = nacc.uds3.Field(name='LBSHDStL', typename='Num', position=(67, 67), length=1, inclusive_range=(0, 1), allowable_values=['0', '1', '9'], blanks=[])
        self.fields['LBSLSStL'] = nacc.uds3.Field(name='LBSLSStL', typename='Num', position=(69, 69), length=1, inclusive_range=(0, 1), allowable_values=['0', '1', '9'], blanks=[])
        self.fields['LBSUBLAD'] = nacc.uds3.Field(name='LBSUBLAD', typename='Num', position=(71, 71), length=1, inclusive_range=(0, 1), allowable_values=['0', '1', '9'], blanks=[])
        self.fields['LBSUStrM'] = nacc.uds3.Field(name='LBSUStrM', typename='Num', position=(73, 73), length=1, inclusive_range=(0, 1), allowable_values=['0', '1', '9'], blanks=[])
        self.fields['LBSUPASS'] = nacc.uds3.Field(name='LBSUPASS', typename='Num', position=(75, 75), length=1, inclusive_range=(0, 1), allowable_values=['0', '1', '9'], blanks=[])
        self.fields['LBSDZStU'] = nacc.uds3.Field(name='LBSDZStU', typename='Num', position=(77, 77), length=1, inclusive_range=(0, 1), allowable_values=['0', '1', '9'], blanks=[])
        self.fields['LBSDZStN'] = nacc.uds3.Field(name='LBSDZStN', typename='Num', position=(79, 79), length=1, inclusive_range=(0, 1), allowable_values=['0', '1', '9'], blanks=[])
        self.fields['LBSFAiNt'] = nacc.uds3.Field(name='LBSFAiNt', typename='Num', position=(81, 81), length=1, inclusive_range=(0, 1), allowable_values=['0', '1', '9'], blanks=[])
        self.fields['LBSPSyM'] = nacc.uds3.Field(name='LBSPSyM', typename='Num', position=(83, 84), length=2, inclusive_range=(0, 19), allowable_values=['0 = Provided at previous visit\n1 = Dribbling saliva during the day 2 = Difficulty swallowing\n3 = Altered interest in sex 4 = Problems having sex\n5 = Recent change in weight not related to dieting\n6 = Change in ability to taste or smell 7 = Excessive sweating\n8 = Difficulty tolerating cold weather 9 = Difficulty tolerating hot weather 10 = Double vision\n11 = Constipation\n12 = Straining to pass hard stools 13 = Involuntary loss of stools\n14 = Feeling after passing urine that bladder is not completely empty\n15 = Stream of urine is weak or reduced 16 = Passing urine within two hours of\nprevious urination\n17 = Feeling light-headed or dizzy when standing up\n18 = Feeling light-headed after stand- ing for some time\n19 = Fainting\n88 = Not applicable– never experienced any of these symptoms\n99 = Unknown', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10 (0-19 and then 88)'], blanks=[])
        self.fields['LBPSyAGe'] = nacc.uds3.Field(name='LBPSyAGe', typename='Num', position=(86, 88), length=3, inclusive_range=(15, 110), allowable_values=[], blanks=[])
        self.fields['LBSSUPSy'] = nacc.uds3.Field(name='LBSSUPSy', typename='Num', position=(90, 92), length=3, inclusive_range=(65, 230), allowable_values=[], blanks=[])
        self.fields['LBSSUPDi'] = nacc.uds3.Field(name='LBSSUPDi', typename='Num', position=(94, 96), length=3, inclusive_range=(25, 140), allowable_values=[], blanks=[])
        self.fields['LBSSUPHt'] = nacc.uds3.Field(name='LBSSUPHt', typename='Num', position=(98, 100), length=3, inclusive_range=(20, 160), allowable_values=[], blanks=[])
        self.fields['LBSStNSy'] = nacc.uds3.Field(name='LBSStNSy', typename='Num', position=(102, 104), length=3, inclusive_range=(50, 240), allowable_values=[], blanks=[])
        self.fields['LBSStNDi'] = nacc.uds3.Field(name='LBSStNDi', typename='Num', position=(106, 108), length=3, inclusive_range=(20, 150), allowable_values=[], blanks=[])
        self.fields['LBSStNHt'] = nacc.uds3.Field(name='LBSStNHt', typename='Num', position=(110, 112), length=3, inclusive_range=(33, 180), allowable_values=[], blanks=[])
        self.fields['LBSAGerM'] = nacc.uds3.Field(name='LBSAGerM', typename='Num', position=(114, 116), length=3, inclusive_range=(15, 110), allowable_values=[], blanks=[])
        self.fields['LBSAGeSM'] = nacc.uds3.Field(name='LBSAGeSM', typename='Num', position=(118, 120), length=3, inclusive_range=(15, 110), allowable_values=[], blanks=[])
        self.fields['LBSAGeGt'] = nacc.uds3.Field(name='LBSAGeGt', typename='Num', position=(122, 124), length=3, inclusive_range=(9, 110), allowable_values=[], blanks=[])
        self.fields['LBSAGeFL'] = nacc.uds3.Field(name='LBSAGeFL', typename='Num', position=(126, 128), length=3, inclusive_range=(9, 110), allowable_values=[], blanks=[])
        self.fields['LBSAGetr'] = nacc.uds3.Field(name='LBSAGetr', typename='Num', position=(130, 132), length=3, inclusive_range=(9, 110), allowable_values=[], blanks=[])
        self.fields['LBSAGeBr'] = nacc.uds3.Field(name='LBSAGeBr', typename='Num', position=(134, 136), length=3, inclusive_range=(9, 110), allowable_values=[], blanks=[])
        self.fields['LBSSCLAU'] = nacc.uds3.Field(name='LBSSCLAU', typename='Num', position=(138, 138), length=1, inclusive_range=(0, 1), allowable_values=['0', '1'], blanks=[])
        self.fields['LBSSCLVr'] = nacc.uds3.Field(name='LBSSCLVr', typename='Num', position=(140, 140), length=1, inclusive_range=(1, 2), allowable_values=['1', '2', '8'], blanks=['Blank if Question 34 LBSSCLAU = 0 (No)'])
        self.fields['LBSSCLot'] = nacc.uds3.Field(name='LBSSCLot', typename='Char', position=(142, 171), length=30, inclusive_range=None, allowable_values=['Any text or numbers with the exception of single quotes (‘), double quotes (“), ampersands (&), or percentage signs (%).'], blanks=['Blank if Question 34 LBSSCLAU= 0 (No) or Question 34a LBSSCLVR ≠ 8 (Other)'])
        self.fields['LBSSCor'] = nacc.uds3.Field(name='LBSSCor', typename='Num', position=(173, 175), length=3, inclusive_range=(0, 998), allowable_values=[], blanks=[])