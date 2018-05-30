###############################################################################
# Copyright 2015-2016 University of Florida. All rights reserved.
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


class FormA4G(nacc.uds3.FieldBag):
    def __init__(self):
        self.fields = header_fields()
        self.fields['ANYMEDS'] = nacc.uds3.Field(name='ANYMEDS',
                                                 typename='Num',
                                                 position=(45, 45), length=1,
                                                 allowable_values=['0', '1'])

### END non-generated code


def header_fields():
    fields = {}
    fields['PACKET'] = nacc.uds3.Field(name='PACKET', typename='Char', position=(1, 2), length=2, inclusive_range=None, allowable_values=[], blanks=[])
    fields['FORMID'] = nacc.uds3.Field(name='FORMID', typename='Char', position=(4, 6), length=3, inclusive_range=None, allowable_values=[], blanks=[])
    fields['FORMVER'] = nacc.uds3.Field(name='FORMVER', typename='Num', position=(8, 10), length=3, inclusive_range=(1, 3), allowable_values=[], blanks=[])
    fields['ADCID'] = nacc.uds3.Field(name='ADCID', typename='Num', position=(12, 13), length=2, inclusive_range=(2, 43), allowable_values=[], blanks=[])
    fields['PTID'] = nacc.uds3.Field(name='PTID', typename='Char', position=(15, 24), length=10, inclusive_range=None, allowable_values=[], blanks=[])
    fields['VISITMO'] = nacc.uds3.Field(name='VISITMO', typename='Num', position=(26, 27), length=2, inclusive_range=(1, 12), allowable_values=[], blanks=[])
    fields['VISITDAY'] = nacc.uds3.Field(name='VISITDAY', typename='Num', position=(29, 30), length=2, inclusive_range=(1, 31), allowable_values=[], blanks=[])
    fields['VISITYR'] = nacc.uds3.Field(name='VISITYR', typename='Num', position=(32, 35), length=4, inclusive_range=(2005, CURRENT_YEAR), allowable_values=[], blanks=[])
    fields['VISITNUM'] = nacc.uds3.Field(name='VISITNUM', typename='Char', position=(37, 39), length=3, inclusive_range=None, allowable_values=[], blanks=[])
    fields['INITIALS'] = nacc.uds3.Field(name='INITIALS', typename='Char', position=(41, 43), length=3, inclusive_range=None, allowable_values=[], blanks=[])
    return fields

class FormCLS(nacc.uds3.FieldBag):
    def __init__(self):
        self.fields = header_fields()
        self.fields['APREFLAN'] = nacc.uds3.Fiels(name='APREFLAN', typename='Num', position=(45, 45), length=1, inclusive_range=(1, 2), allowable_values=['1', '2'], blanks=[])
        self.fields['AYRSPAN'] = nacc.uds3.Fiels(name='AYRSPAN', typename='Num', position=(47, 49), length=3, inclusive_range=(0, 110), allowable_values=[], blanks=[])
        self.fields['AYRENGL'] = nacc.uds3.Fiels(name='AYRENGL', typename='Num', position=(51, 53), length=3, inclusive_range=(0, 110), allowable_values=[], blanks=[])
        self.fields['APCSPAN'] = nacc.uds3.Fiels(name='APCSPAN', typename='Num', position=(55, 57), length=3, inclusive_range=(0, 100), allowable_values=[], blanks=[])
        self.fields['APCENGL'] = nacc.uds3.Fiels(name='APCENGL', typename='Num', position=(59, 61), length=3, inclusive_range=(0, 110), allowable_values=[], blanks=[])
        self.fields['ASPKSPAN'] = nacc.uds3.Fiels(name='ASPKSPAN', typename='Num', position=(63, 63), length=1, inclusive_range=(1, 7), allowable_values=['1', '2', '3', '4', '5', '6', '7'], blanks=[])
        self.fields['AREASPAN'] = nacc.uds3.Fiels(name='AREASPAN', typename='Num', position=(65, 65), length=1, inclusive_range=(1, 7), allowable_values=['1', '2', '3', '4', '5', '6', '7'], blanks=[])
        self.fields['AWRISPAN'] = nacc.uds3.Fiels(name='AWRISPAN', typename='Num', position=(67, 67), length=1, inclusive_range=(1, 7), allowable_values=['1', '2', '3', '4', '5', '6', '7'], blanks=[])
        self.fields['AUNDSPAN'] = nacc.uds3.Fiels(name='AUNDSPAN', typename='Num', position=(69, 69), length=1, inclusive_range=(1, 7), allowable_values=['1', '2', '3', '4', '5', '6', '7'], blanks=[])
        self.fields['ASPKENGL'] = nacc.uds3.Fiels(name='ASPKENGL', typename='Num', position=(71, 71), length=1, inclusive_range=(1, 7), allowable_values=['1', '2', '3', '4', '5', '6', '7'], blanks=[])
        self.fields['AREAENGL'] = nacc.uds3.Fiels(name='AREAENGL', typename='Num', position=(73, 73), length=1, inclusive_range=(1, 7), allowable_values=['1', '2', '3', '4', '5', '6', '7'], blanks=[])
        self.fields['AWRIENGL'] = nacc.uds3.Fiels(name='AWRIENGL', typename='Num', position=(75, 75), length=1, inclusive_range=(1, 7), allowable_values=['1', '2', '3', '4', '5', '6', '7'], blanks=[])
        self.fields['AUNDENGL'] = nacc.uds3.Fiels(name='AUNDENGL', typename='Num', position=(77, 77), length=1, inclusive_range=(1, 7), allowable_values=['1', '2', '3', '4', '5', '6', '7'], blanks=[])