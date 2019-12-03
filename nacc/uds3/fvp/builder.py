###############################################################################
# Copyright 2015-2016 University of Florida. All rights reserved.
# This file is part of UF CTS-IT's NACCulator project.
# Use of this source code is governed by the license found in the LICENSE file.
###############################################################################

from nacc.uds3 import blanks
from nacc.uds3.fvp import forms as fvp_forms
from nacc.uds3 import clsform
from nacc.uds3 import packet as fvp_packet

def build_uds3_fvp_form(record):
    """ Converts REDCap CSV data into a packet (list of FVP Form objects) """
    packet = fvp_packet.Packet()

    # Set up the forms
    add_z1_or_z1x(record, packet)
    add_a1(record, packet)
    if record['fu_a2_sub'] == '1' or record['fu_a2sub'] == '1':
        add_a2(record, packet)
    if record['fu_a3_sub'] == '1' or record['fu_a3sub'] == '1':
        add_a3(record, packet)
    if record['fu_a4_sub'] == '1' or record['fu_a4sub'] == '1':
        add_a4(record, packet)
    if record['fu_b1_sub'] == '1' or record['fu_b1sub'] == '1':
        add_b1(record, packet)
    add_b4(record, packet)
    if record['fu_b5_sub'] == '1' or record['fu_b5sub'] == '1':
        add_b5(record, packet)
    if record['fu_b6_sub'] == '1' or record['fu_b6sub'] == '1':
        add_b6(record, packet)
    if record['fu_b7_sub'] == '1' or record['fu_b7sub'] == '1':
        add_b7(record, packet)
    add_b8(record, packet)
    add_b9(record, packet)
    add_c1s_or_c2(record, packet)
    add_d1(record, packet)
    add_d2(record, packet)
    clsform.add_cls(record, packet, fvp_forms)
    update_header(record, packet)

    return packet


def add_z1_or_z1x(record, packet):
    # Forms A1, A5, B4, B8, B9, C2, D1, and D2 are all REQUIRED.
    # Fields a1sub, a5sub1, b4sub1, b8sub1, b9sub1, c2sub1, d1sub1, and d2sub1
    # are just section separators.
    z1x = fvp_forms.FormZ1X()
    z1x_filled_fields = 0
    z1x_field_mapping = {
        'LANGA1': 'fu_langa1',
        'LANGA2': 'fu_langa2',
        'A2SUB': 'fu_a2sub',
        'A2NOT': 'fu_a2not',
        'LANGA3': 'fu_langa3',
        'A3SUB': 'fu_a3sub',
        'LANGA4': 'fu_langa4',
        'A4SUB': 'fu_a4sub',
        'A4NOT': 'fu_a4not',
        'LANGB1': 'fu_langb1',
        'B1SUB': 'fu_b1sub',
        'B1NOT': 'fu_b1not',
        'LANGB4': 'fu_langb4',
        'LANGB5': 'fu_langb5',
        'B5SUB': 'fu_b5sub',
        'B5NOT': 'fu_b5not',
        'LANGB6': 'fu_langb6',
        'B6SUB': 'fu_b6sub',
        'B6NOT': 'fu_b6not',
        'LANGB7': 'fu_langb7',
        'B7SUB': 'fu_b7sub',
        'B7NOT': 'fu_b7not',
        'LANGB8': 'fu_langb8',
        'LANGB9': 'fu_langb9',
        'LANGC2': 'fu_langc2',
        'LANGD1': 'fu_langd1',
        'LANGD2': 'fu_langd2',
        'LANGA3A': 'fu_langa3a',
        'FTDA3AFS': 'fu_ftda3afs',
        'FTDA3AFR': 'fu_ftda3afr',
        'LANGB3F': 'fu_langb3f',
        'LANGB9F': 'fu_langb9f',
        'LANGC1F': 'fu_langc1f',
        'LANGC2F': 'fu_langc2f',
        'LANGC3F': 'fu_langc3f',
        'LANGC4F': 'fu_langc4f',
        'FTDC4FS': 'fu_ftdc4fs',
        'FTDC4FR': 'fu_ftdc4fr',
        'FTDC5FS': 'fu_ftdc5fs',
        'FTDC5FR': 'fu_ftdc5fr',
        'FTDC6FS': 'fu_ftdc6fs',
        'FTDC6FR': 'fu_ftdc6fr',
        'LANGE2F': 'fu_lange2f',
        'LANGE3F': 'fu_lange3f',
        'LANGCLS': 'fu_langcls',
        'CLSSUB': 'fu_clssub'
    }
    for key, value in z1x_field_mapping.items():
        if record[value].strip():
            setattr(z1x, key, record[value])
            z1x_filled_fields += 1

    z1 = fvp_forms.FormZ1()
    z1_filled_fields = 0
    z1_field_mapping = {
        'A2SUB': 'fu_a2_sub',
        'A2NOT': 'fu_a2_not',
        'A2COMM': 'fu_a2_comm',
        'A3SUB': 'fu_a3_sub',
        'A3NOT': 'fu_a3_not',
        'A3COMM': 'fu_a3_comm',
        'A4SUB': 'fu_a4_sub',
        'A4NOT': 'fu_a4_not',
        'A4COMM': 'fu_a4_comm',
        'B1SUB': 'fu_b1_sub',
        'B1NOT': 'fu_b1_not',
        'B1COMM': 'fu_b1_comm',
        'B5SUB': 'fu_b5_sub',
        'B5NOT': 'fu_b5_not',
        'B5COMM': 'fu_b5_comm',
        'B6SUB': 'fu_b6_sub',
        'B6NOT': 'fu_b6_not',
        'B6COMM': 'fu_b6_comm',
        'B7SUB': 'fu_b7_sub',
        'B7NOT': 'fu_b7_not',
        'B7COMM': 'fu_b7_comm'
    }
    for key, value in z1_field_mapping.items():
        if record[value].strip():
            setattr(z1, key, record[value])
            z1_filled_fields += 1

    # Prefer Z1X to Z1
    # If both are blank, use date (Z1X after 2018/04/02)
    if z1x_filled_fields > 0:
        packet.insert(0, z1x)
    elif z1_filled_fields > 0:
        packet.insert(0, z1)
    elif (int(record['visityr'])>2018) or (int(record['visityr'])==2018 and \
          int(record['visitmo'])>4) or (int(record['visityr'])==2018 and \
          int(record['visitmo'])==4 and int(record['visitday'])>=2):
        packet.insert(0, z1x)
    else:
        packet.insert(0, z1)


def add_a1(record, packet):
    a1 = fvp_forms.FormA1()
    a1.BIRTHMO   = record['fu_birthmo']
    a1.BIRTHYR   = record['fu_birthyr']
    a1.MARISTAT  = record['fu_maristat']
    a1.SEX       = record['fu_sex']
    a1.LIVSITUA  = record['fu_livsitua']
    a1.INDEPEND  = record['fu_independ']
    a1.RESIDENC  = record['fu_residenc']
    a1.ZIP       = record['fu_zip']
    packet.append(a1)


def add_a2(record, packet):
    a2 = fvp_forms.FormA2()
    a2.INBIRMO   = record['fu_inbirmo']
    a2.INBIRYR   = record['fu_inbiryr']
    a2.INSEX     = record['fu_insex']
    a2.NEWINF    = record['fu_newinf']
    a2.INHISP    = record['fu_inhisp']
    a2.INHISPOR  = record['fu_inhispor']
    a2.INHISPOX  = record['fu_inhispox']
    a2.INRACE    = record['fu_inrace']
    a2.INRACEX   = record['fu_inracex']
    a2.INRASEC   = record['fu_inrasec']
    a2.INRASECX  = record['fu_inrasecx']
    a2.INRATER   = record['fu_inrater']
    a2.INRATERX  = record['fu_inraterx']
    a2.INEDUC    = record['fu_ineduc']
    a2.INRELTO   = record['fu_inrelto']
    a2.INKNOWN   = record['fu_inknown']
    a2.INLIVWTH  = record['fu_inlivwth']
    a2.INVISITS  = record['fu_invisits']
    a2.INCALLS   = record['fu_incalls']
    a2.INRELY    = record['fu_inrely']
    packet.append(a2)


def add_a3(record, packet):
    a3 = fvp_forms.FormA3()
    a3.NWINFMUT  = record['fu_nwinfmut']
    a3.FADMUT    = record['fu_fadmut']
    a3.FADMUTX   = record['fu_fadmutx']
    a3.FADMUSO   = record['fu_fadmuso']
    a3.FADMUSOX  = record['fu_fadmusox']
    a3.FFTDMUT   = record['fu_fftdmut']
    a3.FFTDMUTX  = record['fu_fftdmutx']
    a3.FFTDMUSO  = record['fu_fftdmuso']
    a3.FFTDMUSX  = record['fu_fftdmusx']
    a3.FOTHMUT   = record['fu_fothmut']
    a3.FOTHMUTX  = record['fu_fothmutx']
    a3.FOTHMUSO  = record['fu_fothmuso']
    a3.FOTHMUSX  = record['fu_fothmusx']
    a3.NWINFPAR  = record['fu_nwinfpar']
    a3.MOMMOB    = record['fu_mommob']
    a3.MOMYOB    = record['fu_momyob']
    a3.MOMDAGE   = record['fu_momdage']
    a3.MOMNEUR   = record['fu_momneur']
    a3.MOMPRDX   = record['fu_momprdx']
    a3.MOMMOE    = record['fu_mommoe']
    a3.MOMAGEO   = record['fu_momageo']
    a3.DADMOB    = record['fu_dadmob']
    a3.DADYOB    = record['fu_dadyob']
    a3.DADDAGE   = record['fu_daddage']
    a3.DADNEUR   = record['fu_dadneur']
    a3.DADPRDX   = record['fu_dadprdx']
    a3.DADMOE    = record['fu_dadmoe']
    a3.DADAGEO   = record['fu_dadageo']
    a3.SIBS      = record['fu_sibs']
    a3.NWINFSIB  = record['fu_nwinfsib']
    a3.SIB1MOB   = record['fu_sib1mob']
    a3.SIB1YOB   = record['fu_sib1yob']
    a3.SIB1AGD   = record['fu_sib1agd']
    a3.SIB1NEU   = record['fu_sib1neu']
    a3.SIB1PDX   = record['fu_sib1pdx']
    a3.SIB1MOE   = record['fu_sib1moe']
    a3.SIB1AGO   = record['fu_sib1ago']
    a3.SIB2MOB   = record['fu_sib2mob']
    a3.SIB2YOB   = record['fu_sib2yob']
    a3.SIB2AGD   = record['fu_sib2agd']
    a3.SIB2NEU   = record['fu_sib2neu']
    a3.SIB2PDX   = record['fu_sib2pdx']
    a3.SIB2MOE   = record['fu_sib2moe']
    a3.SIB2AGO   = record['fu_sib2ago']
    a3.SIB3MOB   = record['fu_sib3mob']
    a3.SIB3YOB   = record['fu_sib3yob']
    a3.SIB3AGD   = record['fu_sib3agd']
    a3.SIB3NEU   = record['fu_sib3neu']
    a3.SIB3PDX   = record['fu_sib3pdx']
    a3.SIB3MOE   = record['fu_sib3moe']
    a3.SIB3AGO   = record['fu_sib3ago']
    a3.SIB4MOB   = record['fu_sib4mob']
    a3.SIB4YOB   = record['fu_sib4yob']
    a3.SIB4AGD   = record['fu_sib4agd']
    a3.SIB4NEU   = record['fu_sib4neu']
    a3.SIB4PDX   = record['fu_sib4pdx']
    a3.SIB4MOE   = record['fu_sib4moe']
    a3.SIB4AGO   = record['fu_sib4ago']
    a3.SIB5MOB   = record['fu_sib5mob']
    a3.SIB5YOB   = record['fu_sib5yob']
    a3.SIB5AGD   = record['fu_sib5agd']
    a3.SIB5NEU   = record['fu_sib5neu']
    a3.SIB5PDX   = record['fu_sib5pdx']
    a3.SIB5MOE   = record['fu_sib5moe']
    a3.SIB5AGO   = record['fu_sib5ago']
    a3.SIB6MOB   = record['fu_sib6mob']
    a3.SIB6YOB   = record['fu_sib6yob']
    a3.SIB6AGD   = record['fu_sib6agd']
    a3.SIB6NEU   = record['fu_sib6neu']
    a3.SIB6PDX   = record['fu_sib6pdx']
    a3.SIB6MOE   = record['fu_sib6moe']
    a3.SIB6AGO   = record['fu_sib6ago']
    a3.SIB7MOB   = record['fu_sib7mob']
    a3.SIB7YOB   = record['fu_sib7yob']
    a3.SIB7AGD   = record['fu_sib7agd']
    a3.SIB7NEU   = record['fu_sib7neu']
    a3.SIB7PDX   = record['fu_sib7pdx']
    a3.SIB7MOE   = record['fu_sib7moe']
    a3.SIB7AGO   = record['fu_sib7ago']
    a3.SIB8MOB   = record['fu_sib8mob']
    a3.SIB8YOB   = record['fu_sib8yob']
    a3.SIB8AGD   = record['fu_sib8agd']
    a3.SIB8NEU   = record['fu_sib8neu']
    a3.SIB8PDX   = record['fu_sib8pdx']
    a3.SIB8MOE   = record['fu_sib8moe']
    a3.SIB8AGO   = record['fu_sib8ago']
    a3.SIB9MOB   = record['fu_sib9mob']
    a3.SIB9YOB   = record['fu_sib9yob']
    a3.SIB9AGD   = record['fu_sib9agd']
    a3.SIB9NEU   = record['fu_sib9neu']
    a3.SIB9PDX   = record['fu_sib9pdx']
    a3.SIB9MOE   = record['fu_sib9moe']
    a3.SIB9AGO   = record['fu_sib9ago']
    a3.SIB10MOB  = record['fu_sib10mob']
    a3.SIB10YOB  = record['fu_sib10yob']
    a3.SIB10AGD  = record['fu_sib10agd']
    a3.SIB10NEU  = record['fu_sib10neu']
    a3.SIB10PDX  = record['fu_sib10pdx']
    a3.SIB10MOE  = record['fu_sib10moe']
    a3.SIB10AGO  = record['fu_sib10ago']
    a3.SIB11MOB  = record['fu_sib11mob']
    a3.SIB11YOB  = record['fu_sib11yob']
    a3.SIB11AGD  = record['fu_sib11agd']
    a3.SIB11NEU  = record['fu_sib11neu']
    a3.SIB11PDX  = record['fu_sib11pdx']
    a3.SIB11MOE  = record['fu_sib11moe']
    a3.SIB11AGO  = record['fu_sib11ago']
    a3.SIB12MOB  = record['fu_sib12mob']
    a3.SIB12YOB  = record['fu_sib12yob']
    a3.SIB12AGD  = record['fu_sib12agd']
    a3.SIB12NEU  = record['fu_sib12neu']
    a3.SIB12PDX  = record['fu_sib12pdx']
    a3.SIB12MOE  = record['fu_sib12moe']
    a3.SIB12AGO  = record['fu_sib12ago']
    a3.SIB13MOB  = record['fu_sib13mob']
    a3.SIB13YOB  = record['fu_sib13yob']
    a3.SIB13AGD  = record['fu_sib13agd']
    a3.SIB13NEU  = record['fu_sib13neu']
    a3.SIB13PDX  = record['fu_sib13pdx']
    a3.SIB13MOE  = record['fu_sib13moe']
    a3.SIB13AGO  = record['fu_sib13ago']
    a3.SIB14MOB  = record['fu_sib14mob']
    a3.SIB14YOB  = record['fu_sib14yob']
    a3.SIB14AGD  = record['fu_sib14agd']
    a3.SIB14NEU  = record['fu_sib14neu']
    a3.SIB14PDX  = record['fu_sib14pdx']
    a3.SIB14MOE  = record['fu_sib14moe']
    a3.SIB14AGO  = record['fu_sib14ago']
    a3.SIB15MOB  = record['fu_sib15mob']
    a3.SIB15YOB  = record['fu_sib15yob']
    a3.SIB15AGD  = record['fu_sib15agd']
    a3.SIB15NEU  = record['fu_sib15neu']
    a3.SIB15PDX  = record['fu_sib15pdx']
    a3.SIB15MOE  = record['fu_sib15moe']
    a3.SIB15AGO  = record['fu_sib15ago']
    a3.SIB16MOB  = record['fu_sib16mob']
    a3.SIB16YOB  = record['fu_sib16yob']
    a3.SIB16AGD  = record['fu_sib16agd']
    a3.SIB16NEU  = record['fu_sib16neu']
    a3.SIB16PDX  = record['fu_sib16pdx']
    a3.SIB16MOE  = record['fu_sib16moe']
    a3.SIB16AGO  = record['fu_sib16ago']
    a3.SIB17MOB  = record['fu_sib17mob']
    a3.SIB17YOB  = record['fu_sib17yob']
    a3.SIB17AGD  = record['fu_sib17agd']
    a3.SIB17NEU  = record['fu_sib17neu']
    a3.SIB17PDX  = record['fusib17pdx']
    a3.SIB17MOE  = record['fu_sib17moe']
    a3.SIB17AGO  = record['fu_sib17ago']
    a3.SIB18MOB  = record['fu_sib18mob']
    a3.SIB18YOB  = record['fu_sib18yob']
    a3.SIB18AGD  = record['fu_sib18agd']
    a3.SIB18NEU  = record['fu_sib18neu']
    a3.SIB18PDX  = record['fu_sib18pdx']
    a3.SIB18MOE  = record['fu_sib18moe']
    a3.SIB18AGO  = record['fu_sib18ago']
    a3.SIB19MOB  = record['fu_sib19mob']
    a3.SIB19YOB  = record['fu_sib19yob']
    a3.SIB19AGD  = record['fu_sib19agd']
    a3.SIB19NEU  = record['fu_sib19neu']
    a3.SIB19PDX  = record['fu_sib19pdx']
    a3.SIB19MOE  = record['fu_sib19moe']
    a3.SIB19AGO  = record['fu_sib19ago']
    a3.SIB20MOB  = record['fu_sib20mob']
    a3.SIB20YOB  = record['fu_sib20yob']
    a3.SIB20AGD  = record['fu_sib20agd']
    a3.SIB20NEU  = record['fu_sib20neu']
    a3.SIB20PDX  = record['fu_sib20pdx']
    a3.SIB20MOE  = record['fu_sib20moe']
    a3.SIB20AGO  = record['fu_sib20ago']
    a3.KIDS      = record['fu_kids']
    a3.NWINFKID  = record['fu_nwinfkid']
    a3.KID1MOB   = record['fu_kid1mob']
    a3.KID1YOB   = record['fu_kid1yob']
    a3.KID1AGD   = record['fu_kid1agd']
    a3.KID1NEU   = record['fu_kid1neu']
    a3.KID1PDX   = record['fu_kid1pdx']
    a3.KID1MOE   = record['fu_kid1moe']
    a3.KID1AGO   = record['fu_kid1ago']
    a3.KID2MOB   = record['fu_kid2mob']
    a3.KID2YOB   = record['fu_kid2yob']
    a3.KID2AGD   = record['fu_kid2agd']
    a3.KID2NEU   = record['fu_kid2neu']
    a3.KID2PDX   = record['fu_kid2pdx']
    a3.KID2MOE   = record['fu_kid2moe']
    a3.KID2AGO   = record['fu_kid2ago']
    a3.KID3MOB   = record['fu_kid3mob']
    a3.KID3YOB   = record['fu_kid3yob']
    a3.KID3AGD   = record['fu_kid3agd']
    a3.KID3NEU   = record['fu_kid3neu']
    a3.KID3PDX   = record['fu_kid3pdx']
    a3.KID3MOE   = record['fu_kid3moe']
    a3.KID3AGO   = record['fu_kid3ago']
    a3.KID4MOB   = record['fu_kid4mob']
    a3.KID4YOB   = record['fu_kid4yob']
    a3.KID4AGD   = record['fu_kid4agd']
    a3.KID4NEU   = record['fu_kid4neu']
    a3.KID4PDX   = record['fu_kid4pdx']
    a3.KID4MOE   = record['fu_kid4moe']
    a3.KID4AGO   = record['fu_kid4ago']
    a3.KID5MOB   = record['fu_kid5mob']
    a3.KID5YOB   = record['fu_kid5yob']
    a3.KID5AGD   = record['fu_kid5agd']
    a3.KID5NEU   = record['fu_kid5neu']
    a3.KID5PDX   = record['fu_kid5pdx']
    a3.KID5MOE   = record['fu_kid5moe']
    a3.KID5AGO   = record['fu_kid5ago']
    a3.KID6MOB   = record['fu_kid6mob']
    a3.KID6YOB   = record['fu_kid6yob']
    a3.KID6AGD   = record['fu_kid6agd']
    a3.KID6NEU   = record['fu_kid6neu']
    a3.KID6PDX   = record['fu_kid6pdx']
    a3.KID6MOE   = record['fu_kid6moe']
    a3.KID6AGO   = record['fu_kid6ago']
    a3.KID7MOB   = record['fu_kid7mob']
    a3.KID7YOB   = record['fu_kid7yob']
    a3.KID7AGD   = record['fu_kid7agd']
    a3.KID7NEU   = record['fu_kid7neu']
    a3.KID7PDX   = record['fu_kid7pdx']
    a3.KID7MOE   = record['fu_kid7moe']
    a3.KID7AGO   = record['fu_kid7ago']
    a3.KID8MOB   = record['fu_kid8mob']
    a3.KID8YOB   = record['fu_kid8yob']
    a3.KID8AGD   = record['fu_kid8agd']
    a3.KID8NEU   = record['fu_kid8neu']
    a3.KID8PDX   = record['fu_kid8pdx']
    a3.KID8MOE   = record['fu_kid8moe']
    a3.KID8AGO   = record['fu_kid8ago']
    a3.KID9MOB   = record['fu_kid9mob']
    a3.KID9YOB   = record['fu_kid9yob']
    a3.KID9AGD   = record['fukid9agd']
    a3.KID9NEU   = record['fu_kid9neu']
    a3.KID9PDX   = record['fu_kid9pdx']
    a3.KID9MOE   = record['fu_kid9moe']
    a3.KID9AGO   = record['fu_kid9ago']
    a3.KID10MOB  = record['fu_kid10mob']
    a3.KID10YOB  = record['fu_kid10yob']
    a3.KID10AGD  = record['fu_kid10agd']
    a3.KID10NEU  = record['fu_kid10neu']
    a3.KID10PDX  = record['fu_kid10pdx']
    a3.KID10MOE  = record['fu_kid10moe']
    a3.KID10AGO  = record['fu_kid10ago']
    a3.KID11MOB  = record['fu_kid11mob']
    a3.KID11YOB  = record['fu_kid11yob']
    a3.KID11AGD  = record['fu_kid11agd']
    a3.KID11NEU  = record['fu_kid11neu']
    a3.KID11PDX  = record['fu_kid11pdx']
    a3.KID11MOE  = record['fu_kid11moe']
    a3.KID11AGO  = record['fu_kid11ago']
    a3.KID12MOB  = record['fu_kid12mob']
    a3.KID12YOB  = record['fu_kid12yob']
    a3.KID12AGD  = record['fu_kid12agd']
    a3.KID12NEU  = record['fu_kid12neu']
    a3.KID12PDX  = record['fu_kid12pdx']
    a3.KID12MOE  = record['fu_kid12moe']
    a3.KID12AGO  = record['fu_kid12ago']
    a3.KID13MOB  = record['fu_kid13mob']
    a3.KID13YOB  = record['fu_kid13yob']
    a3.KID13AGD  = record['fu_kid13agd']
    a3.KID13NEU  = record['fu_kid13neu']
    a3.KID13PDX  = record['fu_kid13pdx']
    a3.KID13MOE  = record['fu_kid13moe']
    a3.KID13AGO  = record['fu_kid13ago']
    a3.KID14MOB  = record['fu_kid14mob']
    a3.KID14YOB  = record['fu_kid14yob']
    a3.KID14AGD  = record['fu_kid14agd']
    a3.KID14NEU  = record['fu_kid14neu']
    a3.KID14PDX  = record['fu_kid14pdx']
    a3.KID14MOE  = record['fu_kid14moe']
    a3.KID14AGO  = record['fu_kid14ago']
    a3.KID15MOB  = record['fu_kid15mob']
    a3.KID15YOB  = record['fu_kid15yob']
    a3.KID15AGD  = record['fu_kid15agd']
    a3.KID15NEU  = record['fu_kid15neu']
    a3.KID15PDX  = record['fu_kid15pdx']
    a3.KID15MOE  = record['fu_kid15moe']
    a3.KID15AGO  = record['fu_kid15ago']
    packet.append(a3)


def add_a4(record, packet):
    # Form A4D and A4G are special in that our REDCap implementation (FVP A4)
    # combines them by asking if the subject is taking any medications (which
    # corresponds to A4G.ANYMEDS), then has 50 fields to specify each
    # medication used, which we turn each one into a FormA4D object.
    a4g = fvp_forms.FormA4G()
    a4g.ANYMEDS = record['fu_anymeds']
    packet.append(a4g)

    for i in range(1, 51):
            key = 'fu_drugid_' + str(i)
            if record[key]:
                a4d = fvp_forms.FormA4D()
                a4d.DRUGID = record[key]
                packet.append(a4d)


def add_b1(record, packet):
    b1 = fvp_forms.FormB1()
    b1.HEIGHT    = record['fu_height']
    b1.WEIGHT    = record['fu_weight']
    b1.BPSYS     = record['fu_bpsys']
    b1.BPDIAS    = record['fu_bpdias']
    b1.HRATE     = record['fu_hrate']
    b1.VISION    = record['fu_vision']
    b1.VISCORR   = record['fu_viscorr']
    b1.VISWCORR  = record['fu_viswcorr']
    b1.HEARING   = record['fu_hearing']
    b1.HEARAID   = record['fu_hearaid']
    b1.HEARWAID  = record['fu_hearwaid']
    packet.append(b1)


def add_b4(record, packet):
    b4 = fvp_forms.FormB4()
    b4.MEMORY    = record['fu_memory']
    b4.ORIENT    = record['fu_orient']
    b4.JUDGMENT  = record['fu_judgment']
    b4.COMMUN    = record['fu_commun']
    b4.HOMEHOBB  = record['fu_homehobb']
    b4.PERSCARE  = record['fu_perscare']
    b4.CDRSUM    = record['fu_cdrsum']
    b4.CDRGLOB   = record['fu_cdrglob']
    b4.COMPORT   = record['fu_comport']
    b4.CDRLANG   = record['fu_cdrlang']
    packet.append(b4)


def add_b5(record, packet):
    b5 = fvp_forms.FormB5()
    b5.NPIQINF   = record['fu_npiqinf']
    b5.NPIQINFX  = record['fu_npiqinfx']
    b5.DEL       = record['fu_del']
    b5.DELSEV    = record['fu_delsev']
    b5.HALL      = record['fu_hall']
    b5.HALLSEV   = record['fu_hallsev']
    b5.AGIT      = record['fu_agit']
    b5.AGITSEV   = record['fu_agitsev']
    b5.DEPD      = record['fu_depd']
    b5.DEPDSEV   = record['fu_depdsev']
    b5.ANX       = record['fu_anx']
    b5.ANXSEV    = record['fu_anxsev']
    b5.ELAT      = record['fu_elat']
    b5.ELATSEV   = record['fu_elatsev']
    b5.APA       = record['fu_apa']
    b5.APASEV    = record['fu_apasev']
    b5.DISN      = record['fu_disn']
    b5.DISNSEV   = record['fu_disnsev']
    b5.IRR       = record['fu_irr']
    b5.IRRSEV    = record['fu_irrsev']
    b5.MOT       = record['fu_mot']
    b5.MOTSEV    = record['fu_motsev']
    b5.NITE      = record['fu_nite']
    b5.NITESEV   = record['fu_nitesev']
    b5.APP       = record['fu_app']
    b5.APPSEV    = record['fu_appsev']
    packet.append(b5)


def add_b6(record, packet):
    b6 = fvp_forms.FormB6()
    b6.NOGDS     = record['fu_nogds']
    b6.SATIS     = record['fu_satis']
    b6.DROPACT   = record['fu_dropact']
    b6.EMPTY     = record['fu_empty']
    b6.BORED     = record['fu_bored']
    b6.SPIRITS   = record['fu_spirits']
    b6.AFRAID    = record['fu_afraid']
    b6.HAPPY     = record['fu_happy']
    b6.HELPLESS  = record['fu_helpless']
    b6.STAYHOME  = record['fu_stayhome']
    b6.MEMPROB   = record['fu_memprob']
    b6.WONDRFUL  = record['fu_wondrful']
    b6.WRTHLESS  = record['fu_wrthless']
    b6.ENERGY    = record['fu_energy']
    b6.HOPELESS  = record['fu_hopeless']
    b6.BETTER    = record['fu_better']
    b6.GDS       = record['fu_gds']
    packet.append(b6)


def add_b7(record, packet):
    b7 = fvp_forms.FormB7()
    b7.BILLS     = record['fu_bills']
    b7.TAXES     = record['fu_taxes']
    b7.SHOPPING  = record['fu_shopping']
    b7.GAMES     = record['fu_games']
    b7.STOVE     = record['fu_stove']
    b7.MEALPREP  = record['fu_mealprep']
    b7.EVENTS    = record['fu_events']
    b7.PAYATTN   = record['fu_payattn']
    b7.REMDATES  = record['fu_remdates']
    b7.TRAVEL    = record['fu_travel']
    packet.append(b7)


def add_b8(record, packet):
    b8 = fvp_forms.FormB8()
    b8.NORMEXAM  = record['fu_normexam']
    b8.PARKSIGN  = record['fu_parksign']
    b8.RESTTRL   = record['fu_resttrl']
    b8.RESTTRR   = record['fu_resttrr']
    b8.SLOWINGL  = record['fu_slowingl']
    b8.SLOWINGR  = record['fu_slowingr']
    b8.RIGIDL    = record['fu_rigidl']
    b8.RIGIDR    = record['fu_rigidr']
    b8.BRADY     = record['fu_brady']
    b8.PARKGAIT  = record['fu_parkgait']
    b8.POSTINST  = record['fu_postinst']
    b8.CVDSIGNS  = record['fu_cvdsigns']
    b8.CORTDEF   = record['fu_cortdef']
    b8.SIVDFIND  = record['fu_sivdfind']
    b8.CVDMOTL   = record['fu_cvdmotl']
    b8.CVDMOTR   = record['fu_cvdmotr']
    b8.CORTVISL  = record['fu_cortvisl']
    b8.CORTVISR  = record['fu_cortvisr']
    b8.SOMATL    = record['fu_somatl']
    b8.SOMATR    = record['fu_somatr']
    b8.POSTCORT  = record['fu_postcort']
    b8.PSPCBS    = record['fu_pspcbs']
    b8.EYEPSP    = record['fu_eyepsp']
    b8.DYSPSP    = record['fu_dyspsp']
    b8.AXIALPSP  = record['fu_axialpsp']
    b8.GAITPSP   = record['fu_gaitpsp']
    b8.APRAXSP   = record['fu_apraxsp']
    b8.APRAXL    = record['fu_apraxl']
    b8.APRAXR    = record['fu_apraxr']
    b8.CORTSENL  = record['fu_cortsenl']
    b8.CORTSENR  = record['fu_cortsenr']
    b8.ATAXL     = record['fu_ataxl']
    b8.ATAXR     = record['fu_ataxr']
    b8.ALIENLML  = record['fu_alienlml']
    b8.ALIENLMR  = record['fu_alienlmr']
    b8.DYSTONL   = record['fu_dystonl']
    b8.DYSTONR   = record['fu_dystonr']
    b8.ALSFIND   = record['fu_alsfind']
    b8.GAITNPH   = record['fu_gaitnph']
    b8.OTHNEUR   = record['fu_othneur']
    b8.OTHNEURX  = record['fu_othneurx']
    packet.append(b8)


def add_b9(record, packet):
    b9 = fvp_forms.FormB9()
    b9.DECSUB    = record['fu_decsub']
    b9.DECIN     = record['fu_decin']
    b9.DECCLCOG  = record['fu_decclcog']
    b9.COGMEM    = record['fu_cogmem']
    b9.COGORI    = record['fu_cogori']
    b9.COGJUDG   = record['fu_cogjudg']
    b9.COGLANG   = record['fu_coglang']
    b9.COGVIS    = record['fu_cogvis']
    b9.COGATTN   = record['fu_cogattn']
    b9.COGFLUC   = record['fu_cogfluc']
    b9.COGFLAGO  = record['fu_cogflago']
    b9.COGOTHR   = record['fu_cogothr']
    b9.COGOTHRX  = record['fu_cogothrx']
    b9.COGFPRED  = record['fu_cogfpred']
    b9.COGFPREX  = record['fu_cogfprex']
    b9.COGMODE   = record['fu_cogmode']
    b9.COGMODEX  = record['fu_cogmodex']
    b9.DECAGE    = record['fu_decage']
    b9.DECCLBE   = record['fu_decclbe']
    b9.BEAPATHY  = record['fu_beapathy']
    b9.BEDEP     = record['fu_bedep']
    b9.BEVHALL   = record['fu_bevhall']
    b9.BEVWELL   = record['fu_bevwell']
    b9.BEVHAGO   = record['fu_bevhago']
    b9.BEAHALL   = record['fu_beahall']
    b9.BEDEL     = record['fu_bedel']
    b9.BEDISIN   = record['fu_bedisin']
    b9.BEIRRIT   = record['fu_beirrit']
    b9.BEAGIT    = record['fu_beagit']
    b9.BEPERCH   = record['fu_beperch']
    b9.BEREM     = record['fu_berem']
    b9.BEREMAGO  = record['fu_beremago']
    b9.BEANX     = record['fu_beanx']
    b9.BEOTHR    = record['fu_beothr']
    b9.BEOTHRX   = record['fu_beothrx']
    b9.BEFPRED   = record['fu_befpred']
    b9.BEFPREDX  = record['fu_befpredx']
    b9.BEMODE    = record['fu_bemode']
    b9.BEMODEX   = record['fu_bemodex']
    b9.BEAGE     = record['fu_beage']
    b9.DECCLMOT  = record['fu_decclmot']
    b9.MOGAIT    = record['fu_mogait']
    b9.MOFALLS   = record['fu_mofalls']
    b9.MOTREM    = record['fu_motrem']
    b9.MOSLOW    = record['fu_moslow']
    b9.MOFRST    = record['fu_mofrst']
    b9.MOMODE    = record['fu_momode']
    b9.MOMODEX   = record['fu_momodex']
    b9.MOMOPARK  = record['fu_momopark']
    b9.PARKAGE   = record['fu_parkage']
    b9.MOMOALS   = record['fu_momoals']
    b9.ALSAGE    = record['fu_alsage']
    b9.MOAGE     = record['fu_moage']
    b9.COURSE    = record['fu_course']
    b9.FRSTCHG   = record['fu_frstchg']
    b9.LBDEVAL   = record['fu_lbdeval']
    b9.FTLDEVAL  = record['fu_ftldeval']
    packet.append(b9)


def add_c1s_or_c2(record, packet):
    c2 = fvp_forms.FormC2()
    c2_filled_fields = 0
    c2_field_mapping = {
        'MOCACOMP': 'fu_mocacomp',
        'MOCAREAS': 'fu_mocareas',
        'MOCALOC': 'fu_mocaloc',
        'MOCALAN': 'fu_mocalan',
        'MOCALANX': 'fu_mocalanx',
        'MOCAVIS': 'fu_mocavis',
        'MOCAHEAR': 'fu_mocahear',
        'MOCATOTS': 'fu_mocatots',
        'MOCATRAI': 'fu_mocatrai',
        'MOCACUBE': 'fu_mocacube',
        'MOCACLOC': 'fu_mocacloc',
        'MOCACLON': 'fu_mocaclon',
        'MOCACLOH': 'fu_mocacloh',
        'MOCANAMI': 'fu_mocanami',
        'MOCAREGI': 'fu_mocaregi',
        'MOCADIGI': 'fu_mocadigi',
        'MOCALETT': 'fu_mocalett',
        'MOCASER7': 'fu_mocaser7',
        'MOCAREPE': 'fu_mocarepe',
        'MOCAFLUE': 'fu_mocaflue',
        'MOCAABST': 'fu_mocaabst',
        'MOCARECN': 'fu_mocarecn',
        'MOCARECC': 'fu_mocarecc',
        'MOCARECR': 'fu_mocarecr',
        'MOCAORDT': 'fu_mocaordt',
        'MOCAORMO': 'fu_mocaormo',
        'MOCAORYR': 'fu_mocaoryr',
        'MOCAORDY': 'fu_mocaordy',
        'MOCAORPL': 'fu_mocaorpl',
        'MOCAORCT': 'fu_mocaorct',
        'NPSYCLOC': 'fu_npsycloc_c2',
        'NPSYLAN': 'fu_npsylan_c2',
        'NPSYLANX': 'fu_npsylanx_c2',
        'CRAFTVRS': 'fu_craftvrs',
        'CRAFTURS': 'fu_crafturs',
        'UDSBENTC': 'fu_udsbentc',
        'DIGFORCT': 'fu_digforct',
        'DIGFORSL': 'fu_digforsl',
        'DIGBACCT': 'fu_digbacct',
        'DIGBACLS': 'fu_digbacls',
        'ANIMALS': 'fu_animals_c2',
        'VEG': 'fu_veg_c2',
        'TRAILA': 'fu_traila_c2',
        'TRAILARR': 'fu_trailarr_c2',
        'TRAILALI': 'fu_trailali_c2',
        'TRAILB': 'fu_trailb_c2',
        'TRAILBRR': 'fu_trailbrr_c2',
        'TRAILBLI': 'fu_trailbli_c2',
        'CRAFTDVR': 'fu_craftdvr',
        'CRAFTDRE': 'fu_craftdre',
        'CRAFTDTI': 'fu_craftdti',
        'CRAFTCUE': 'fu_craftcue',
        'UDSBENTD': 'fu_udsbentd',
        'UDSBENRS': 'fu_udsbenrs',
        'MINTTOTS': 'fu_minttots',
        'MINTTOTW': 'fu_minttotw',
        'MINTSCNG': 'fu_mintscng',
        'MINTSCNC': 'fu_mintscnc',
        'MINTPCNG': 'fu_mintpcng',
        'MINTPCNC': 'fu_mintpcnc',
        'UDSVERFC': 'fu_udsverfc',
        'UDSVERFN': 'fu_udsverfn',
        'UDSVERNF': 'fu_udsvernf',
        'UDSVERLC': 'fu_udsverlc',
        'UDSVERLR': 'fu_udsverlr',
        'UDSVERLN': 'fu_udsverln',
        'UDSVERTN': 'fu_udsvertn',
        'UDSVERTE': 'fu_udsverte',
        'UDSVERTI': 'fu_udsverti',
        'COGSTAT': 'fu_cogstat_c2'
    }
    for key, value in c2_field_mapping.items():
        if record[value].strip():
            setattr(c2, key, record[value])
            c2_filled_fields += 1

    c1s = fvp_forms.FormC1S()
    c1s_filled_fields = 0
    c1s_field_mapping = {
        'MMSECOMP': 'fu_mmsecomp',
        'MMSEREAS': 'fu_mmsereas',
        'MMSELOC': 'fu_mmseloc',
        'MMSELAN': 'fu_mmselan',
        'MMSELANX': 'fu_mmselanx',
        'MMSEVIS': 'fu_mmsevis',
        'MMSEHEAR':  'fu_mmsehear',
        'MMSEORDA': 'fu_mmseorda',
        'MMSEORLO': 'fu_mmseorlo',
        'PENTAGON': 'fu_pentagon',
        'MMSE': 'fu_mmse',
        'NPSYCLOC': 'fu_npsycloc',
        'NPSYLAN': 'fu_npsylan',
        'NPSYLANX': 'fu_npsylanx',
        'LOGIMO': 'fu_logimo',
        'LOGIDAY': 'fu_logiday', 
        'LOGIYR': 'fu_logiyr', 
        'LOGIPREV': 'fu_logiprev',
        'LOGIMEM': 'fu_logimem',
        'UDSBENTC': 'fu_udsbentc_c1', 
        'DIGIF': 'fu_digif',
        'DIGIFLEN': 'fu_digiflen',
        'DIGIB': 'fu_digib',
        'DIGIBLEN': 'fu_digiblen',
        'ANIMALS': 'fu_animals',
        'VEG': 'fu_veg',
        'TRAILA': 'fu_traila',
        'TRAILARR': 'fu_trailarr',
        'TRAILALI': 'fu_trailali',
        'TRAILB': 'fu_trailb',
        'TRAILBRR': 'fu_trailbrr',
        'TRAILBLI': 'fu_trailbli',
        'MEMUNITS': 'fu_memunits',
        'MEMTIME': 'fu_memtime',
        'UDSBENTD': 'fu_udsbentd_c1', 
        'UDSBENRS': 'fu_udsbenrs_c1', 
        'BOSTON': 'fu_boston',
        'UDSVERFC': 'fu_udsverfc_c1', 
        'UDSVERFN': 'fu_udsverfn_c1', 
        'UDSVERNF': 'fu_udsvernf_c1', 
        'UDSVERLC': 'fu_udsverlc_c1', 
        'UDSVERLR': 'fu_udsverlr_c1', 
        'UDSVERLN': 'fu_udsverln_c1', 
        'UDSVERTN': 'fu_udsvertn_c1', 
        'UDSVERTE': 'fu_udsverte_c1', 
        'UDSVERTI': 'fu_udsverti_c1', 
        'COGSTAT': 'fu_cogstat'
    }
    for key, value in c1s_field_mapping.items():
        if record[value].strip():
            setattr(c1s, key, record[value])
            c1s_filled_fields += 1

    # Prefer C2 to C1S
    # If both are blank, use date (C2 after 2017/10/23)
    if c2_filled_fields > 0:
        packet.insert(0, c2)
    elif c1s_filled_fields > 0:
        packet.insert(0, c1s)
    elif (int(record['visityr'])>2017) or (int(record['visityr'])==2017 and \
          int(record['visitmo'])>10) or (int(record['visityr'])==2017 and \
          int(record['visitmo'])==10 and int(record['visitday'])>=23):
        packet.insert(0, c2)
    else:
        packet.insert(0, c1s)


def add_d1(record, packet):
    d1 = fvp_forms.FormD1()
    d1.DXMETHOD  = record['fu_dxmethod']
    d1.NORMCOG   = record['fu_normcog']
    d1.DEMENTED  = record['fu_demented']
    d1.AMNDEM    = record['fu_amndem']
    d1.PCA       = record['fu_pca']
    d1.PPASYN    = record['fu_ppasyn']
    d1.PPASYNT   = record['fu_ppasynt']
    d1.FTDSYN    = record['fu_ftdsyn']
    d1.LBDSYN    = record['fu_lbdsyn']
    d1.NAMNDEM   = record['fu_namndem']
    d1.MCIAMEM   = record['fu_mciamem']
    d1.MCIAPLUS  = record['fu_mciaplus']
    d1.MCIAPLAN  = record['fu_mciaplan']
    d1.MCIAPATT  = record['fu_mciapatt']
    d1.MCIAPEX   = record['fu_mciapex']
    d1.MCIAPVIS  = record['fu_mciapvis']
    d1.MCINON1   = record['fu_mcinon1']
    d1.MCIN1LAN  = record['fu_mcin1lan']
    d1.MCIN1ATT  = record['fu_mcin1att']
    d1.MCIN1EX   = record['fu_mcin1ex']
    d1.MCIN1VIS  = record['fu_mcin1vis']
    d1.MCINON2   = record['fu_mcinon2']
    d1.MCIN2LAN  = record['fu_mcin2lan']
    d1.MCIN2ATT  = record['fu_mcin2att']
    d1.MCIN2EX   = record['fu_mcin2ex']
    d1.MCIN2VIS  = record['fu_mcin2vis']
    d1.IMPNOMCI  = record['fu_impnomci']
    d1.AMYLPET   = record['fu_amylpet']
    d1.AMYLCSF   = record['fu_amylcsf']
    d1.FDGAD     = record['fu_fdgad']
    d1.HIPPATR   = record['fu_hippatr']
    d1.TAUPETAD  = record['fu_taupetad']
    d1.CSFTAU    = record['fu_csftau']
    d1.FDGFTLD   = record['fu_fdgftld']
    d1.TPETFTLD  = record['fu_tpetftld']
    d1.MRFTLD    = record['fu_mrftld']
    d1.DATSCAN   = record['fu_datscan']
    d1.OTHBIOM   = record['fu_othbiom']
    d1.OTHBIOMX  = record['fu_othbiomx']
    d1.IMAGLINF  = record['fu_imaglinf']
    d1.IMAGLAC   = record['fu_imaglac']
    d1.IMAGMACH  = record['fu_imagmach']
    d1.IMAGMICH  = record['fu_imagmich']
    d1.IMAGMWMH  = record['fu_imagmwmh']
    d1.IMAGEWMH  = record['fu_imagewmh']
    d1.ADMUT     = record['fu_admut']
    d1.FTLDMUT   = record['fu_ftldmut']
    d1.OTHMUT    = record['fu_othmut']
    d1.OTHMUTX   = record['fu_othmutx']
    d1.ALZDIS    = record['fu_alzdis']
    d1.ALZDISIF  = record['fu_alzdisif']
    d1.LBDIS     = record['fu_lbdis']
    d1.LBDIF     = record['fu_lbdif']
    d1.PARK      = record['fu_park']
    d1.MSA       = record['fu_msa']
    d1.MSAIF     = record['fu_msaif']
    d1.PSP       = record['fu_psp']
    d1.PSPIF     = record['fu_pspif']
    d1.CORT      = record['fu_cort']
    d1.CORTIF    = record['fu_cortif']
    d1.FTLDMO    = record['fu_ftldmo']
    d1.FTLDMOIF  = record['fu_ftldmoif']
    d1.FTLDNOS   = record['fu_ftldnos']
    d1.FTLDNOIF  = record['fu_ftldnoif']
    d1.FTLDSUBT  = record['fu_ftldsubt']
    d1.FTLDSUBX  = record['fu_ftldsubx']
    d1.CVD       = record['fu_cvd']
    d1.CVDIF     = record['fu_cvdif']
    d1.PREVSTK   = record['fu_prevstk']
    d1.STROKDEC  = record['fu_strokdec']
    d1.STKIMAG   = record['fu_stkimag']
    d1.INFNETW   = record['fu_infnetw']
    d1.INFWMH    = record['fu_infwmh']
    d1.ESSTREM   = record['fu_esstrem']
    d1.ESSTREIF  = record['fu_esstreif']
    d1.DOWNS     = record['fu_downs']
    d1.DOWNSIF   = record['fu_downsif']
    d1.HUNT      = record['fu_hunt']
    d1.HUNTIF    = record['fu_huntif']
    d1.PRION     = record['fu_prion']
    d1.PRIONIF   = record['fu_prionif']
    d1.BRNINJ    = record['fu_brninj']
    d1.BRNINJIF  = record['fu_brninjif']
    d1.BRNINCTE  = record['fu_brnincte']
    d1.HYCEPH    = record['fu_hyceph']
    d1.HYCEPHIF  = record['fu_hycephif']
    d1.EPILEP    = record['fu_epilep']
    d1.EPILEPIF  = record['fu_epilepif']
    d1.NEOP      = record['fu_neop']
    d1.NEOPIF    = record['fu_neopif']
    d1.NEOPSTAT  = record['fu_neopstat']
    d1.HIV       = record['fu_hiv']
    d1.HIVIF     = record['fu_hivif']
    d1.OTHCOG    = record['fu_othcog']
    d1.OTHCOGIF  = record['fu_othcogif']
    d1.OTHCOGX   = record['fu_othcogx']
    d1.DEP       = record['fu_dep']
    d1.DEPIF     = record['fu_depif']
    d1.DEPTREAT  = record['fu_deptreat']
    d1.BIPOLDX   = record['fu_bipoldx']
    d1.BIPOLDIF  = record['fu_bipoldif']
    d1.SCHIZOP   = record['fu_schizop']
    d1.SCHIZOIF  = record['fu_schizoif']
    d1.ANXIET    = record['fu_anxiet']
    d1.ANXIETIF  = record['fu_anxietif']
    d1.DELIR     = record['fu_delir']
    d1.DELIRIF   = record['fu_delirif']
    d1.PTSDDX    = record['fu_ptsddx']
    d1.PTSDDXIF  = record['fu_ptsddxif']
    d1.OTHPSY    = record['fu_othpsy']
    d1.OTHPSYIF  = record['fu_othpsyif']
    d1.OTHPSYX   = record['fu_othpsyx']
    d1.ALCDEM    = record['fu_alcdem']
    d1.ALCDEMIF  = record['fu_alcdemif']
    d1.ALCABUSE  = record['fu_alcabuse']
    d1.IMPSUB    = record['fu_impsub']
    d1.IMPSUBIF  = record['fu_impsubif']
    d1.DYSILL    = record['fu_dysill']
    d1.DYSILLIF  = record['fu_dysillif']
    d1.MEDS      = record['fu_meds']
    d1.MEDSIF    = record['fu_medsif']
    d1.COGOTH    = record['fu_cogoth']
    d1.COGOTHIF  = record['fu_cogothif']
    d1.COGOTHX   = record['fu_cogothx']
    d1.COGOTH2   = record['fu_cogoth2']
    d1.COGOTH2F  = record['fu_cogoth2f']
    d1.COGOTH2X  = record['fu_cogoth2x']
    d1.COGOTH3   = record['fu_cogoth3']
    d1.COGOTH3F  = record['fu_cogoth3f']
    d1.COGOTH3X  = record['fu_cogoth3x']
    packet.append(d1)


def add_d2(record, packet):
    d2 = fvp_forms.FormD2()
    d2.CANCER    = record['fu_cancer']
    d2.CANCSITE  = record['fu_cancsite']
    d2.DIABET    = record['fu_diabet']
    d2.MYOINF    = record['fu_myoinf']
    d2.CONGHRT   = record['fu_conghrt']
    d2.AFIBRILL  = record['fu_afibrill']
    d2.HYPERT    = record['fu_hypert']
    d2.ANGINA    = record['fu_angina']
    d2.HYPCHOL   = record['fu_hypchol']
    d2.VB12DEF   = record['fu_vb12def']
    d2.THYDIS    = record['fu_thydis']
    d2.ARTH      = record['fu_arth']
    d2.ARTYPE    = record['fu_artype']
    d2.ARTYPEX   = record['fu_artypex']
    d2.ARTUPEX   = record['fu_artupex']
    d2.ARTLOEX   = record['fu_artloex']
    d2.ARTSPIN   = record['fu_artspin']
    d2.ARTUNKN   = record['fu_artunkn']
    d2.URINEINC  = record['fu_urineinc']
    d2.BOWLINC   = record['fu_bowlinc']
    d2.SLEEPAP   = record['fu_sleepap']
    d2.REMDIS    = record['fu_remdis']
    d2.HYPOSOM   = record['fu_hyposom']
    d2.SLEEPOTH  = record['fu_sleepoth']
    d2.SLEEPOTX  = record['fu_sleepotx']
    d2.ANGIOCP   = record['fu_angiocp']
    d2.ANGIOPCI  = record['fu_angiopci']
    d2.PACEMAKE  = record['fu_pacemake']
    d2.HVALVE    = record['fu_hvalve']
    d2.ANTIENC   = record['fu_antienc']
    d2.ANTIENCX  = record['fu_antiencx']
    d2.OTHCOND   = record['fu_othcond']
    d2.OTHCONDX  = record['fu_othcondx']
    packet.append(d2)


def update_header(record, packet):
    for header in packet:
        header.PACKET = "F"
        header.FORMID = header.form_name
        if header.FORMID.value == "B5 ":
            header.FORMVER = "3.1"
        else:
            header.FORMVER = 3
        header.ADCID = record['adcid']
        header.PTID = record['ptid']
        header.VISITMO = record['visitmo']
        header.VISITDAY = record['visitday']
        header.VISITYR = record['visityr']
        header.VISITNUM = record['visitnum']
        header.INITIALS = record['initials']