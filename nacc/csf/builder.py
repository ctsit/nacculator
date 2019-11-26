###############################################################################
# Copyright 2015-2019 University of Florida. All rights reserved.
# This file is part of UF CTS-IT's NACCulator project.
# Use of this source code is governed by the license found in the LICENSE file.
###############################################################################

from nacc.csf import forms as csf_forms
from nacc.uds3 import packet as csf_packet


def build_uds3_csf_form(record):
    """ Converts REDCap CSV data into a packet (list of CSF Module objects) """
    packet = csf_packet.Packet()

    # Set up the forms.
    eE2 = csf_forms.FormEE2()
    eE2.CSFABETA = record['csfabeta']
    eE2.CSFABmo  = record['csfabmo']
    eE2.CSFABDY  = record['csfabdy']
    eE2.CSFABYr  = record['csfabyr']
    eE2.CSFABmD  = record['csfabmd']
    eE2.CSFABmDX = record['csfabmdx']
    eE2.CSFPTAU  = record['csfptau']
    eE2.CSFPTmo  = record['csfptmo']
    eE2.CSFPTDY  = record['csfptdy']
    eE2.CSFPTYr  = record['csfptyr']
    eE2.CSFPTmD  = record['csfptmd']
    eE2.CSFPTmDX = record['csfptmdx']
    eE2.CSFTTAU  = record['csfttau']
    eE2.CSFTTmo  = record['csfttmo']
    eE2.CSFTTDY  = record['csfttdy']
    eE2.CSFTTYr  = record['csfttyr']
    eE2.CSFTTmD  = record['csfttmd']
    eE2.CSFTTmDX = record['csfttmdx']
    packet.append(eE2)

    update_header(record, packet)
    return packet


def update_header(record, packet):
    for header in packet:
        # header.PACKET = "CSF"
        # header.FORMID = header.form_name
        # header.FORMVER = 1
        header.ADCID = record['adcid']
        header.PTID = record['ptid']
        header.VISITMO = record['visitmo']
        header.VISITDAY = record['visitday']
        header.VISITYR = record['visityr']
        # header.VISITNUM = record['visitnum']
        header.CSFLPmo = record['csflpmo']
        header.CSFLPDY = record['csflpdy']
        header.CSFLPYR = record['csflpyr']
        header.CSFINIT = record['csfinit']
