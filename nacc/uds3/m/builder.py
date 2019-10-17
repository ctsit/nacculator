###############################################################################
# Copyright 2015-2016 University of Florida. All rights reserved.
# This file is part of UF CTS-IT's NACCulator project.
# Use of this source code is governed by the license found in the LICENSE file.
###############################################################################

from nacc.uds3 import blanks
from nacc.uds3.m import forms as m_form
from nacc.uds3 import packet as m_packet
import sys
import re

def build_uds3_m_form(record):
    
    """ Converts REDCap CSV data into a packet (list of M Form objects) """
    packet = m_packet.Packet()
    m = m_form.FormM()
    m.CHANGEMO = parse_date(record['m1_1'],'M')
    m.CHANGEDY = parse_date(record['m1_1'],'D')
    m.CHANGEYR = parse_date(record['m1_1'],'Y')
    m.PROTOCOL = record['m1_2a']
    m.ACONSENT = record['m1_2a1']
    m.RECOGIM  = record['m1_2b___1']
    m.REPHYILL = record['m1_2b___2']
    m.REREFUSE = record['m1_2b___3']
    m.RENAVAIL = record['m1_2b___4']
    m.RENURSE  = record['m1_2b___5']
    m.NURSEMO  = parse_date(record['m1_2b1'],'M')
    m.NURSEDY  = parse_date(record['m1_2b1'],'D')
    m.NURSEYR  = parse_date(record['m1_2b1'],'Y')
    m.REJOIN   = record['m1_2b___6']
    m.FTLDDISC = record['m1_3']
    m.FTLDREAS = record['m1_3a']
    m.FTLDREAx = record['m1_3a1']   # Note :  May need to add testing for {',",&,%} to remove
    m.DECEASED = subject_deceased(record['m1_4'])
    m.DISCONT  =  subject_discont(record['m1_4'])
    m.DEATHMO  = parse_date(record['m1_5a'],'M')
    m.DEATHDY  = parse_date(record['m1_5a'],'D')
    m.DEATHYR  = parse_date(record['m1_5a'],'Y')
    m.AUTOPSY  = record['m1_5b']
    m.DISCMO   = parse_date(record['m1_6a'],'M')
    m.DISCDAY  = parse_date(record['m1_6a'],'D')
    m.DISCYR   = parse_date(record['m1_6a'],'Y')
    m.DROPREAS = record['m1_6b']
    packet.append(m)

    update_header(record,packet)
    return packet
    
    #update header function may be wrong
def update_header(record, packet):
    for header in packet:
        header.PACKET = 'M'
        header.FORMID = 'M1' # header.form_name
        header.FORMVER = 3
        header.ADCID = 41 #record['ABCID']
        header.PTID = record['ptid']
        header.VISITMO =   parse_date(record['m1_form_date'],'M')
        header.VISITDAY =  parse_date(record['m1_form_date'],'D')
        header.VISITYR =   parse_date(record['m1_form_date'],'Y')
        header.INITIALS =  '' #record['INITIALS'] Note not in RedCap

    
# parse 
def parse_date(date,DMY_choice):   
    ymd = re.compile('\d\d\d\d[-\/]\d\d[-\/]\d\d')
    mdy = re.compile('\d\d[-\/]\d\d[-\/]\d\d\d\d')
    dub = re.compile('\d\d')
    if mdy.match(date) != None: # format is mdy
        m = dub.findall(date)
        if DMY_choice == "D": 
            return m[1]
        elif DMY_choice == "M":
            return m[0]
        elif DMY_choice == "Y":
            return m[2] + m[3]
    elif ymd.match(date)!= None: #format is ymd
        m = dub.findall(date)
        if DMY_choice == "D":
            return m[3]
        elif  DMY_choice == "M": 
            return m[2] 
        elif DMY_choice == "Y":
            return m[0] + m[1]
    elif date =='':   
        return ''
    raise ValueError('Inccorect death date format, date must be MM/DD/YYYY')

def subject_deceased(status):
    """ Splits Deceased from Discont """
    if status == '1': 
        return 1
    else:
        return 

def subject_discont(status):
    """ Splits Discont from Deceased """
    if status == '2': 
        return 1
    else:
        return 
