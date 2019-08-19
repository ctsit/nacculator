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

def header_fields(): # may not need the headers. 
    fields = {}
    fields['PACKET'] = nacc.uds3.Field(name='PACKET', typename='Char', position=(1, 2), length=2, inclusive_range=None, allowable_values=[], blanks=[])
    fields['FORMID'] = nacc.uds3.Field(name='FORMID', typename='Char', position=(4, 6), length=3, inclusive_range=None, allowable_values=[], blanks=[])
    fields['FORMVER'] = nacc.uds3.Field(name='FORMVER', typename='Num', position=(8, 10), length=3, inclusive_range=(1, 3), allowable_values=[], blanks=[]) 
    fields['ADCID'] = nacc.uds3.Field(name='ADCID', typename='Num', position=(12, 13), length=2, inclusive_range=(2, 38), allowable_values=[], blanks=[])
    fields['PTID'] = nacc.uds3.Field(name='PTID', typename='Char', position=(15, 24), length=10, inclusive_range=None, allowable_values=[], blanks=[])
    fields['VISITMO'] = nacc.uds3.Field(name='VISITMO', typename='Num', position=(26, 27), length=2, inclusive_range=(1, 12), allowable_values=[], blanks=[])
    fields['VISITDAY'] = nacc.uds3.Field(name='VISITDAY', typename='Num', position=(29, 30), length=2, inclusive_range=(1, 31), allowable_values=[], blanks=[])
    fields['VISITYR'] = nacc.uds3.Field(name='VISITYR', typename='Num', position=(32, 35), length=4, inclusive_range=(2005, CURRENT_YEAR), allowable_values=[], blanks=[])
    fields['INITIALS'] = nacc.uds3.Field(name='INITIALS', typename='Char', position=(41, 43), length=3, inclusive_range=None, allowable_values=[], blanks=[])
    return fields

class FormM(nacc.uds3.FieldBag): 
    def __init__(self):
        self.fields = header_fields()
        self.fields['CHANGEMO'] = nacc.uds3.Field(name='CHANGEMO', typename='Num', position=(45,46), length=2, inclusive_range=(1, 12), allowable_values=['99'], blanks=['Blank if Question 4a DECEASED = 1 (Yes)', 'Blank if Question 4b DISCONT = 1 (Yes)'])
        self.fields['CHANGEDY'] = nacc.uds3.Field(name='CHANGEDY', typename='Num', position=(48,49), length=2, inclusive_range=(1, 31), allowable_values=['99'], blanks=['Blank if Question 4a DECEASED = 1 (Yes)', 'Blank if Question 4b DISCONT = 1 (Yes)'])
        self.fields['CHANGEYR'] = nacc.uds3.Field(name='CHANGEYR', typename='Num', position=(51,54), length=4, inclusive_range=(2015, CURRENT_YEAR), allowable_values=[], blanks=['Blank if Question 4a DECEASED = 1 (Yes)', 'Blank if Question 4b DISCONT = 1 (Yes)'])
        self.fields['PROTOCOL'] = nacc.uds3.Field(name='PROTOCOL', typename='Num', position=(56,56), length=1, inclusive_range=(1, 3), allowable_values=[], blanks=['Blank if Question 4a DECEASED = 1 (Yes)','Blank if Question 4b DISCONT = 1 (Yes)']) 
        self.fields['ACONSENT'] = nacc.uds3.Field(name='ACONSENT', typename='Num', position=(58,58), length=1, inclusive_range=(0, 1), allowable_values=['1', '0'], blanks=['Blank if Question 4a DECEASED = 1 (Yes)', 'Blank if Question 4b DISCONT = 1 (Yes)','Blank if Question 2a PROTOCOL = 3 (Annual  in-person follow-up)'])
        self.fields['RECOGIM'] =  nacc.uds3.Field(name='RECOGIM',  typename='Num', position=(60,60), length=1, inclusive_range=(0, 1), allowable_values=['1', '0'], blanks=['Blank if Question 4a DECEASED = 1 (Yes)', 'Blank if Question 4b DISCONT = 1 (Yes)'])
        self.fields['REPHYILL'] = nacc.uds3.Field(name='REPHYILL', typename='Num', position=(62,62), length=1, inclusive_range=(0, 1), allowable_values=['1', '0'], blanks=['Blank if Question 4a DECEASED = 1 (Yes)', 'Blank if Question 4b DISCONT = 1 (Yes)'])
        self.fields['REREFUSE'] = nacc.uds3.Field(name='REREFUSE', typename='Num', position=(64,64), length=1, inclusive_range=(0, 1), allowable_values=['1', '0'], blanks=['Blank if Question 4a DECEASED = 1 (Yes)', 'Blank if Question 4b DISCONT = 1 (Yes)'])
        self.fields['RENAVAIL'] = nacc.uds3.Field(name='RENAVAIL', typename='Num', position=(66,66), length=1, inclusive_range=(0, 1), allowable_values=['1', '0'], blanks=['Blank if Question 4a DECEASED = 1 (Yes)', 'Blank if Question 4b DISCONT = 1 (Yes)'])
        self.fields['RENURSE'] =  nacc.uds3.Field(name='RENURSE',  typename='Num', position=(68,68), length=1, inclusive_range=(0, 1), allowable_values=['1', '0'], blanks=['Blank if Question 4a DECEASED = 1 (Yes)', 'Blank if Question 4b DISCONT = 1 (Yes)'])
        self.fields['NURSEMO'] =  nacc.uds3.Field(name='NURSEMO',  typename='Num', position=(70,71), length=2, inclusive_range=(1, 12), allowable_values=['99'], blanks=['Blank if Question 2b5 RENURSE ne 1 (Yes)', 'Blank if Question 4a DECEASED = 1 (Yes)','Blank if Question 4b DISCONT = 1 (Yes)'])
        self.fields['NURSEDY'] =  nacc.uds3.Field(name='NURSEDY',  typename='Num', position=(73,74), length=2, inclusive_range=(1, 31), allowable_values=['99'], blanks=['Blank if Question 2b5 RENURSE ne 1 (Yes)', 'Blank if Question 4a DECEASED = 1 (Yes)','Blank if Question 4b DISCONT = 1 (Yes)'])
        self.fields['NURSEYR'] =  nacc.uds3.Field(name='NURSEYR',  typename='Num', position=(76,79), length=4, inclusive_range=(2015, CURRENT_YEAR), allowable_values=[], blanks=['Blank if Question 2b5 RENURSE ne 1 (Yes)', 'Blank if Question 4a DECEASED = 1 (Yes)','Blank if Question 4b DISCONT = 1 (Yes)'])
        self.fields['REJOIN'] =   nacc.uds3.Field(name='REJOIN',  typename='Num', position=(81,81), length=1, inclusive_range=(0, 1), allowable_values=['1', '0'], blanks=['Blank if Question 4a DECEASED = 1 (Yes)', 'Blank if Question 4b DISCONT = 1 (Yes)']) 
        self.fields['FTLDDISC'] = nacc.uds3.Field(name='FTLDDISC', typename='Num', position=(83,83), length=1, inclusive_range=(0, 1), allowable_values=['1', '0'], blanks=['Blank if Question 4a DECEASED = 1 (Yes)', 'Blank if Question 4b DISCONT = 1 (Yes)'])
        self.fields['FTLDREAS'] = nacc.uds3.Field(name='FTLDREAS', typename='Num', position=(85,85), length=1, inclusive_range=(1, 4), allowable_values=[], blanks=['Blank if Question 3 FTLDDISC ne 1 (Discontine FTLD)','Blank if Question 4a DECEASED = 1 (Yes)', 'Blank if Question 4b DISCONT = 1 (Yes)'])
        self.fields['FTLDREAX'] = nacc.uds3.Field(name='FTLDREAX', typename='Char', position=(87,146), length=60, inclusive_range=None, allowable_values=[], blanks=['Blank if Question 3a FTLDREAS ne 4 (Other)','Blank if Question 4a DECEASED = 1 (Yes)', 'Blank if Question 4b DISCONT = 1 (Yes)'])
        self.fields['DECEASED'] = nacc.uds3.Field(name='DECEASED', typename='Num', position=(148,148), length=1, inclusive_range=(0, 1), allowable_values=['1', '0'], blanks=['Blank if Question 2a PROTOCOL = 1 (Follow-up by telephone)', 'Blank if Question 2a PROTOCOL = 2 (Minimal contact)', 'Blank if Question 2a PROTOCOL = 3 (Annual in-person follow-up)', 'Blank if Question 3 FTLDDISC = 1 (Discontinue FTLD)', 'Blank if Question 4b DISCONT = 1 (Yes)'])#,'If Question 4a = 1 (Yes) then skip to Question 5a1'
        self.fields['DISCONT'] =  nacc.uds3.Field(name='DISCONT', typename='Num', position=(150,150), length=1, inclusive_range=(0, 1), allowable_values=['1', '0'], blanks=['Blank if Question 2a PROTOCOL = 1 (Follow-up by telephone)', 'Blank if Question 2a PROTOCOL = 2 (Minimal contact)', 'Blank if Question 2a PROTOCOL = 3 (Annual in-person follow-up)', 'Blank if Question 3 FTLDDISC = 1 (Discontinue FTLD)', 'Blank if Question 4a DECEASED = 1 (Yes)'])#,'If Question 4b = 1 (Yes) then skip to Question 6a1'
        self.fields['DEATHMO'] =  nacc.uds3.Field(name='DEATHMO', typename='Num', position=(152,153), length=2, inclusive_range=(1, 12), allowable_values=['99'], blanks=['Blank if Question 2a PROTOCOL = 1 (Follow-up by telephone)', 'Blank if Question 2a PROTOCOL = 2 (Minimal contact)', 'Blank if Question 2a PROTOCOL = 3 (Annual in-person follow-up)', 'Blank if Question 3 FTLDDISC = 1 (Discontinue FTLD)', 'Blank if Question 4b DISCONT = 1 (Yes)'])
        self.fields['DEATHDY'] =  nacc.uds3.Field(name='DEATHDY', typename='Num', position=(155,156), length=2, inclusive_range=(1, 31), allowable_values=['99'], blanks=['Blank if Question 2a PROTOCOL = 1 (Follow-up by telephone)', 'Blank if Question 2a PROTOCOL = 2 (Minimal contact)', 'Blank if Question 2a PROTOCOL = 3 (Annual in-person follow-up)', 'Blank if Question 3 FTLDDISC = 1 (Discontinue FTLD)', 'Blank if Question 4b DISCONT = 1 (Yes)'])
        self.fields['DEATHYR'] =  nacc.uds3.Field(name='DEATHYR', typename='Num', position=(158,161), length=4, inclusive_range=(2015, CURRENT_YEAR), allowable_values=[], blanks=['Blank if Question 2a PROTOCOL = 1 (Follow-up by telephone)', 'Blank if Question 2a PROTOCOL = 2 (Minimal contact)', 'Blank if Question 2a PROTOCOL = 3 (Annual in-person follow-up)', 'Blank if Question 3 FTLDDISC = 1 (Discontinue FTLD)', 'Blank if Question 4b DISCONT = 1 (Yes)'])
        self.fields['AUTOPSY'] =  nacc.uds3.Field(name='AUTOPSY', typename='Num', position=(163,163), length=1, inclusive_range=(0, 1), allowable_values=['1', '0'], blanks=['Blank if Question 2a PROTOCOL = 1 (Follow-up by telephone)', 'Blank if Question 2a PROTOCOL = 2 (Minimal contact)', 'Blank if Question 2a PROTOCOL = 3 (Annual in-person follow-up)', 'Blank if Question 3 FTLDDISC = 1 (Discontinue FTLD)', 'Blank if Question 4b DISCONT = 1 (Yes)'])
        self.fields['DISCMO'] =   nacc.uds3.Field(name='DISCMO', typename='Num', position=(165,166), length=2, inclusive_range=(1, 12), allowable_values=['99'], blanks=['Blank if Question 2a PROTOCOL = 1 (Follow-up by telephone)', 'Blank if Question 2a PROTOCOL = 2 (Minimal contact)', 'Blank if Question 2a PROTOCOL = 3 (Annual in-person follow-up)', 'Blank if Question 3 FTLDDISC = 1 (Discontinue FTLD)', 'Blank if Question 4a DECEASED = 1 (Yes)'])
        self.fields['DISCDAY'] =  nacc.uds3.Field(name='DISCDAY', typename='Num', position=(168,169), length=2, inclusive_range=(1, 31), allowable_values=['99'], blanks=['Blank if Question 2a PROTOCOL = 1 (Follow-up by telephone)', 'Blank if Question 2a PROTOCOL = 2 (Minimal contact)', 'Blank if Question 2a PROTOCOL = 3 (Annual in-person follow-up)', 'Blank if Question 3 FTLDDISC = 1 (Discontinue FTLD)', 'Blank if Question 4a DECEASED = 1 (Yes)'])
        self.fields['DISCYR'] =   nacc.uds3.Field(name='DISCYR', typename='Num', position=(171,174), length=4, inclusive_range=(2015, CURRENT_YEAR), allowable_values=[], blanks=['Blank if Question 2a PROTOCOL = 1 (Follow-up by telephone)', 'Blank if Question 2a PROTOCOL = 2 (Minimal contact)', 'Blank if Question 2a PROTOCOL = 3 (Annual in-person follow-up)', 'Blank if Question 3 FTLDDISC = 1 (Discontinue FTLD)', 'Blank if Question 4a DECEASED = 1 (Yes)'])
        self.fields['DROPREAS'] = nacc.uds3.Field(name='DROPREAS', typename='Num', position=(176,176), length=1, inclusive_range=(1, 2), allowable_values=['1', '2'], blanks=['Blank if Question 2a PROTOCOL = 1 (Follow-up by telephone)', 'Blank if Question 2a PROTOCOL = 2 (Minimal contact)', 'Blank if Question 2a PROTOCOL = 3 (Annual in-person follow-up)', 'Blank if Question 3 FTLDDISC = 1 (Discontinue FTLD)', 'Blank if Question 4a DECEASED = 1 (Yes)'])
