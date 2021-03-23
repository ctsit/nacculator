###############################################################################
# Copyright 2015-2021 University of Florida. All rights reserved.
# This file is part of UF CTS-IT's NACCulator project.
# Use of this source code is governed by the license found in the LICENSE file.
###############################################################################

import sys

from nacc.uds3.tfp.v3_2 import forms as tfp_new_forms
from nacc.uds3 import clsform
from nacc.uds3 import packet as tfp_new_packet


def build_uds3_tfp_new_form(record, err=sys.stderr):
    """ Converts REDCap CSV data into a packet (list of TFP V3.2 Form objects) """
    packet = tfp_new_packet.Packet()

    # Set up the forms
    add_z1x(record, packet)
    add_t1(record, packet)
    add_a1(record, packet)
    add_a2(record, packet)
    try:
        z1x_complete = record['tvp_z1x_checklist_complete']
    except KeyError:
        try:
            z1x_complete = record['tfp_z1x_complete']
        except KeyError:
            try:
                z1x_complete = record['tele_z1x_complete']
            except KeyError:
                z1x_complete = '0'
    if z1x_complete in ['1', '2']:
        try:
            if record['tele_a3sub'] == '1':
                add_a3(record, packet)
        except KeyError:
            pass
        try:
            if record['tele_a4sub'] == '1':
                add_a4(record, packet)
        except KeyError:
            pass
        add_b4(record, packet)
        try:
            if record['tele_b5sub'] == '1':
                add_b5(record, packet)
        except KeyError:
            pass
        try:
            if record['tele_b6sub'] == '1':
                add_b6(record, packet)
        except KeyError:
            pass
        try:
            if record['tele_b7sub'] == '1':
                add_b7(record, packet)
        except KeyError:
            pass
        add_b9(record, packet)
        try:
            if record['tele_c2sub'] == '1':
                add_c2t(record, packet)
        except KeyError:
            pass
    add_d1(record, packet)
    add_d2(record, packet)
    try:
        clsform.add_cls(record, packet, tfp_new_forms)
    except KeyError:
        pass
    update_header(record, packet)

    return packet


def add_z1x(record, packet):
    # Forms T1, A1, A5, B4, B9, C2T, D1, and D2 are all REQUIRED.
    z1x = tfp_new_forms.FormZ1X()
    z1x.LANGT1  = record['tele_langt1']
    z1x.LANGA1  = record['tele_langa1']
    z1x.LANGA2  = record['tele_langa2']
    z1x.LANGA3  = record['tele_langa3']
    z1x.A3SUB   = record['tele_a3sub']
    z1x.LANGA4  = record['tele_langa4']
    z1x.A4SUB   = record['tele_a4sub']
    z1x.A4NOT   = record['tele_a4not']
    z1x.LANGB4  = record['tele_langb4']
    z1x.LANGB5  = record['tele_langb5']
    z1x.B5SUB   = record['tele_b5sub']
    z1x.B5NOT   = record['tele_b5not']
    z1x.LANGB6  = record['tele_langb6']
    z1x.B6SUB   = record['tele_b6sub']
    z1x.B6NOT   = record['tele_b6not']
    z1x.LANGB7  = record['tele_langb7']
    z1x.B7SUB   = record['tele_b7sub']
    z1x.B7NOT   = record['tele_b7not']
    z1x.LANGB9  = record['tele_langb9']
    z1x.C2SUB   = record['tele_c2sub']
    z1x.C2NOT   = record['tele_c2not']
    z1x.LANGD1  = record['tele_langd1']
    z1x.LANGD2  = record['tele_langd2']
    z1x.LANGCLS = record['tele_langcls']
    z1x.CLSSUB  = record['tele_clssub']
    packet.insert(0, z1x)


def add_t1(record, packet):
    t1 = tfp_new_forms.FormT1()
    t1.TELCOG   = record['TELCOG'.lower()]
    t1.TELILL   = record['TELILL'.lower()]
    t1.TELHOME  = record['TELHOME'.lower()]
    t1.TELREFU  = record['TELREFU'.lower()]
    t1.TELCOV   = record['TELCOV'.lower()]
    t1.TELOTHR  = record['TELOTHR'.lower()]
    t1.TELOTHRX = record['TELOTHRX'.lower()]
    t1.TELMOD   = record['TELMOD'.lower()]
    t1.TELINPER = record['TELINPER'.lower()]
    t1.TELMILE  = record['TELMILE'.lower()]
    packet.append(t1)


def add_a1(record, packet):
    a1 = tfp_new_forms.FormA1()
    a1.BIRTHMO   = record['tele_birthmo']
    a1.BIRTHYR   = record['tele_birthyr']
    a1.MARISTAT  = record['tele_maristat']
    a1.SEX       = record['tele_sex']
    a1.LIVSITUA  = record['tele_livsitua']
    a1.INDEPEND  = record['tele_independ']
    a1.RESIDENC  = record['tele_residenc']
    a1.ZIP       = record['tele_zip']
    packet.append(a1)


def add_a2(record, packet):
    a2 = tfp_new_forms.FormA2()
    a2.INBIRMO   = record['tele_inbirmo']
    a2.INBIRYR   = record['tele_inbiryr']
    a2.INSEX     = record['tele_insex']
    a2.NEWINF    = record['tele_newinf']
    a2.INHISP    = record['tele_inhisp']
    a2.INHISPOR  = record['tele_inhispor']
    a2.INHISPOX  = record['tele_inhispox']
    a2.INRACE    = record['tele_inrace']
    a2.INRACEX   = record['tele_inracex']
    a2.INRASEC   = record['tele_inrasec']
    a2.INRASECX  = record['tele_inrasecx']
    a2.INRATER   = record['tele_inrater']
    a2.INRATERX  = record['tele_inraterx']
    a2.INEDUC    = record['tele_ineduc']
    a2.INRELTO   = record['tele_inrelto']
    a2.INKNOWN   = record['tele_inknown']
    a2.INLIVWTH  = record['tele_inlivwth']
    a2.INVISITS  = record['tele_invisits']
    a2.INCALLS   = record['tele_incalls']
    a2.INRELY    = record['tele_inrely']
    packet.append(a2)


def add_a3(record, packet):
    a3 = tfp_new_forms.FormA3()
    a3.NWINFMUT  = record['tele_nwinfmut']
    a3.FADMUT    = record['tele_fadmut']
    a3.FADMUTX   = record['tele_fadmutx']
    a3.FADMUSO   = record['tele_fadmuso']
    a3.FADMUSOX  = record['tele_fadmusox']
    a3.FFTDMUT   = record['tele_fftdmut']
    a3.FFTDMUTX  = record['tele_fftdmutx']
    a3.FFTDMUSO  = record['tele_fftdmuso']
    a3.FFTDMUSX  = record['tele_fftdmusx']
    a3.FOTHMUT   = record['tele_fothmut']
    a3.FOTHMUTX  = record['tele_fothmutx']
    a3.FOTHMUSO  = record['tele_fothmuso']
    a3.FOTHMUSX  = record['tele_fothmusx']
    a3.NWINFPAR  = record['tele_nwinfpar']
    a3.MOMMOB    = record['tele_mommob']
    a3.MOMYOB    = record['tele_momyob']
    a3.MOMDAGE   = record['tele_momdage']
    a3.MOMNEUR   = record['tele_momneur']
    a3.MOMPRDX   = record['tele_momprdx']
    a3.MOMMOE    = record['tele_mommoe']
    a3.MOMAGEO   = record['tele_momageo']
    a3.DADMOB    = record['tele_dadmob']
    a3.DADYOB    = record['tele_dadyob']
    a3.DADDAGE   = record['tele_daddage']
    a3.DADNEUR   = record['tele_dadneur']
    a3.DADPRDX   = record['tele_dadprdx']
    a3.DADMOE    = record['tele_dadmoe']
    a3.DADAGEO   = record['tele_dadageo']
    a3.SIBS      = record['tele_sibs']
    a3.NWINFSIB  = record['tele_nwinfsib']
    a3.SIB1MOB   = record['tele_sib1mob']
    a3.SIB1YOB   = record['tele_sib1yob']
    a3.SIB1AGD   = record['tele_sib1agd']
    a3.SIB1NEU   = record['tele_sib1neu']
    a3.SIB1PDX   = record['tele_sib1pdx']
    a3.SIB1MOE   = record['tele_sib1moe']
    a3.SIB1AGO   = record['tele_sib1ago']
    a3.SIB2MOB   = record['tele_sib2mob']
    a3.SIB2YOB   = record['tele_sib2yob']
    a3.SIB2AGD   = record['tele_sib2agd']
    a3.SIB2NEU   = record['tele_sib2neu']
    a3.SIB2PDX   = record['tele_sib2pdx']
    a3.SIB2MOE   = record['tele_sib2moe']
    a3.SIB2AGO   = record['tele_sib2ago']
    a3.SIB3MOB   = record['tele_sib3mob']
    a3.SIB3YOB   = record['tele_sib3yob']
    a3.SIB3AGD   = record['tele_sib3agd']
    a3.SIB3NEU   = record['tele_sib3neu']
    a3.SIB3PDX   = record['tele_sib3pdx']
    a3.SIB3MOE   = record['tele_sib3moe']
    a3.SIB3AGO   = record['tele_sib3ago']
    a3.SIB4MOB   = record['tele_sib4mob']
    a3.SIB4YOB   = record['tele_sib4yob']
    a3.SIB4AGD   = record['tele_sib4agd']
    a3.SIB4NEU   = record['tele_sib4neu']
    a3.SIB4PDX   = record['tele_sib4pdx']
    a3.SIB4MOE   = record['tele_sib4moe']
    a3.SIB4AGO   = record['tele_sib4ago']
    a3.SIB5MOB   = record['tele_sib5mob']
    a3.SIB5YOB   = record['tele_sib5yob']
    a3.SIB5AGD   = record['tele_sib5agd']
    a3.SIB5NEU   = record['tele_sib5neu']
    a3.SIB5PDX   = record['tele_sib5pdx']
    a3.SIB5MOE   = record['tele_sib5moe']
    a3.SIB5AGO   = record['tele_sib5ago']
    a3.SIB6MOB   = record['tele_sib6mob']
    a3.SIB6YOB   = record['tele_sib6yob']
    a3.SIB6AGD   = record['tele_sib6agd']
    a3.SIB6NEU   = record['tele_sib6neu']
    a3.SIB6PDX   = record['tele_sib6pdx']
    a3.SIB6MOE   = record['tele_sib6moe']
    a3.SIB6AGO   = record['tele_sib6ago']
    a3.SIB7MOB   = record['tele_sib7mob']
    a3.SIB7YOB   = record['tele_sib7yob']
    a3.SIB7AGD   = record['tele_sib7agd']
    a3.SIB7NEU   = record['tele_sib7neu']
    a3.SIB7PDX   = record['tele_sib7pdx']
    a3.SIB7MOE   = record['tele_sib7moe']
    a3.SIB7AGO   = record['tele_sib7ago']
    a3.SIB8MOB   = record['tele_sib8mob']
    a3.SIB8YOB   = record['tele_sib8yob']
    a3.SIB8AGD   = record['tele_sib8agd']
    a3.SIB8NEU   = record['tele_sib8neu']
    a3.SIB8PDX   = record['tele_sib8pdx']
    a3.SIB8MOE   = record['tele_sib8moe']
    a3.SIB8AGO   = record['tele_sib8ago']
    a3.SIB9MOB   = record['tele_sib9mob']
    a3.SIB9YOB   = record['tele_sib9yob']
    a3.SIB9AGD   = record['tele_sib9agd']
    a3.SIB9NEU   = record['tele_sib9neu']
    a3.SIB9PDX   = record['tele_sib9pdx']
    a3.SIB9MOE   = record['tele_sib9moe']
    a3.SIB9AGO   = record['tele_sib9ago']
    a3.SIB10MOB  = record['tele_sib10mob']
    a3.SIB10YOB  = record['tele_sib10yob']
    a3.SIB10AGD  = record['tele_sib10agd']
    a3.SIB10NEU  = record['tele_sib10neu']
    a3.SIB10PDX  = record['tele_sib10pdx']
    a3.SIB10MOE  = record['tele_sib10moe']
    a3.SIB10AGO  = record['tele_sib10ago']
    a3.SIB11MOB  = record['tele_sib11mob']
    a3.SIB11YOB  = record['tele_sib11yob']
    a3.SIB11AGD  = record['tele_sib11agd']
    a3.SIB11NEU  = record['tele_sib11neu']
    a3.SIB11PDX  = record['tele_sib11pdx']
    a3.SIB11MOE  = record['tele_sib11moe']
    a3.SIB11AGO  = record['tele_sib11ago']
    a3.SIB12MOB  = record['tele_sib12mob']
    a3.SIB12YOB  = record['tele_sib12yob']
    a3.SIB12AGD  = record['tele_sib12agd']
    a3.SIB12NEU  = record['tele_sib12neu']
    a3.SIB12PDX  = record['tele_sib12pdx']
    a3.SIB12MOE  = record['tele_sib12moe']
    a3.SIB12AGO  = record['tele_sib12ago']
    a3.SIB13MOB  = record['tele_sib13mob']
    a3.SIB13YOB  = record['tele_sib13yob']
    a3.SIB13AGD  = record['tele_sib13agd']
    a3.SIB13NEU  = record['tele_sib13neu']
    a3.SIB13PDX  = record['tele_sib13pdx']
    a3.SIB13MOE  = record['tele_sib13moe']
    a3.SIB13AGO  = record['tele_sib13ago']
    a3.SIB14MOB  = record['tele_sib14mob']
    a3.SIB14YOB  = record['tele_sib14yob']
    a3.SIB14AGD  = record['tele_sib14agd']
    a3.SIB14NEU  = record['tele_sib14neu']
    a3.SIB14PDX  = record['tele_sib14pdx']
    a3.SIB14MOE  = record['tele_sib14moe']
    a3.SIB14AGO  = record['tele_sib14ago']
    a3.SIB15MOB  = record['tele_sib15mob']
    a3.SIB15YOB  = record['tele_sib15yob']
    a3.SIB15AGD  = record['tele_sib15agd']
    a3.SIB15NEU  = record['tele_sib15neu']
    a3.SIB15PDX  = record['tele_sib15pdx']
    a3.SIB15MOE  = record['tele_sib15moe']
    a3.SIB15AGO  = record['tele_sib15ago']
    a3.SIB16MOB  = record['tele_sib16mob']
    a3.SIB16YOB  = record['tele_sib16yob']
    a3.SIB16AGD  = record['tele_sib16agd']
    a3.SIB16NEU  = record['tele_sib16neu']
    a3.SIB16PDX  = record['tele_sib16pdx']
    a3.SIB16MOE  = record['tele_sib16moe']
    a3.SIB16AGO  = record['tele_sib16ago']
    a3.SIB17MOB  = record['tele_sib17mob']
    a3.SIB17YOB  = record['tele_sib17yob']
    a3.SIB17AGD  = record['tele_sib17agd']
    a3.SIB17NEU  = record['tele_sib17neu']
    a3.SIB17PDX  = record['tele_sib17pdx']
    a3.SIB17MOE  = record['tele_sib17moe']
    a3.SIB17AGO  = record['tele_sib17ago']
    a3.SIB18MOB  = record['tele_sib18mob']
    a3.SIB18YOB  = record['tele_sib18yob']
    a3.SIB18AGD  = record['tele_sib18agd']
    a3.SIB18NEU  = record['tele_sib18neu']
    a3.SIB18PDX  = record['tele_sib18pdx']
    a3.SIB18MOE  = record['tele_sib18moe']
    a3.SIB18AGO  = record['tele_sib18ago']
    a3.SIB19MOB  = record['tele_sib19mob']
    a3.SIB19YOB  = record['tele_sib19yob']
    a3.SIB19AGD  = record['tele_sib19agd']
    a3.SIB19NEU  = record['tele_sib19neu']
    a3.SIB19PDX  = record['tele_sib19pdx']
    a3.SIB19MOE  = record['tele_sib19moe']
    a3.SIB19AGO  = record['tele_sib19ago']
    a3.SIB20MOB  = record['tele_sib20mob']
    a3.SIB20YOB  = record['tele_sib20yob']
    a3.SIB20AGD  = record['tele_sib20agd']
    a3.SIB20NEU  = record['tele_sib20neu']
    a3.SIB20PDX  = record['tele_sib20pdx']
    a3.SIB20MOE  = record['tele_sib20moe']
    a3.SIB20AGO  = record['tele_sib20ago']
    a3.KIDS      = record['tele_kids']
    a3.NWINFKID  = record['tele_nwinfkid']
    a3.KID1MOB   = record['tele_kid1mob']
    a3.KID1YOB   = record['tele_kid1yob']
    a3.KID1AGD   = record['tele_kid1agd']
    a3.KID1NEU   = record['tele_kid1neu']
    a3.KID1PDX   = record['tele_kid1pdx']
    a3.KID1MOE   = record['tele_kid1moe']
    a3.KID1AGO   = record['tele_kid1ago']
    a3.KID2MOB   = record['tele_kid2mob']
    a3.KID2YOB   = record['tele_kid2yob']
    a3.KID2AGD   = record['tele_kid2agd']
    a3.KID2NEU   = record['tele_kid2neu']
    a3.KID2PDX   = record['tele_kid2pdx']
    a3.KID2MOE   = record['tele_kid2moe']
    a3.KID2AGO   = record['tele_kid2ago']
    a3.KID3MOB   = record['tele_kid3mob']
    a3.KID3YOB   = record['tele_kid3yob']
    a3.KID3AGD   = record['tele_kid3agd']
    a3.KID3NEU   = record['tele_kid3neu']
    a3.KID3PDX   = record['tele_kid3pdx']
    a3.KID3MOE   = record['tele_kid3moe']
    a3.KID3AGO   = record['tele_kid3ago']
    a3.KID4MOB   = record['tele_kid4mob']
    a3.KID4YOB   = record['tele_kid4yob']
    a3.KID4AGD   = record['tele_kid4agd']
    a3.KID4NEU   = record['tele_kid4neu']
    a3.KID4PDX   = record['tele_kid4pdx']
    a3.KID4MOE   = record['tele_kid4moe']
    a3.KID4AGO   = record['tele_kid4ago']
    a3.KID5MOB   = record['tele_kid5mob']
    a3.KID5YOB   = record['tele_kid5yob']
    a3.KID5AGD   = record['tele_kid5agd']
    a3.KID5NEU   = record['tele_kid5neu']
    a3.KID5PDX   = record['tele_kid5pdx']
    a3.KID5MOE   = record['tele_kid5moe']
    a3.KID5AGO   = record['tele_kid5ago']
    a3.KID6MOB   = record['tele_kid6mob']
    a3.KID6YOB   = record['tele_kid6yob']
    a3.KID6AGD   = record['tele_kid6agd']
    a3.KID6NEU   = record['tele_kid6neu']
    a3.KID6PDX   = record['tele_kid6pdx']
    a3.KID6MOE   = record['tele_kid6moe']
    a3.KID6AGO   = record['tele_kid6ago']
    a3.KID7MOB   = record['tele_kid7mob']
    a3.KID7YOB   = record['tele_kid7yob']
    a3.KID7AGD   = record['tele_kid7agd']
    a3.KID7NEU   = record['tele_kid7neu']
    a3.KID7PDX   = record['tele_kid7pdx']
    a3.KID7MOE   = record['tele_kid7moe']
    a3.KID7AGO   = record['tele_kid7ago']
    a3.KID8MOB   = record['tele_kid8mob']
    a3.KID8YOB   = record['tele_kid8yob']
    a3.KID8AGD   = record['tele_kid8agd']
    a3.KID8NEU   = record['tele_kid8neu']
    a3.KID8PDX   = record['tele_kid8pdx']
    a3.KID8MOE   = record['tele_kid8moe']
    a3.KID8AGO   = record['tele_kid8ago']
    a3.KID9MOB   = record['tele_kid9mob']
    a3.KID9YOB   = record['tele_kid9yob']
    a3.KID9AGD   = record['tele_kid9agd']
    a3.KID9NEU   = record['tele_kid9neu']
    a3.KID9PDX   = record['tele_kid9pdx']
    a3.KID9MOE   = record['tele_kid9moe']
    a3.KID9AGO   = record['tele_kid9ago']
    a3.KID10MOB  = record['tele_kid10mob']
    a3.KID10YOB  = record['tele_kid10yob']
    a3.KID10AGD  = record['tele_kid10agd']
    a3.KID10NEU  = record['tele_kid10neu']
    a3.KID10PDX  = record['tele_kid10pdx']
    a3.KID10MOE  = record['tele_kid10moe']
    a3.KID10AGO  = record['tele_kid10ago']
    a3.KID11MOB  = record['tele_kid11mob']
    a3.KID11YOB  = record['tele_kid11yob']
    a3.KID11AGD  = record['tele_kid11agd']
    a3.KID11NEU  = record['tele_kid11neu']
    a3.KID11PDX  = record['tele_kid11pdx']
    a3.KID11MOE  = record['tele_kid11moe']
    a3.KID11AGO  = record['tele_kid11ago']
    a3.KID12MOB  = record['tele_kid12mob']
    a3.KID12YOB  = record['tele_kid12yob']
    a3.KID12AGD  = record['tele_kid12agd']
    a3.KID12NEU  = record['tele_kid12neu']
    a3.KID12PDX  = record['tele_kid12pdx']
    a3.KID12MOE  = record['tele_kid12moe']
    a3.KID12AGO  = record['tele_kid12ago']
    a3.KID13MOB  = record['tele_kid13mob']
    a3.KID13YOB  = record['tele_kid13yob']
    a3.KID13AGD  = record['tele_kid13agd']
    a3.KID13NEU  = record['tele_kid13neu']
    a3.KID13PDX  = record['tele_kid13pdx']
    a3.KID13MOE  = record['tele_kid13moe']
    a3.KID13AGO  = record['tele_kid13ago']
    a3.KID14MOB  = record['tele_kid14mob']
    a3.KID14YOB  = record['tele_kid14yob']
    a3.KID14AGD  = record['tele_kid14agd']
    a3.KID14NEU  = record['tele_kid14neu']
    a3.KID14PDX  = record['tele_kid14pdx']
    a3.KID14MOE  = record['tele_kid14moe']
    a3.KID14AGO  = record['tele_kid14ago']
    a3.KID15MOB  = record['tele_kid15mob']
    a3.KID15YOB  = record['tele_kid15yob']
    a3.KID15AGD  = record['tele_kid15agd']
    a3.KID15NEU  = record['tele_kid15neu']
    a3.KID15PDX  = record['tele_kid15pdx']
    a3.KID15MOE  = record['tele_kid15moe']
    a3.KID15AGO  = record['tele_kid15ago']
    packet.append(a3)


def add_a4(record, packet):
    # Form A4D and A4G are special in that our REDCap implementation (FVP A4)
    # combines them by asking if the subject is taking any medications (which
    # corresponds to A4G.ANYMEDS), then has 50 fields to specify each
    # medication used, which we turn each one into a FormA4D object.
    a4g = tfp_new_forms.FormA4G()
    a4g.ANYMEDS = record['tele_anymeds']
    packet.append(a4g)

    for i in range(1, 51):
            key = 'tele_drugid_' + str(i)
            if record[key]:
                a4d = tfp_new_forms.FormA4D()
                a4d.DRUGID = record[key]
                packet.append(a4d)


def add_b4(record, packet):
    b4 = tfp_new_forms.FormB4()
    b4.MEMORY    = record['tele_memory']
    b4.ORIENT    = record['tele_orient']
    b4.JUDGMENT  = record['tele_judgment']
    b4.COMMUN    = record['tele_commun']
    b4.HOMEHOBB  = record['tele_homehobb']
    b4.PERSCARE  = record['tele_perscare']
    b4.CDRSUM    = record['tele_cdrsum']
    b4.CDRGLOB   = record['tele_cdrglob']
    b4.COMPORT   = record['tele_comport']
    b4.CDRLANG   = record['tele_cdrlang']
    packet.append(b4)


def add_b5(record, packet):
    b5 = tfp_new_forms.FormB5()
    b5.NPIQINF   = record['tele_npiqinf']
    b5.NPIQINFX  = record['tele_npiqinfx']
    b5.DEL       = record['tele_del']
    b5.DELSEV    = record['tele_delsev']
    b5.HALL      = record['tele_hall']
    b5.HALLSEV   = record['tele_hallsev']
    b5.AGIT      = record['tele_agit']
    b5.AGITSEV   = record['tele_agitsev']
    b5.DEPD      = record['tele_depd']
    b5.DEPDSEV   = record['tele_depdsev']
    b5.ANX       = record['tele_anx']
    b5.ANXSEV    = record['tele_anxsev']
    b5.ELAT      = record['tele_elat']
    b5.ELATSEV   = record['tele_elatsev']
    b5.APA       = record['tele_apa']
    b5.APASEV    = record['tele_apasev']
    b5.DISN      = record['tele_disn']
    b5.DISNSEV   = record['tele_disnsev']
    b5.IRR       = record['tele_irr']
    b5.IRRSEV    = record['tele_irrsev']
    b5.MOT       = record['tele_mot']
    b5.MOTSEV    = record['tele_motsev']
    b5.NITE      = record['tele_nite']
    b5.NITESEV   = record['tele_nitesev']
    b5.APP       = record['tele_app']
    b5.APPSEV    = record['tele_appsev']
    packet.append(b5)


def add_b6(record, packet):
    b6 = tfp_new_forms.FormB6()
    b6.NOGDS     = record['tele_nogds']
    b6.SATIS     = record['tele_satis']
    b6.DROPACT   = record['tele_dropact']
    b6.EMPTY     = record['tele_empty']
    b6.BORED     = record['tele_bored']
    b6.SPIRITS   = record['tele_spirits']
    b6.AFRAID    = record['tele_afraid']
    b6.HAPPY     = record['tele_happy']
    b6.HELPLESS  = record['tele_helpless']
    b6.STAYHOME  = record['tele_stayhome']
    b6.MEMPROB   = record['tele_memprob']
    b6.WONDRFUL  = record['tele_wondrful']
    b6.WRTHLESS  = record['tele_wrthless']
    b6.ENERGY    = record['tele_energy']
    b6.HOPELESS  = record['tele_hopeless']
    b6.BETTER    = record['tele_better']
    b6.GDS       = record['tele_gds']
    packet.append(b6)


def add_b7(record, packet):
    b7 = tfp_new_forms.FormB7()
    b7.BILLS     = record['tele_bills']
    b7.TAXES     = record['tele_taxes']
    b7.SHOPPING  = record['tele_shopping']
    b7.GAMES     = record['tele_games']
    b7.STOVE     = record['tele_stove']
    b7.MEALPREP  = record['tele_mealprep']
    b7.EVENTS    = record['tele_events']
    b7.PAYATTN   = record['tele_payattn']
    b7.REMDATES  = record['tele_remdates']
    b7.TRAVEL    = record['tele_travel']
    packet.append(b7)


def add_b9(record, packet):
    b9 = tfp_new_forms.FormB9()
    b9.DECSUB    = record['tele_decsub']
    b9.DECIN     = record['tele_decin']
    b9.DECCLCOG  = record['tele_decclcog']
    b9.COGMEM    = record['tele_cogmem']
    b9.COGORI    = record['tele_cogori']
    b9.COGJUDG   = record['tele_cogjudg']
    b9.COGLANG   = record['tele_coglang']
    b9.COGVIS    = record['tele_cogvis']
    b9.COGATTN   = record['tele_cogattn']
    b9.COGFLUC   = record['tele_cogfluc']
    b9.COGFLAGO  = record['tele_cogflago']
    b9.COGOTHR   = record['tele_cogothr']
    b9.COGOTHRX  = record['tele_cogothrx']
    b9.COGFPRED  = record['tele_cogfpred']
    b9.COGFPREX  = record['tele_cogfprex']
    b9.COGMODE   = record['tele_cogmode']
    b9.COGMODEX  = record['tele_cogmodex']
    b9.DECAGE    = record['tele_decage']
    b9.DECCLBE   = record['tele_decclbe']
    b9.BEAPATHY  = record['tele_beapathy']
    b9.BEDEP     = record['tele_bedep']
    b9.BEVHALL   = record['tele_bevhall']
    b9.BEVWELL   = record['tele_bevwell']
    b9.BEVHAGO   = record['tele_bevhago']
    b9.BEAHALL   = record['tele_beahall']
    b9.BEDEL     = record['tele_bedel']
    b9.BEDISIN   = record['tele_bedisin']
    b9.BEIRRIT   = record['tele_beirrit']
    b9.BEAGIT    = record['tele_beagit']
    b9.BEPERCH   = record['tele_beperch']
    b9.BEREM     = record['tele_berem']
    b9.BEREMAGO  = record['tele_beremago']
    b9.BEANX     = record['tele_beanx']
    b9.BEOTHR    = record['tele_beothr']
    b9.BEOTHRX   = record['tele_beothrx']
    b9.BEFPRED   = record['tele_befpred']
    b9.BEFPREDX  = record['tele_befpredx']
    b9.BEMODE    = record['tele_bemode']
    b9.BEMODEX   = record['tele_bemodex']
    b9.BEAGE     = record['tele_beage']
    b9.DECCLMOT  = record['tele_decclmot']
    b9.MOGAIT    = record['tele_mogait']
    b9.MOFALLS   = record['tele_mofalls']
    b9.MOTREM    = record['tele_motrem']
    b9.MOSLOW    = record['tele_moslow']
    b9.MOFRST    = record['tele_mofrst']
    b9.MOMODE    = record['tele_momode']
    b9.MOMODEX   = record['tele_momodex']
    b9.MOMOPARK  = record['tele_momopark']
    b9.PARKAGE   = record['tele_parkage']
    b9.MOMOALS   = record['tele_momoals']
    b9.ALSAGE    = record['tele_alsage']
    b9.MOAGE     = record['tele_moage']
    b9.COURSE    = record['tele_course']
    b9.FRSTCHG   = record['tele_frstchg']
    b9.LBDEVAL   = record['tele_lbdeval']
    b9.FTLDEVAL  = record['tele_ftldeval']
    packet.append(b9)


def add_c2t(record, packet):
    c2 = tfp_new_forms.FormC2()
    c2.MODCOMM  = record['tele_modcomm']
    c2.MOCACOMP = record['tele_mocacomp']
    c2.MOCAREAS = record['tele_mocareas']
    c2.MOCALAN  = record['tele_mocalan']
    c2.MOCALANX = record['tele_mocalanx']
    c2.MOCAHEAR = record['tele_mocahear']
    c2.MOCBTOTS = record['tele_mocbtots']
    c2.MOCADIGI = record['tele_mocadigi']
    c2.MOCALETT = record['tele_mocalett']
    c2.MOCASER7 = record['tele_mocaser7']
    c2.MOCAREPE = record['tele_mocarepe']
    c2.MOCAFLUE = record['tele_mocaflue']
    c2.MOCAABST = record['tele_mocaabst']
    c2.MOCARECN = record['tele_mocarecn']
    c2.MOCARECC = record['tele_mocarecc']
    c2.MOCARECR = record['tele_mocarecr']
    c2.MOCAORDT = record['tele_mocaordt']
    c2.MOCAORMO = record['tele_mocaormo']
    c2.MOCAORYR = record['tele_mocaoryr']
    c2.MOCAORDY = record['tele_mocaordy']
    c2.MOCAORPL = record['tele_mocaorpl']
    c2.MOCAORCT = record['tele_mocaorct']
    c2.NPSYLAN  = record['tele_npsylan']
    c2.NPSYLANX = record['tele_npsylanx']
    c2.CRAFTVRS = record['tele_craftvrs']
    c2.CRAFTURS = record['tele_crafturs']
    c2.REY1REC  = record['tele_rey1rec']
    c2.REY1INT  = record['tele_rey1int']
    c2.REY2REC  = record['tele_rey2rec']
    c2.REY2INT  = record['tele_rey2int']
    c2.REY3REC  = record['tele_rey3rec']
    c2.REY3INT  = record['tele_rey3int']
    c2.REY4REC  = record['tele_rey4rec']
    c2.REY4INT  = record['tele_rey4int']
    c2.REY5REC  = record['tele_rey5rec']
    c2.REY5INT  = record['tele_rey5int']
    c2.REY6REC  = record['tele_rey6rec']
    c2.REY6INT  = record['tele_rey6int']
    c2.DIGFORCT = record['tele_digforct']
    c2.DIGFORSL = record['tele_digforsl']
    c2.DIGBACCT = record['tele_digbacct']
    c2.DIGBACLS = record['tele_digbacls']
    c2.OTRAILA  = record['tele_otraila']
    c2.OTRLARR  = record['tele_otrlarr']
    c2.OTRLALI  = record['tele_otrlali']
    c2.OTRAILB  = record['tele_otrailb']
    c2.OTRLBRR  = record['tele_otrlbrr']
    c2.OTRLBLI  = record['tele_otrlbli']
    c2.CRAFTDVR = record['tele_craftdvr']
    c2.CRAFTDRE = record['tele_craftdre']
    c2.CRAFTDTI = record['tele_craftdti']
    c2.CRAFTCUE = record['tele_craftcue']
    c2.ANIMALS  = record['tele_animals']
    c2.VEG      = record['tele_veg']
    c2.UDSVERFC = record['tele_udsverfc']
    c2.UDSVERFN = record['tele_udsverfn']
    c2.UDSVERNF = record['tele_udsvernf']
    c2.UDSVERLC = record['tele_udsverlc']
    c2.UDSVERLR = record['tele_udsverlr']
    c2.UDSVERLN = record['tele_udsverln']
    c2.UDSVERTN = record['tele_udsvertn']
    c2.UDSVERTE = record['tele_udsverte']
    c2.UDSVERTI = record['tele_udsverti']
    c2.REYDREC  = record['tele_reydrec']
    c2.REYDINT  = record['tele_reydint']
    c2.REYTCOR  = record['tele_reytcor']
    c2.REYFPOS  = record['tele_reyfpos']
    c2.VNTTOTW  = record['tele_vnttotw']
    c2.VNTPCNC  = record['tele_vntpcnc']
    c2.COGSTAT  = record['tele_cogstat']
    c2.RESPVAL  = record['tele_respval']
    c2.RESPHEAR = record['tele_resphear']
    c2.RESPDIST = record['tele_respdist']
    c2.RESPINTR = record['tele_respintr']
    c2.RESPDISN = record['tele_respdisn']
    c2.RESPFATG = record['tele_respfatg']
    c2.RESPEMOT = record['tele_respemot']
    c2.RESPASST = record['tele_respasst']
    c2.RESPOTH  = record['tele_respoth']
    c2.RESPOTHX = record['tele_respothx']
    packet.append(c2)


def add_d1(record, packet):
    d1 = tfp_new_forms.FormD1()
    d1.DXMETHOD  = record['tele_dxmethod']
    d1.NORMCOG   = record['tele_normcog']
    d1.DEMENTED  = record['tele_demented']
    d1.AMNDEM    = record['tele_amndem']
    d1.PCA       = record['tele_pca']
    d1.PPASYN    = record['tele_ppasyn']
    d1.PPASYNT   = record['tele_ppasynt']
    d1.FTDSYN    = record['tele_ftdsyn']
    d1.LBDSYN    = record['tele_lbdsyn']
    d1.NAMNDEM   = record['tele_namndem']
    d1.MCIAMEM   = record['tele_mciamem']
    d1.MCIAPLUS  = record['tele_mciaplus']
    d1.MCIAPLAN  = record['tele_mciaplan']
    d1.MCIAPATT  = record['tele_mciapatt']
    d1.MCIAPEX   = record['tele_mciapex']
    d1.MCIAPVIS  = record['tele_mciapvis']
    d1.MCINON1   = record['tele_mcinon1']
    d1.MCIN1LAN  = record['tele_mcin1lan']
    d1.MCIN1ATT  = record['tele_mcin1att']
    d1.MCIN1EX   = record['tele_mcin1ex']
    d1.MCIN1VIS  = record['tele_mcin1vis']
    d1.MCINON2   = record['tele_mcinon2']
    d1.MCIN2LAN  = record['tele_mcin2lan']
    d1.MCIN2ATT  = record['tele_mcin2att']
    d1.MCIN2EX   = record['tele_mcin2ex']
    d1.MCIN2VIS  = record['tele_mcin2vis']
    d1.IMPNOMCI  = record['tele_impnomci']
    d1.AMYLPET   = record['tele_amylpet']
    d1.AMYLCSF   = record['tele_amylcsf']
    d1.FDGAD     = record['tele_fdgad']
    d1.HIPPATR   = record['tele_hippatr']
    d1.TAUPETAD  = record['tele_taupetad']
    d1.CSFTAU    = record['tele_csftau']
    d1.FDGFTLD   = record['tele_fdgftld']
    d1.TPETFTLD  = record['tele_tpetftld']
    d1.MRFTLD    = record['tele_mrftld']
    d1.DATSCAN   = record['tele_datscan']
    d1.OTHBIOM   = record['tele_othbiom']
    d1.OTHBIOMX  = record['tele_othbiomx']
    d1.IMAGLINF  = record['tele_imaglinf']
    d1.IMAGLAC   = record['tele_imaglac']
    d1.IMAGMACH  = record['tele_imagmach']
    d1.IMAGMICH  = record['tele_imagmich']
    d1.IMAGMWMH  = record['tele_imagmwmh']
    d1.IMAGEWMH  = record['tele_imagewmh']
    d1.ADMUT     = record['tele_admut']
    d1.FTLDMUT   = record['tele_ftldmut']
    d1.OTHMUT    = record['tele_othmut']
    d1.OTHMUTX   = record['tele_othmutx']
    d1.ALZDIS    = record['tele_alzdis']
    d1.ALZDISIF  = record['tele_alzdisif']
    d1.LBDIS     = record['tele_lbdis']
    d1.LBDIF     = record['tele_lbdif']
    d1.PARK      = record['tele_park']
    d1.MSA       = record['tele_msa']
    d1.MSAIF     = record['tele_msaif']
    d1.PSP       = record['tele_psp']
    d1.PSPIF     = record['tele_pspif']
    d1.CORT      = record['tele_cort']
    d1.CORTIF    = record['tele_cortif']
    d1.FTLDMO    = record['tele_ftldmo']
    d1.FTLDMOIF  = record['tele_ftldmoif']
    d1.FTLDNOS   = record['tele_ftldnos']
    d1.FTLDNOIF  = record['tele_ftldnoif']
    d1.FTLDSUBT  = record['tele_ftldsubt']
    d1.FTLDSUBX  = record['tele_ftldsubx']
    d1.CVD       = record['tele_cvd']
    d1.CVDIF     = record['tele_cvdif']
    d1.PREVSTK   = record['tele_prevstk']
    d1.STROKDEC  = record['tele_strokdec']
    d1.STKIMAG   = record['tele_stkimag']
    d1.INFNETW   = record['tele_infnetw']
    d1.INFWMH    = record['tele_infwmh']
    d1.ESSTREM   = record['tele_esstrem']
    d1.ESSTREIF  = record['tele_esstreif']
    d1.DOWNS     = record['tele_downs']
    d1.DOWNSIF   = record['tele_downsif']
    d1.HUNT      = record['tele_hunt']
    d1.HUNTIF    = record['tele_huntif']
    d1.PRION     = record['tele_prion']
    d1.PRIONIF   = record['tele_prionif']
    d1.BRNINJ    = record['tele_brninj']
    d1.BRNINJIF  = record['tele_brninjif']
    d1.BRNINCTE  = record['tele_brnincte']
    d1.HYCEPH    = record['tele_hyceph']
    d1.HYCEPHIF  = record['tele_hycephif']
    d1.EPILEP    = record['tele_epilep']
    d1.EPILEPIF  = record['tele_epilepif']
    d1.NEOP      = record['tele_neop']
    d1.NEOPIF    = record['tele_neopif']
    d1.NEOPSTAT  = record['tele_neopstat']
    d1.HIV       = record['tele_hiv']
    d1.HIVIF     = record['tele_hivif']
    d1.OTHCOG    = record['tele_othcog']
    d1.OTHCOGIF  = record['tele_othcogif']
    d1.OTHCOGX   = record['tele_othcogx']
    d1.DEP       = record['tele_dep']
    d1.DEPIF     = record['tele_depif']
    d1.DEPTREAT  = record['tele_deptreat']
    d1.BIPOLDX   = record['tele_bipoldx']
    d1.BIPOLDIF  = record['tele_bipoldif']
    d1.SCHIZOP   = record['tele_schizop']
    d1.SCHIZOIF  = record['tele_schizoif']
    d1.ANXIET    = record['tele_anxiet']
    d1.ANXIETIF  = record['tele_anxietif']
    d1.DELIR     = record['tele_delir']
    d1.DELIRIF   = record['tele_delirif']
    d1.PTSDDX    = record['tele_ptsddx']
    d1.PTSDDXIF  = record['tele_ptsddxif']
    d1.OTHPSY    = record['tele_othpsy']
    d1.OTHPSYIF  = record['tele_othpsyif']
    d1.OTHPSYX   = record['tele_othpsyx']
    d1.ALCDEM    = record['tele_alcdem']
    d1.ALCDEMIF  = record['tele_alcdemif']
    d1.ALCABUSE  = record['tele_alcabuse']
    d1.IMPSUB    = record['tele_impsub']
    d1.IMPSUBIF  = record['tele_impsubif']
    d1.DYSILL    = record['tele_dysill']
    d1.DYSILLIF  = record['tele_dysillif']
    d1.MEDS      = record['tele_meds']
    d1.MEDSIF    = record['tele_medsif']
    d1.COGOTH    = record['tele_cogoth']
    d1.COGOTHIF  = record['tele_cogothif']
    d1.COGOTHX   = record['tele_cogothx']
    d1.COGOTH2   = record['tele_cogoth2']
    d1.COGOTH2F  = record['tele_cogoth2f']
    d1.COGOTH2X  = record['tele_cogoth2x']
    d1.COGOTH3   = record['tele_cogoth3']
    d1.COGOTH3F  = record['tele_cogoth3f']
    d1.COGOTH3X  = record['tele_cogoth3x']
    packet.append(d1)


def add_d2(record, packet):
    d2 = tfp_new_forms.FormD2()
    d2.CANCER    = record['tele_cancer']
    d2.CANCSITE  = record['tele_cancsite']
    d2.DIABET    = record['tele_diabet']
    d2.MYOINF    = record['tele_myoinf']
    d2.CONGHRT   = record['tele_conghrt']
    d2.AFIBRILL  = record['tele_afibrill']
    d2.HYPERT    = record['tele_hypert']
    d2.ANGINA    = record['tele_angina']
    d2.HYPCHOL   = record['tele_hypchol']
    d2.VB12DEF   = record['tele_vb12def']
    d2.THYDIS    = record['tele_thydis']
    d2.ARTH      = record['tele_arth']
    d2.ARTYPE    = record['tele_artype']
    d2.ARTYPEX   = record['tele_artypex']
    d2.ARTUPEX   = record['tele_artupex']
    d2.ARTLOEX   = record['tele_artloex']
    d2.ARTSPIN   = record['tele_artspin']
    d2.ARTUNKN   = record['tele_artunkn']
    d2.URINEINC  = record['tele_urineinc']
    d2.BOWLINC   = record['tele_bowlinc']
    d2.SLEEPAP   = record['tele_sleepap']
    d2.REMDIS    = record['tele_remdis']
    d2.HYPOSOM   = record['tele_hyposom']
    d2.SLEEPOTH  = record['tele_sleepoth']
    d2.SLEEPOTX  = record['tele_sleepotx']
    d2.ANGIOCP   = record['tele_angiocp']
    d2.ANGIOPCI  = record['tele_angiopci']
    d2.PACEMAKE  = record['tele_pacemake']
    d2.HVALVE    = record['tele_hvalve']
    d2.ANTIENC   = record['tele_antienc']
    d2.ANTIENCX  = record['tele_antiencx']
    d2.OTHCOND   = record['tele_othcond']
    d2.OTHCONDX  = record['tele_othcondx']
    packet.append(d2)


def update_header(record, packet):
    for header in packet:
        header.PACKET = "T"
        header.FORMID = header.form_name

        # Custom header info
        formdate = ''
        formrater = ''
        try:
            if header.FORMID.value == "T1":
                formdate = record['tfp_t1_date']
                formrater = record['tfp_t1_rater']
            elif header.FORMID.value == "A1":
                formdate = record['tfp_a1_date']
                formrater = record['tfp_a1_rater']
            elif header.FORMID.value == "A2":
                formdate = record['tfp_a2_date']
                formrater = record['tfp_a2_rater']
            elif header.FORMID.value == "A3":
                formdate = record['tfp_a3_date']
                formrater = record['tfp_a3_rater']
            elif header.FORMID.value == "A4D":
                formdate = record['tfp_a4d_date']
                formrater = record['tfp_a4d_rater']
            elif header.FORMID.value == "A4G":
                formdate = record['tfp_a4g_date']
                formrater = record['tfp_a4g_rater']
            elif header.FORMID.value == "B4":
                formdate = record['tfp_b4_date']
                formrater = record['tfp_b4_rater']
            elif header.FORMID.value == "B5":
                formdate = record['tfp_b5_date']
                formrater = record['tfp_b5_rater']
            elif header.FORMID.value == "B7":
                formdate = record['tfp_b7_date']
                formrater = record['tfp_b7_rater']
            elif header.FORMID.value == "B9":
                formdate = record['tfp_b9_date']
                formrater = record['tfp_b9_rater']
            elif header.FORMID.value == "C2":
                formdate = record['tfp_c2_date']
                formrater = record['tfp_c2_rater']
            elif header.FORMID.value == "D1":
                formdate = record['tfp_d1_date']
                formrater = record['tfp_d1_rater']
            elif header.FORMID.value == "D2":
                formdate = record['tfp_d2_date']
                formrater = record['tfp_d2_rater']
            elif header.FORMID.value == "Z1X":
                formdate = record['tfp_z1x_date']
                formrater = record['tfp_z1x_rater']
            # Date should be format of yyyy-mm-dd. If not,
            # then use form header defaults.
            if len(formdate.split("-")) == 3:
                yyyy = formdate.split("-")[0]
                mm = formdate.split("-")[1]
                dd = formdate.split("-")[2]
            else:
                yyyy = record['visityr']
                mm = record['visitmo']
                dd = record['visitday']
            header.VISITMO = mm
            header.VISITDAY = dd
            header.VISITYR = yyyy
        except KeyError:
            header.VISITMO = record['visitmo']
            header.VISITDAY = record['visitday']
            header.VISITYR = record['visityr']

        header.FORMVER = "3.2"
        header.ADCID = record['adcid']
        header.PTID = record['ptid']
        header.VISITNUM = record['visitnum']
        if formrater is not None:
            header.INITIALS = formrater
        else:
            header.INITIALS = record['initials']