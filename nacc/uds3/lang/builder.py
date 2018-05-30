###############################################################################
# Copyright 2015-2016 University of Florida. All rights reserved.
# This file is part of UF CTS-IT's NACCulator project.
# Use of this source code is governed by the license found in the LICENSE file.
###############################################################################

from nacc.uds3 import blanks
import forms as ivp_forms
from nacc.uds3 import packet as ivp_packet
import sys

def build_uds3_ivp_form(record):
    """ Converts REDCap CSV data into a packet (list of IVP Form objects) """
    packet = ivp_packet.Packet()

    # Set up us the forms
    cls_form = ivp_forms.FormCLS()
    cls_form.APREFLAN = record['eng_preferred_language']
    cls_form.AYRSPAN = record['eng_years_speak_spanish']
    cls_form.AYRENGL = record['eng_years_speak_english']
    cls_form.APCSPAN = record['eng_percentage_spanish']
    cls_form.APCENGL = record['eng_percentage_english']
    cls_form.ASPKSPAN = record['eng_proficiency_spanish']
    cls_form.AREASPAN = record['eng_proficiency_read_spanish']
    cls_form.AWRISPAN = record['eng_proficiency_write_spanish']
    cls_form.AUNDSPAN = record['eng_proficiency_oral_spanish']
    cls_form.ASPKENGL = record['eng_proficiency_speak_english']
    cls_form.AREAENGL = record['eng_proficiency_read_english']
    cls_form.AWRIENGL = record['eng_proficiency_write_english']
    cls_form.AUNDENGL = record['eng_proficiency_oral_english']
    packet.append(cls_form)

def update_header(record, packet):
    for header in packet:
        header.PACKET = "I"
        header.FORMID = header.form_name
        if header.FORMID.value == "B5 ":
            header.FORMVER = "3.1"
        elif header.FORMID.value == "C1S":
            header.FORMVER = 2
        else:
            header.FORMVER = 3
        header.ADCID = record['adcid']
        header.PTID = record['ptid']
        header.VISITMO = record['visitmo']
        header.VISITDAY = record['visitday']
        header.VISITYR = record['visityr']
        header.VISITNUM = record['visitnum']
        header.INITIALS = record['initials']
