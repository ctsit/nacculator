###############################################################################
# Copyright 2015-2016 University of Florida. All rights reserved.
# This file is part of UF CTS-IT's NACCulator project.
# Use of this source code is governed by the license found in the LICENSE file.
###############################################################################

from datetime import date
import nacc.uds2
import nacc.uds3
import nacc.uds3.ivp.forms


CURRENT_YEAR = date.today().year


class FormC1S(nacc.uds3.FieldBag):
    def __init__(self):
        self.fields = nacc.uds3.ivp.forms.header_fields()
        self.fields['MMSELOC'] = nacc.uds3.Field(
            name='MMSELOC', typename='Num', position=(45, 45), length=1,
            allowable_values=['1', '2', '3'])
        self.fields['MMSELAN'] = nacc.uds3.Field(
            name='MMSELAN', typename='Num', position=(47, 47), length=1,
            allowable_values=['1', '2', '3'])
        self.fields['MMSELANX'] = nacc.uds3.Field(
            name='MMSELANX', typename='Char', position=(49, 108), length=60,
            blanks=['Blank if Question 1A1 MMSELAN ne 3 (Other)'])
        self.fields['MMSEORDA'] = nacc.uds3.Field(
            name='MMSEORDA', typename='Num', position=(110, 111), length=2,
            inclusive_range=(0, 5), allowable_values=['95', '96', '97', '98'])
        self.fields['MMSEORLO'] = nacc.uds3.Field(
            name='MMSEORLO', typename='Num', position=(113, 114), length=2,
            inclusive_range=(0, 5), allowable_values=['95', '96', '97', '98'])
        self.fields['PENTAGON'] = nacc.uds3.Field(
            name='PENTAGON', typename='Num', position=(116, 117), length=2,
            inclusive_range=(0, 1), allowable_values=['95', '96', '97', '98'])
        self.fields['MMSE'] = nacc.uds3.Field(
            name='MMSE', typename='Num', position=(119, 120), length=2,
            inclusive_range=(0, 30), allowable_values=['95', '96', '97', '98'])
        self.fields['NPSYCLOC'] = nacc.uds3.Field(
            name='NPSYCLOC', length=1, position=(122, 122), typename='Num',
            allowable_values=['1', '2', '3'])
        self.fields['NPSYLAN'] = nacc.uds3.Field(
            name='NPSYLAN', length=1, position=(124, 124), typename='Num',
            allowable_values=['1', '2', '3'])
        self.fields['NPSYLANX'] = nacc.uds3.Field(
            name='NPSYLANX', length=60, position=(126, 185), typename='Char',
            blanks=['Blank if Question 2A NPSYLAN ne 3 (Other)'])
        self.fields['LOGIMO'] = nacc.uds3.Field(
            name='LOGIMO', length=2, position=(187, 188), typename='Num',
            inclusive_range=(1, 12), allowable_values=['88'])
        self.fields['LOGIDAY'] = nacc.uds3.Field(
            name='LOGIDAY', length=2, position=(190, 191), typename='Num',
            inclusive_range=(1, 31), allowable_values=['88'])
        self.fields['LOGIYR'] = nacc.uds3.Field(
            name='LOGIYR', length=4, position=(193, 196), typename='Num',
            allowable_values=[str(CURRENT_YEAR), str(CURRENT_YEAR-1), '88'])
        self.fields['LOGIPREV'] = nacc.uds3.Field(
            name='LOGIPREV', length=2, position=(198, 199), typename='Num',
            inclusive_range=(0, 25), allowable_values=['88'])
        self.fields['LOGIMEM'] = nacc.uds3.Field(
            name='LOGIMEM', length=2, position=(201, 202), typename='Num',
            inclusive_range=(0, 25),
            allowable_values=['95', '96', '97', '98'])

        self.fields['DIGIF'] = nacc.uds3.Field(
            name='DIGIF', length=2, position=(204, 205), typename='Num',
            inclusive_range=(0, 12),
            allowable_values=['95', '96', '97', '98'])
        self.fields['DIGIFLEN'] = nacc.uds3.Field(
            name='DIGIFLEN', length=2, position=(207, 208), typename='Num',
            inclusive_range=(0, 8), allowable_values=['95', '96', '97', '98'])

        self.fields['DIGIB'] = nacc.uds3.Field(
            name='DIGIB', length=2, position=(210, 211), typename='Num',
            inclusive_range=(0, 12),
            allowable_values=['95', '96', '97', '98'])
        self.fields['DIGIBLEN'] = nacc.uds3.Field(
            name='DIGIBLEN', length=2, position=(213, 214), typename='Num',
            inclusive_range=(0, 7), allowable_values=['95', '96', '97', '98'])

        self.fields['ANIMALS'] = nacc.uds3.Field(
            name='ANIMALS', length=2, position=(216, 217), typename='Num',
            inclusive_range=(0, 77),
            allowable_values=['95', '96', '97', '98'])
        self.fields['VEG'] = nacc.uds3.Field(
            name='VEG', length=2, position=(219, 220), typename='Num',
            inclusive_range=(0, 77),
            allowable_values=['95', '96', '97', '98'])

        self.fields['TRAILA'] = nacc.uds3.Field(
            name='TRAILA', length=3, position=(222, 224), typename='Num',
            inclusive_range=(0, 150),
            allowable_values=['995', '996', '997', '998'])
        self.fields['TRAILARR'] = nacc.uds3.Field(
            name='TRAILARR', length=2, position=(226, 227), typename='Num',
            inclusive_range=(0, 40), allowable_values=['88'],
            blanks=['Blank if Question 7A TRAILA = 995-998'])
        self.fields['TRAILALI'] = nacc.uds3.Field(
            name='TRAILALI', length=2, position=(229, 230), typename='Num',
            inclusive_range=(0, 24), allowable_values=['88'],
            blanks=['Blank if Question 7A TRAILA = 995-998'])

        self.fields['TRAILB'] = nacc.uds3.Field(
            name='TRAILB', length=3, position=(232, 234), typename='Num',
            inclusive_range=(0, 300),
            allowable_values=['995', '996', '997', '998'])
        self.fields['TRAILBRR'] = nacc.uds3.Field(
            name='TRAILBRR', length=2, position=(236, 237), typename='Num',
            inclusive_range=(0, 40), allowable_values=['88'],
            blanks=['Blank if Question 7B TRAILB = 995-998'])
        self.fields['TRAILBLI'] = nacc.uds3.Field(
            name='TRAILBLI', length=2, position=(239, 240), typename='Num',
            inclusive_range=(0, 24), allowable_values=['88'],
            blanks=['Blank if Question 7B TRAILB = 995-998'])

        self.fields['WAIS'] = nacc.uds3.Field(
            name='WAIS', length=2, position=(242, 243), typename='Num',
            inclusive_range=(0, 93), allowable_values=['95', '96', '97', '98'])

        self.fields['MEMUNITS'] = nacc.uds3.Field(
            name='MEMUNITS', length=2, position=(245, 246), typename='Num',
            inclusive_range=(0, 25), allowable_values=['95', '96', '97', '98'])
        self.fields['MEMTIME'] = nacc.uds3.Field(
            name='MEMTIME', length=2, position=(248, 249), typename='Num',
            inclusive_range=(0, 85), allowable_values=['88', '99'])

        self.fields['BOSTON'] = nacc.uds3.Field(
            name='BOSTON', length=2, position=(251, 252), typename='Num',
            inclusive_range=(0, 30), allowable_values=['95', '96', '97', '98'])

        self.fields['COGSTAT'] = nacc.uds3.Field(
            name='COGSTAT', length=2, position=(254, 254), typename='Num',
            allowable_values=['1', '2', '3', '4', '0'])
