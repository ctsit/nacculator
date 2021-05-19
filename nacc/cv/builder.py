###############################################################################
# Copyright 2015-2021 University of Florida. All rights reserved.
# This file is part of UF CTS-IT's NACCulator project.
# Use of this source code is governed by the license found in the LICENSE file.
###############################################################################

import sys

from nacc.cv import forms as cv_forms
from nacc.uds3 import packet as cv_packet
import re


def build_cv_form(record: dict, err=sys.stderr):
    ''' Converts REDCap CSV data into a packet (list of FVP Form objects) '''
    packet = cv_packet.Packet()

    # This form cannot precede Jan 1, 2020.
    if not (int(parse_date(record['date'], 'Y')) > 2019):
        raise ValueError('Form date cannot precede Jan 1, 2020.')

    add_f1(record, packet)
    add_f2(record, packet)
    add_f3(record, packet)
    update_header(record, packet)

    return packet


def add_f1(record, packet):
    F1 = cv_forms.FormF1()
    F1.C19TVIS  = record['C19TVIS'.lower()]
    F1.C19TPHON = record['C19TPHON'.lower()]
    F1.C19TTAB  = record['C19TTAB'.lower()]
    F1.C19TLAP  = record['C19TLAP'.lower()]
    F1.C19TCOMP = record['C19TCOMP'.lower()]
    F1.C19TOTH  = record['C19TOTH'.lower()]
    F1.C19TOTHX = record['C19TOTHX'.lower()]
    F1.C19TEMAI = record['C19TEMAI'.lower()]
    F1.C19TIPHN = record['C19TIPHN'.lower()]
    F1.C19TITAB = record['C19TITAB'.lower()]
    F1.C19TILAP = record['C19TILAP'.lower()]
    F1.C19TICOM = record['C19TICOM'.lower()]
    F1.C19TIWED = record['C19TIWED'.lower()]
    F1.C19TISHD = record['C19TISHD'.lower()]
    F1.C19TIOTH = record['C19TIOTH'.lower()]
    F1.C19TIOTX = record['C19TIOTX'.lower()]
    packet.append(F1)


def add_f2(record, packet):
    F2 = cv_forms.FormF2()
    F2.C19SYMPT = record['C19SYMPT'.lower()]
    F2.C19SYOTX = record['C19SYOTX'.lower()]
    F2.C19TEST  = record['C19TEST'.lower()]
    try:
        F2.C19T1MO  = record['C19T1MO'.lower()]
        F2.C19T1DY  = record['C19T1DY'.lower()]
        F2.C19T1YR  = record['C19T1YR'.lower()]
    except KeyError:
        F2.C19T1MO  = parse_date(record['C19T1'.lower()], 'M')
        F2.C19T1DY  = parse_date(record['C19T1'.lower()], 'D')
        F2.C19T1YR  = parse_date(record['C19T1'.lower()], 'Y')
    F2.C19T1TYP = record['C19T1TYP'.lower()]
    try:
        F2.C19T2MO  = record['C19T2MO'.lower()]
        F2.C19T2DY  = record['C19T2DY'.lower()]
        F2.C19T2YR  = record['C19T2YR'.lower()]
    except KeyError:
        F2.C19T2MO  = parse_date(record['C19T2'.lower()], 'M')
        F2.C19T2DY  = parse_date(record['C19T2'.lower()], 'D')
        F2.C19T2YR  = parse_date(record['C19T2'.lower()], 'Y')
    F2.C19T2TYP = record['C19T2TYP'.lower()]
    try:
        F2.C19T3MO  = record['C19T3MO'.lower()]
        F2.C19T3DY  = record['C19T3DY'.lower()]
        F2.C19T3YR  = record['C19T3YR'.lower()]
    except KeyError:
        F2.C19T3MO  = parse_date(record['C19T3'.lower()], 'M')
        F2.C19T3DY  = parse_date(record['C19T3'.lower()], 'D')
        F2.C19T3YR  = parse_date(record['C19T3'.lower()], 'Y')
    F2.C19T3TYP = record['C19T3TYP'.lower()]
    F2.C19DIAG  = record['C19DIAG'.lower()]
    F2.C19HOSP  = record['C19HOSP'.lower()]
    try:
        F2.C19H1MO  = record['C19H1MO'.lower()]
        F2.C19H1DY  = record['C19H1DY'.lower()]
        F2.C19H1YR  = record['C19H1YR'.lower()]
    except KeyError:
        F2.C19H1MO  = parse_date(record['C19H1'.lower()], 'M')
        F2.C19H1DY  = parse_date(record['C19H1'.lower()], 'D')
        F2.C19H1YR  = parse_date(record['C19H1'.lower()], 'Y')
    F2.C19H1DYS = record['C19H1DYS'.lower()]
    try:
        F2.C19H2MO  = record['C19H2MO'.lower()]
        F2.C19H2DY  = record['C19H2DY'.lower()]
        F2.C19H2YR  = record['C19H2YR'.lower()]
    except KeyError:
        F2.C19H2MO  = parse_date(record['C19H2'.lower()], 'M')
        F2.C19H2DY  = parse_date(record['C19H2'.lower()], 'D')
        F2.C19H2YR  = parse_date(record['C19H2'.lower()], 'Y')
    F2.C19H2DYS = record['C19H2DYS'.lower()]
    try:
        F2.C19H3MO  = record['C19H3MO'.lower()]
        F2.C19H3DY  = record['C19H3DY'.lower()]
        F2.C19H3YR  = record['C19H3YR'.lower()]
    except KeyError:
        F2.C19H3MO  = parse_date(record['C19H3'.lower()], 'M')
        F2.C19H3DY  = parse_date(record['C19H3'.lower()], 'D')
        F2.C19H3YR  = parse_date(record['C19H3'.lower()], 'Y')
    F2.C19H3DYS = record['C19H3DYS'.lower()]
    F2.C19WORRY = record['C19WORRY'.lower()]
    F2.C19ISO  = record['C19ISO'.lower()]
    F2.C19DIS  = record['C19DIS'.lower()]
    F2.C19INC  = record['C19INC'.lower()]
    F2.C19CTRL = record['C19CTRL'.lower()]
    F2.C19MH   = record['C19MH'.lower()]
    F2.C19CMEM = record['C19CMEM'.lower()]
    F2.C19CDEP = record['C19CDEP'.lower()]
    F2.C19CANX = record['C19CANX'.lower()]
    F2.C19CBEH = record['C19CBEH'.lower()]
    F2.C19COTH = record['C19COTH'.lower()]
    F2.C19OTHX = record['C19OTHX'.lower()]
    F2.C19RES  = record['C19RES'.lower()]
    packet.append(F2)


def add_f3(record, packet):
    F3 = cv_forms.FormF3()
    F3.C19COISO = record['C19COISO'.lower()]
    F3.C19CODIS = record['C19CODIS'.lower()]
    F3.C19COINC = record['C19COINC'.lower()]
    F3.C19COCTL = record['C19COCTL'.lower()]
    F3.C19CONN  = record['C19CONN'.lower()]
    F3.C19CARE  = record['C19CARE'.lower()]
    F3.C19KFAM  = record['C19KFAM'.lower()]
    F3.C19KAGE  = record['C19KAGE'.lower()]
    F3.C19KACT  = record['C19KACT'.lower()]
    F3.C19KOVE  = record['C19KOVE'.lower()]
    F3.C19KFAC  = record['C19KFAC'.lower()]
    F3.C19KAPP  = record['C19KAPP'.lower()]
    F3.C19KOTH  = record['C19KOTH'.lower()]
    F3.C19KOTHX = record['C19KOTHX'.lower()]
    F3.C19CORE  = record['C19CORE'.lower()]
    F3.C19COPRE = record['C19COPRE'.lower()]
    F3.C19COSPX = record['C19COSPX'.lower()]
    packet.append(F3)


def update_header(record, packet):
    for header in packet:
        header.PACKET = "CV"
        header.FORMID = header.form_name
        header.FORMVER = 1
        header.ADCID = record['adcid']
        header.PTID = record['ptid']
        header.VISITMO = parse_date(record['date'], 'M')
        header.VISITDAY = parse_date(record['date'], 'D')
        header.VISITYR = parse_date(record['date'], 'Y')
        header.INITIALS = record['initials']


# parse header date
def parse_date(date, DMY_choice):
    ymd = re.compile('\d\d\d\d[-\/]\d\d[-\/]\d\d')
    mdy = re.compile('\d\d[-\/]\d\d[-\/]\d\d\d\d')
    dub = re.compile('\d\d')
    if mdy.match(date) != None:  # format is mdy
        m = dub.findall(date)
        if DMY_choice == "D":
            return m[1]
        elif DMY_choice == "M":
            return m[0]
        elif DMY_choice == "Y":
            return m[2] + m[3]
    elif ymd.match(date) != None:  # format is ymd
        m = dub.findall(date)
        if DMY_choice == "D":
            return m[3]
        elif DMY_choice == "M":
            return m[2]
        elif DMY_choice == "Y":
            return m[0] + m[1]
    elif date == '':
        return ''
    raise ValueError('Inccorect date format for %s, date must be MM/DD/YYYY' % date)
