###############################################################################
# Copyright 2015-2016 University of Florida. All rights reserved.
# This file is part of UF CTS-IT's NACCulator project.
# Use of this source code is governed by the license found in the LICENSE file.
###############################################################################

from nacc.uds3 import blanks
from nacc.uds3 import clsform
import forms as m_form
from nacc.uds3 import packet as m_packet
import sys
import datetime

def build_uds3_m_form(record):
    """ Converts REDCap CSV data into a packet (list of M Form objects) """
    packet = m_packet.Packet()
    # Set up us the forms
    m = m_form.FormM()
    m.CHANGEMO = split_date(record['m1_1'],'M')
    m.CHANGEDY = split_date(record['m1_1'],'D')
    m.CHANGEYR = split_date(record['m1_1'],'Y')
    m.PROTOCOL = record['m1_2a']
    m.ACONSENT = record['m1_2a1']
    m.RECOGIM = record['m1_2b___1']
    m.REPHYILL = record['m1_2b___2']
    m.REREFUSE = record['m1_2b___3']
    m.RENAVAIL = record['m1_2b___4']
    m.RENURSE = record['m1_2b___5']
    m.NURSEMO = split_date(record['m1_2b1'],'M')
    m.NURSEDY = split_date(record['m1_2b1'],'D')
    m.NURSEYR = split_date(record['m1_2b1'],'Y')
    m.REJOIN = record['m1_2b___6']
    m.FTLDDISC = record['m1_3']
    m.FTLDREAS = record['m1_3a']
    m.FTLDREAx = record['m1_3a'] # Could not find in redcap.
    m.DECEASED = subject_deceased(record['m1_4'])
    m.DISCONT = subject_discont(record['m1_4'])
    m.DEATHMO = split_date(record['m1_5a'],'M')
    m.DEATHDY = split_date(record['m1_5a'],'D')
    m.DEATHYR = split_date(record['m1_5a'],'Y')
    m.AUTOPSY = record['m1_5b']
    m.DISCMO = split_date(record['m1_6a'],'M')
    m.DISCDAY = split_date(record['m1_6a'],'D')
    m.DISCYR = split_date(record['m1_6a'],'Y')
    m.DROPREAS = record['m1_6b']

    packet.append(m)
    return packet
    
def update_header(record, packet):
    for header in packet:
        header.PACKET = "M"
        header.FORMID = header.form_name
        header.FORMVER = 3
        header.ADCID = record['adcid']
        header.PTID = record['ptid']
        header.VISITMO = record['visitmo']
        header.VISITDAY = record['visitday']
        header.VISITYR = record['visityr']
        header.INITIALS = record['initials']

# may want to use python time object
# add condition for 99 as unknown
def split_date(date,DMY_choice):
    for fmt in ["%Y-%m-%d" ,"%m/%d/%Y"]:
        try:
            if DMY_choice =='D':
                return int(datetime.datetime.strptime(date, fmt).date().strftime("%d"))
            elif DMY_choice =='M':
                return int(datetime.datetime.strptime(date, fmt).date().strftime("%m"))
            elif DMY_choice == 'Y':
                return int(datetime.datetime.strptime(date, fmt).date().strftime("%Y"))
        except ValueError:
            print(ValueError)
            continue
# may be wrong depending on what record[] returns
def subject_deceased(status):
    if status == 1:
        return 1
    else:
        return 0

def subject_discont(status):
    if status == 2:
        return 1
    else:
        return 0
    