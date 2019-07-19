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

def build_uds3_m_form(record):
    """ Converts REDCap CSV data into a packet (list of IVP Form objects) """
    packet = m_packet.Packet()

    # Set up us the forms
    m = m_form.FormM()
    m.CHANGEMO = record['changemo']
    m.CHANGEDY = record['changedy']
    m.CHANGEYR = record['changeyr']
    m.PROTOCOL = record['protocol']
    m.ACONSENT = record['aconsent']
    m.RECOGIM = record['recogim']
    m.REPHYILL = record['rephyill']
    m.REREFUSE = record['rerefuse']
    m.RENAVAIL = record['renavail']
    m.RENURSE = record['renurse']
    m.NURSEMO = record['nursemo']
    m.NURSEDY = record['nursedy']
    m.NURSEYR = record['nerseyr']
    m.REJOIN = record['rejoin']
    m.FTLDDISC = record['ftlddisc']
    m.FTLDREAS = record['ftldreas']
    m.FTLDREAx = record['ftldreax']
    m.DECEASED = record['deceased']
    m.DISCONT = record['discont']
    m.DEATHMO = record['deathmo']
    m.DEATHDY = record['deathdy']
    m.DEATHYR = record['deathyr']
    m.AUTOPSY = record['autopsy']
    m.DISCMO = record['discmo']
    m.DISCDY = record['discdy']
    m.DISCYR = record['discyr']
    m.DROPREAS = record['dropreas']

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