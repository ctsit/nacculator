###############################################################################
# Copyright 2015-2016 University of Florida. All rights reserved.
# This file is part of UF CTS-IT's NACCulator project.
# Use of this source code is governed by the license found in the LICENSE file.
###############################################################################

from nacc.uds3 import clsform
from nacc.uds3 import packet as ivp_packet
from nacc.uds3.ivp import forms as ivp_forms


def build_uds3_ivp_form(record):
    """ Converts REDCap CSV data into a packet (list of IVP Form objects) """
    packet = ivp_packet.Packet()

    # Set up the forms
    add_z1_or_z1x(record, packet)
    add_a1(record, packet)
    if record['a2_sub'] == '1' or record['a2sub'] == '1':
        add_a2(record, packet)
    if record['a3_sub'] == '1' or record['a3sub'] == '1':
        add_a3(record, packet)
    if record['a4_sub'] == '1' or record['a4sub'] == '1':
        add_a4(record, packet)
    add_a5(record, packet)
    if record['b1_sub'] == '1' or record['b1sub'] == '1':
        add_b1(record, packet)
    add_b4(record, packet)
    if record['b5_sub'] == '1' or record['b5sub'] == '1':
        add_b5(record, packet)
    if record['b6_sub'] == '1' or record['b6sub'] == '1':
        add_b6(record, packet)
    if record['b7_sub'] == '1' or record['b7sub'] == '1':
        add_b7(record, packet)
    add_b8(record, packet)
    add_b9(record, packet)
    add_c1s_or_c2(record, packet)
    add_d1(record, packet)
    add_d2(record, packet)
    clsform.add_cls(record, packet, ivp_forms)
    update_header(record, packet)

    return packet


def add_z1_or_z1x(record, packet):
    # Forms A1, A5, B4, B8, B9, C2, D1, and D2 are all REQUIRED.
    # Fields a1sub, a5sub1, b4sub1, b8sub1, b9sub1, c2sub1, d1sub1, and d2sub1
    # are just section separators.
    z1x = ivp_forms.FormZ1X()
    z1x_filled_fields = 0
    z1x_field_mapping = {
        'LANGA1': 'langa1',
        'LANGA2': 'langa2',
        'A2SUB': 'a2sub',
        'A2NOT': 'a2not',
        'LANGA3': 'langa3',
        'A3SUB': 'a3sub',
        'LANGA4': 'langa4',
        'A4SUB': 'a4sub',
        'A4NOT': 'a4not',
        'LANGA5': 'langa5',
        'LANGB1': 'langb1',
        'B1SUB': 'b1sub',
        'B1NOT': 'b1not',
        'LANGB4': 'langb4',
        'LANGB5': 'langb5',
        'B5SUB': 'b5sub',
        'B5NOT': 'b5not',
        'LANGB6': 'langb6',
        'B6SUB': 'b6sub',
        'B6NOT': 'b6not',
        'LANGB7': 'langb7',
        'B7SUB': 'b7sub',
        'B7NOT': 'b7not',
        'LANGB8': 'langb8',
        'LANGB9': 'langb9',
        'LANGC2': 'langc2',
        'LANGD1': 'langd1',
        'LANGD2': 'langd2',
        'LANGA3A': 'langa3a',
        'FTDA3AFS': 'ftda3afs',
        'FTDA3AFR': 'ftda3afr',
        'LANGB3F': 'langb3f',
        'LANGB9F': 'langb9f',
        'LANGC1F': 'langc1f',
        'LANGC2F': 'langc2f',
        'LANGC3F': 'langc3f',
        'LANGC4F': 'langc4f',
        'FTDC4FS': 'ftdc4fs',
        'FTDC4FR': 'ftdc4fr',
        'FTDC5FS': 'ftdc5fs',
        'FTDC5FR': 'ftdc5fr',
        'FTDC6FS': 'ftdc6fs',
        'FTDC6FR': 'ftdc6fr',
        'LANGE2F': 'lange2f',
        'LANGE3F': 'lange3f',
        'LANGCLS': 'langcls',
        'CLSSUB': 'clssub'
    }
    for key, value in z1x_field_mapping.items():
        try:
            if record[value].strip():
                setattr(z1x, key, record[value])
                z1x_filled_fields += 1
        except KeyError:
            pass

    z1 = ivp_forms.FormZ1()
    z1_filled_fields = 0
    z1_field_mapping = {
        'A2SUB': 'a2_sub',
        'A2NOT': 'a2_not',
        'A2COMM': 'a2_comm',
        'A3SUB': 'a3_sub',
        'A3NOT': 'a3_not',
        'A3COMM': 'a3_comm',
        'A4SUB': 'a4_sub',
        'A4NOT': 'a4_not',
        'A4COMM': 'a4_comm',
        'B1SUB': 'b1_sub',
        'B1NOT': 'b1_not',
        'B1COMM': 'b1_comm',
        'B5SUB': 'b5_sub',
        'B5NOT': 'b5_not',
        'B5COMM': 'b5_comm',
        'B6SUB': 'b6_sub',
        'B6NOT': 'b6_not',
        'B6COMM': 'b6_comm',
        'B7SUB': 'b7_sub',
        'B7NOT': 'b7_not',
        'B7COMM': 'b7_comm'
    }
    for key, value in z1_field_mapping.items():
        try:
            if record[value].strip():
                setattr(z1, key, record[value])
                z1_filled_fields += 1
        except KeyError:
            pass

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
    a1 = ivp_forms.FormA1()
    a1.REASON = record['reason']
    a1.REFERSC = record['refersc']
    a1.LEARNED = record['learned']
    a1.PRESTAT = record['prestat']
    a1.PRESPART = record['prespart']
    a1.SOURCENW = record['source']
    a1.BIRTHMO = record['birthmo']
    a1.BIRTHYR = record['birthyr']
    a1.SEX = record['sex']
    a1.HISPANIC = record['hispanic']
    a1.HISPOR = record['hispor']
    a1.HISPORX = record['hisporx']
    a1.RACE = record['race']
    a1.RACEX = record['racex']
    a1.RACESEC = record['racesec']
    a1.RACESECX = record['racesecx']
    a1.RACETER = record['raceter']
    a1.RACETERX = record['raceterx']
    a1.PRIMLANG = record['primlang']
    a1.PRIMLANX = record['primlanx']
    a1.EDUC = record['educ']
    a1.MARISTAT = record['maristat']
    a1.LIVSITUA = record['livsitua']
    a1.INDEPEND = record['independ']
    a1.RESIDENC = record['residenc']
    a1.ZIP = record['zip']
    a1.HANDED = record['handed']
    packet.append(a1)


def add_a2(record, packet):
    a2 = ivp_forms.FormA2()
    a2.INBIRMO = record['inbirmo']
    a2.INBIRYR = record['inbiryr']
    a2.INSEX = record['insex']
    a2.INHISP = record['inhisp']
    a2.INHISPOR = record['inhispor']
    a2.INHISPOX = record['inhispox']
    a2.INRACE = record['inrace']
    a2.INRACEX = record['inracex']
    a2.INRASEC = record['inrasec']
    a2.INRASECX = record['inrasecx']
    a2.INRATER = record['inrater']
    a2.INRATERX = record['inraterx']
    a2.INEDUC = record['ineduc']
    a2.INRELTO = record['inrelto']
    a2.INKNOWN = record['inknown']
    a2.INLIVWTH = record['inlivwth']
    a2.INVISITS = record['invisits']
    a2.INCALLS = record['incalls']
    a2.INRELY = record['inrely']
    packet.append(a2)


def add_a3(record, packet):
    a3 = ivp_forms.FormA3()
    a3.AFFFAMM = record['afffamm']
    a3.FADMUT = record['fadmut']
    a3.FADMUTX = record['fadmutx']
    a3.FADMUSO = record['fadmuso']
    a3.FADMUSOX = record['fadmusox']
    a3.FFTDMUT = record['fftdmut']
    a3.FFTDMUTX = record['fftdmutx']
    a3.FFTDMUSO = record['fftdmuso']
    a3.FFTDMUSX = record['fftdmusx']
    a3.FOTHMUT = record['fothmut']
    a3.FOTHMUTX = record['fothmutx']
    a3.FOTHMUSO = record['fothmuso']
    a3.FOTHMUSX = record['fothmusx']
    a3.MOMMOB = record['mommob']
    a3.MOMYOB = record['momyob']
    a3.MOMDAGE = record['momdage']
    a3.MOMNEUR = record['momneur']
    a3.MOMPRDX = record['momprdx']
    a3.MOMMOE = record['mommoe']
    a3.MOMAGEO = record['momageo']
    a3.DADMOB = record['dadmob']
    a3.DADYOB = record['dadyob']
    a3.DADDAGE = record['daddage']
    a3.DADNEUR = record['dadneur']
    a3.DADPRDX = record['dadprdx']
    a3.DADMOE = record['dadmoe']
    a3.DADAGEO = record['dadageo']
    a3.SIBS = record['sibs']
    a3.SIB1MOB = record['sib1mob']
    a3.SIB1YOB = record['sib1yob']
    a3.SIB1AGD = record['sib1agd']
    a3.SIB1NEU = record['sib1neu']
    a3.SIB1PDX = record['sib1pdx']
    a3.SIB1MOE = record['sib1moe']
    a3.SIB1AGO = record['sib1ago']
    a3.SIB2MOB = record['sib2mob']
    a3.SIB2YOB = record['sib2yob']
    a3.SIB2AGD = record['sib2agd']
    a3.SIB2NEU = record['sib2neu']
    a3.SIB2PDX = record['sib2pdx']
    a3.SIB2MOE = record['sib2moe']
    a3.SIB2AGO = record['sib2ago']
    a3.SIB3MOB = record['sib3mob']
    a3.SIB3YOB = record['sib3yob']
    a3.SIB3AGD = record['sib3agd']
    a3.SIB3NEU = record['sib3neu']
    a3.SIB3PDX = record['sib3pdx']
    a3.SIB3MOE = record['sib3moe']
    a3.SIB3AGO = record['sib3ago']
    a3.SIB4MOB = record['sib4mob']
    a3.SIB4YOB = record['sib4yob']
    a3.SIB4AGD = record['sib4agd']
    a3.SIB4NEU = record['sib4neu']
    a3.SIB4PDX = record['sib4pdx']
    a3.SIB4MOE = record['sib4moe']
    a3.SIB4AGO = record['sib4ago']
    a3.SIB5MOB = record['sib5mob']
    a3.SIB5YOB = record['sib5yob']
    a3.SIB5AGD = record['sib5agd']
    a3.SIB5NEU = record['sib5neu']
    a3.SIB5PDX = record['sib5pdx']
    a3.SIB5MOE = record['sib5moe']
    a3.SIB5AGO = record['sib5ago']
    a3.SIB6MOB = record['sib6mob']
    a3.SIB6YOB = record['sib6yob']
    a3.SIB6AGD = record['sib6agd']
    a3.SIB6NEU = record['sib6neu']
    a3.SIB6PDX = record['sib6pdx']
    a3.SIB6MOE = record['sib6moe']
    a3.SIB6AGO = record['sib6ago']
    a3.SIB7MOB = record['sib7mob']
    a3.SIB7YOB = record['sib7yob']
    a3.SIB7AGD = record['sib7agd']
    a3.SIB7NEU = record['sib7neu']
    a3.SIB7PDX = record['sib7pdx']
    a3.SIB7MOE = record['sib7moe']
    a3.SIB7AGO = record['sib7ago']
    a3.SIB8MOB = record['sib8mob']
    a3.SIB8YOB = record['sib8yob']
    a3.SIB8AGD = record['sib8agd']
    a3.SIB8NEU = record['sib8neu']
    a3.SIB8PDX = record['sib8pdx']
    a3.SIB8MOE = record['sib8moe']
    a3.SIB8AGO = record['sib8ago']
    a3.SIB9MOB = record['sib9mob']
    a3.SIB9YOB = record['sib9yob']
    a3.SIB9AGD = record['sib9agd']
    a3.SIB9NEU = record['sib9neu']
    a3.SIB9PDX = record['sib9pdx']
    a3.SIB9MOE = record['sib9moe']
    a3.SIB9AGO = record['sib9ago']
    a3.SIB10MOB = record['sib10mob']
    a3.SIB10YOB = record['sib10yob']
    a3.SIB10AGD = record['sib10agd']
    a3.SIB10NEU = record['sib10neu']
    a3.SIB10PDX = record['sib10pdx']
    a3.SIB10MOE = record['sib10moe']
    a3.SIB10AGO = record['sib10ago']
    a3.SIB11MOB = record['sib11mob']
    a3.SIB11YOB = record['sib11yob']
    a3.SIB11AGD = record['sib11agd']
    a3.SIB11NEU = record['sib11neu']
    a3.SIB11PDX = record['sib11pdx']
    a3.SIB11MOE = record['sib11moe']
    a3.SIB11AGO = record['sib11ago']
    a3.SIB12MOB = record['sib12mob']
    a3.SIB12YOB = record['sib12yob']
    a3.SIB12AGD = record['sib12agd']
    a3.SIB12NEU = record['sib12neu']
    a3.SIB12PDX = record['sib12pdx']
    a3.SIB12MOE = record['sib12moe']
    a3.SIB12AGO = record['sib12ago']
    a3.SIB13MOB = record['sib13mob']
    a3.SIB13YOB = record['sib13yob']
    a3.SIB13AGD = record['sib13agd']
    a3.SIB13NEU = record['sib13neu']
    a3.SIB13PDX = record['sib13pdx']
    a3.SIB13MOE = record['sib13moe']
    a3.SIB13AGO = record['sib13ago']
    a3.SIB14MOB = record['sib14mob']
    a3.SIB14YOB = record['sib14yob']
    a3.SIB14AGD = record['sib14agd']
    a3.SIB14NEU = record['sib14neu']
    a3.SIB14PDX = record['sib14pdx']
    a3.SIB14MOE = record['sib14moe']
    a3.SIB14AGO = record['sib14ago']
    a3.SIB15MOB = record['sib15mob']
    a3.SIB15YOB = record['sib15yob']
    a3.SIB15AGD = record['sib15agd']
    a3.SIB15NEU = record['sib15neu']
    a3.SIB15PDX = record['sib15pdx']
    a3.SIB15MOE = record['sib15moe']
    a3.SIB15AGO = record['sib15ago']
    a3.SIB16MOB = record['sib16mob']
    a3.SIB16YOB = record['sib16yob']
    a3.SIB16AGD = record['sib16agd']
    a3.SIB16NEU = record['sib16neu']
    a3.SIB16PDX = record['sib16pdx']
    a3.SIB16MOE = record['sib16moe']
    a3.SIB16AGO = record['sib16ago']
    a3.SIB17MOB = record['sib17mob']
    a3.SIB17YOB = record['sib17yob']
    a3.SIB17AGD = record['sib17agd']
    a3.SIB17NEU = record['sib17neu']
    a3.SIB17PDX = record['sib17pdx']
    a3.SIB17MOE = record['sib17moe']
    a3.SIB17AGO = record['sib17ago']
    a3.SIB18MOB = record['sib18mob']
    a3.SIB18YOB = record['sib18yob']
    a3.SIB18AGD = record['sib18agd']
    a3.SIB18NEU = record['sib18neu']
    a3.SIB18PDX = record['sib18pdx']
    a3.SIB18MOE = record['sib18moe']
    a3.SIB18AGO = record['sib18ago']
    a3.SIB19MOB = record['sib19mob']
    a3.SIB19YOB = record['sib19yob']
    a3.SIB19AGD = record['sib19agd']
    a3.SIB19NEU = record['sib19neu']
    a3.SIB19PDX = record['sib19pdx']
    a3.SIB19MOE = record['sib19moe']
    a3.SIB19AGO = record['sib19ago']
    a3.SIB20MOB = record['sib20mob']
    a3.SIB20YOB = record['sib20yob']
    a3.SIB20AGD = record['sib20agd']
    a3.SIB20NEU = record['sib20neu']
    a3.SIB20PDX = record['sib20pdx']
    a3.SIB20MOE = record['sib20moe']
    a3.SIB20AGO = record['sib20ago']
    a3.KIDS = record['kids']
    a3.KID1MOB = record['kid1mob']
    a3.KID1YOB = record['kid1yob']
    a3.KID1AGD = record['kid1agd']
    a3.KID1NEU = record['kid1neu']
    a3.KID1PDX = record['kid1pdx']
    a3.KID1MOE = record['kid1moe']
    a3.KID1AGO = record['kid1ago']
    a3.KID2MOB = record['kid2mob']
    a3.KID2YOB = record['kid2yob']
    a3.KID2AGD = record['kid2agd']
    a3.KID2NEU = record['kid2neu']
    a3.KID2PDX = record['kid2pdx']
    a3.KID2MOE = record['kid2moe']
    a3.KID2AGO = record['kid2ago']
    a3.KID3MOB = record['kid3mob']
    a3.KID3YOB = record['kid3yob']
    a3.KID3AGD = record['kid3agd']
    a3.KID3NEU = record['kid3neu']
    a3.KID3PDX = record['kid3pdx']
    a3.KID3MOE = record['kid3moe']
    a3.KID3AGO = record['kid3ago']
    a3.KID4MOB = record['kid4mob']
    a3.KID4YOB = record['kid4yob']
    a3.KID4AGD = record['kid4agd']
    a3.KID4NEU = record['kid4neu']
    a3.KID4PDX = record['kid4pdx']
    a3.KID4MOE = record['kid4moe']
    a3.KID4AGO = record['kid4ago']
    a3.KID5MOB = record['kid5mob']
    a3.KID5YOB = record['kid5yob']
    a3.KID5AGD = record['kid5agd']
    a3.KID5NEU = record['kid5neu']
    a3.KID5PDX = record['kid5pdx']
    a3.KID5MOE = record['kid5moe']
    a3.KID5AGO = record['kid5ago']
    a3.KID6MOB = record['kid6mob']
    a3.KID6YOB = record['kid6yob']
    a3.KID6AGD = record['kid6agd']
    a3.KID6NEU = record['kid6neu']
    a3.KID6PDX = record['kid6pdx']
    a3.KID6MOE = record['kid6moe']
    a3.KID6AGO = record['kid6ago']
    a3.KID7MOB = record['kid7mob']
    a3.KID7YOB = record['kid7yob']
    a3.KID7AGD = record['kid7agd']
    a3.KID7NEU = record['kid7neu']
    a3.KID7PDX = record['kid7pdx']
    a3.KID7MOE = record['kid7moe']
    a3.KID7AGO = record['kid7ago']
    a3.KID8MOB = record['kid8mob']
    a3.KID8YOB = record['kid8yob']
    a3.KID8AGD = record['kid8agd']
    a3.KID8NEU = record['kid8neu']
    a3.KID8PDX = record['kid8pdx']
    a3.KID8MOE = record['kid8moe']
    a3.KID8AGO = record['kid8ago']
    a3.KID9MOB = record['kid9mob']
    a3.KID9YOB = record['kid9yob']
    a3.KID9AGD = record['kid9agd']
    a3.KID9NEU = record['kid9neu']
    a3.KID9PDX = record['kid9pdx']
    a3.KID9MOE = record['kid9moe']
    a3.KID9AGO = record['kid9ago']
    a3.KID10MOB = record['kid10mob']
    a3.KID10YOB = record['kid10yob']
    a3.KID10AGD = record['kid10agd']
    a3.KID10NEU = record['kid10neu']
    a3.KID10PDX = record['kid10pdx']
    a3.KID10MOE = record['kid10moe']
    a3.KID10AGO = record['kid10ago']
    a3.KID11MOB = record['kid11mob']
    a3.KID11YOB = record['kid11yob']
    a3.KID11AGD = record['kid11agd']
    a3.KID11NEU = record['kid11neu']
    a3.KID11PDX = record['kid11pdx']
    a3.KID11MOE = record['kid11moe']
    a3.KID11AGO = record['kid11ago']
    a3.KID12MOB = record['kid12mob']
    a3.KID12YOB = record['kid12yob']
    a3.KID12AGD = record['kid12agd']
    a3.KID12NEU = record['kid12neu']
    a3.KID12PDX = record['kid12pdx']
    a3.KID12MOE = record['kid12moe']
    a3.KID12AGO = record['kid12ago']
    a3.KID13MOB = record['kid13mob']
    a3.KID13YOB = record['kid13yob']
    a3.KID13AGD = record['kid13agd']
    a3.KID13NEU = record['kid13neu']
    a3.KID13PDX = record['kid13pdx']
    a3.KID13MOE = record['kid13moe']
    a3.KID13AGO = record['kid13ago']
    a3.KID14MOB = record['kid14mob']
    a3.KID14YOB = record['kid14yob']
    a3.KID14AGD = record['kid14agd']
    a3.KID14NEU = record['kid14neu']
    a3.KID14PDX = record['kid14pdx']
    a3.KID14MOE = record['kid14moe']
    a3.KID14AGO = record['kid14ago']
    a3.KID15MOB = record['kid15mob']
    a3.KID15YOB = record['kid15yob']
    a3.KID15AGD = record['kid15agd']
    a3.KID15NEU = record['kid15neu']
    a3.KID15PDX = record['kid15pdx']
    a3.KID15MOE = record['kid15moe']
    a3.KID15AGO = record['kid15ago']
    packet.append(a3)


def add_a4(record, packet):
    # Form A4D and A4G are special in that our REDCap implementation (IVP A4)
    # combines them by asking if the subject is taking any medications (which
    # corresponds to A4G.ANYMEDS), then has 50 fields to specify each
    # medication used, which we turn each one into a FormA4D object.
    a4g = ivp_forms.FormA4G()
    a4g.ANYMEDS = record['anymeds']
    packet.append(a4g)

    if a4g.ANYMEDS == 1:
        for i in range(1, 51):
            key = 'drugid_' + str(i)
            if record[key]:
                a4d = ivp_forms.FormA4D()
                a4d.DRUGID = record[key]
                packet.append(a4d)


def add_a5(record, packet):
    a5 = ivp_forms.FormA5()
    a5.TOBAC30 = record['tobac30']
    a5.TOBAC100 = record['tobac100']
    a5.SMOKYRS = record['smokyrs']
    a5.PACKSPER = record['packsper']
    a5.QUITSMOK = record['quitsmok']
    a5.ALCOCCAS = record['alcoccas']
    a5.ALCFREQ = record['alcfreq']
    a5.CVHATT = record['cvhatt']
    a5.HATTMULT = record['hattmult']
    a5.HATTYEAR = record['hattyear']
    a5.CVAFIB = record['cvafib']
    a5.CVANGIO = record['cvangio']
    a5.CVBYPASS = record['cvbypass']
    a5.CVPACDEF = record['cvpacdef']
    a5.CVCHF = record['cvchf']
    a5.CVANGINA = record['cvangina']
    a5.CVHVALVE = record['cvhvalve']
    a5.CVOTHR = record['cvothr']
    a5.CVOTHRX = record['cvothrx']
    a5.CBSTROKE = record['cbstroke']
    a5.STROKMUL = record['strokmul']
    a5.STROKYR = record['strokyr']
    a5.CBTIA = record['cbtia']
    a5.TIAMULT = record['tiamult']
    a5.TIAYEAR = record['tiayear']
    a5.PD = record['pd']
    a5.PDYR = record['pdyr']
    a5.PDOTHR = record['pdothr']
    a5.PDOTHRYR = record['pdothryr']
    a5.SEIZURES = record['seizures']
    a5.TBI = record['tbi']
    a5.TBIBRIEF = record['tbibrief']
    a5.TBIEXTEN = record['tbiexten']
    a5.TBIWOLOS = record['tbiwolos']
    a5.TBIYEAR = record['tbiyear']
    a5.DIABETES = record['diabetes']
    a5.DIABTYPE = record['diabtype']
    a5.HYPERTEN = record['hyperten']
    a5.HYPERCHO = record['hypercho']
    a5.B12DEF = record['b12def']
    a5.THYROID = record['thyroid']
    a5.ARTHRIT = record['arthrit']
    a5.ARTHTYPE = record['arthtype']
    a5.ARTHTYPX = record['arthtypx']
    a5.ARTHUPEX = record['arthupex']
    a5.ARTHLOEX = record['arthloex']
    a5.ARTHSPIN = record['arthspin']
    a5.ARTHUNK = record['arthunk']
    a5.INCONTU = record['incontu']
    a5.INCONTF = record['incontf']
    a5.APNEA = record['apnea']
    a5.RBD = record['rbd']
    a5.INSOMN = record['insomn']
    a5.OTHSLEEP = record['othsleep']
    a5.OTHSLEEX = record['othsleex']
    a5.ALCOHOL = record['alcohol']
    a5.ABUSOTHR = record['abusothr']
    a5.ABUSX = record['abusx']
    a5.PTSD = record['ptsd']
    a5.BIPOLAR = record['bipolar']
    a5.SCHIZ = record['schiz']
    a5.DEP2YRS = record['dep2yrs']
    a5.DEPOTHR = record['depothr']
    a5.ANXIETY = record['anxiety']
    a5.OCD = record['ocd']
    a5.NPSYDEV = record['npsydev']
    a5.PSYCDIS = record['psycdis']
    a5.PSYCDISX = record['psycdisx']

    if a5.ARTHRIT == 0:
        a5.ARTHUPEX = ''
        a5.ARTHLOEX = ''
        a5.ARTHSPIN = ''
        a5.ARTHUNK = ''
    packet.append(a5)


def add_b1(record, packet):
    b1 = ivp_forms.FormB1()
    b1.HEIGHT = record['height']
    b1.WEIGHT = record['weight']
    b1.BPSYS = record['bpsys']
    b1.BPDIAS = record['bpdias']
    b1.HRATE = record['hrate']
    b1.VISION = record['vision']
    b1.VISCORR = record['viscorr']
    b1.VISWCORR = record['viswcorr']
    b1.HEARING = record['hearing']
    b1.HEARAID = record['hearaid']
    b1.HEARWAID = record['hearwaid']
    packet.append(b1)


def add_b4(record, packet):
    b4 = ivp_forms.FormB4()
    b4.MEMORY = record['memory']
    b4.ORIENT = record['orient']
    b4.JUDGMENT = record['judgment']
    b4.COMMUN = record['commun']
    b4.HOMEHOBB = record['homehobb']
    b4.PERSCARE = record['perscare']
    b4.CDRSUM = record['cdrsum']
    b4.CDRGLOB = record['cdrglob']
    b4.COMPORT = record['comport']
    b4.CDRLANG = record['cdrlang']
    packet.append(b4)


def add_b5(record, packet):
    b5 = ivp_forms.FormB5()
    b5.NPIQINF = record['npiqinf']
    b5.NPIQINFX = record['npiqinfx']
    b5.DEL = record['del']
    b5.DELSEV = record['delsev']
    b5.HALL = record['hall']
    b5.HALLSEV = record['hallsev']
    b5.AGIT = record['agit']
    b5.AGITSEV = record['agitsev']
    b5.DEPD = record['depd']
    b5.DEPDSEV = record['depdsev']
    b5.ANX = record['anx']
    b5.ANXSEV = record['anxsev']
    b5.ELAT = record['elat']
    b5.ELATSEV = record['elatsev']
    b5.APA = record['apa']
    b5.APASEV = record['apasev']
    b5.DISN = record['disn']
    b5.DISNSEV = record['disnsev']
    b5.IRR = record['irr']
    b5.IRRSEV = record['irrsev']
    b5.MOT = record['mot']
    b5.MOTSEV = record['motsev']
    b5.NITE = record['nite']
    b5.NITESEV = record['nitesev']
    b5.APP = record['app']
    b5.APPSEV = record['appsev']
    packet.append(b5)


def add_b6(record, packet):
    b6 = ivp_forms.FormB6()
    b6.NOGDS = record['nogds']
    b6.SATIS = record['satis']
    b6.DROPACT = record['dropact']
    b6.EMPTY = record['empty']
    b6.BORED = record['bored']
    b6.SPIRITS = record['spirits']
    b6.AFRAID = record['afraid']
    b6.HAPPY = record['happy']
    b6.HELPLESS = record['helpless']
    b6.STAYHOME = record['stayhome']
    b6.MEMPROB = record['memprob']
    b6.WONDRFUL = record['wondrful']
    b6.WRTHLESS = record['wrthless']
    b6.ENERGY = record['energy']
    b6.HOPELESS = record['hopeless']
    b6.BETTER = record['better']
    b6.GDS = record['gds']
    packet.append(b6)


def add_b7(record, packet):
    b7 = ivp_forms.FormB7()
    b7.BILLS = record['bills']
    b7.TAXES = record['taxes']
    b7.SHOPPING = record['shopping']
    b7.GAMES = record['games']
    b7.STOVE = record['stove']
    b7.MEALPREP = record['mealprep']
    b7.EVENTS = record['events']
    b7.PAYATTN = record['payattn']
    b7.REMDATES = record['remdates']
    b7.TRAVEL = record['travel']
    packet.append(b7)


def add_b8(record, packet):
    b8 = ivp_forms.FormB8()
    b8.NORMEXAM = record['normexam']
    b8.PARKSIGN = record['parksign']
    b8.RESTTRL = record['resttrl']
    b8.SLOWINGL = record['slowingl']
    b8.RIGIDL = record['rigidl']
    b8.RESTTRR = record['resttrr']
    b8.SLOWINGR = record['slowingr']
    b8.RIGIDR = record['rigidr']
    b8.BRADY = record['brady']
    b8.PARKGAIT = record['parkgait']
    b8.POSTINST = record['postinst']
    b8.CVDSIGNS = record['cvdsigns']
    b8.CORTDEF = record['cortdef']
    b8.SIVDFIND = record['sivdfind']
    b8.CVDMOTL = record['cvdmotl']
    b8.CORTVISL = record['cortvisl']
    b8.SOMATL = record['somatl']
    b8.CVDMOTR = record['cvdmotr']
    b8.CORTVISR = record['cortvisr']
    b8.SOMATR = record['somatr']
    b8.POSTCORT = record['postcort']
    b8.PSPCBS = record['pspcbs']
    b8.EYEPSP = record['eyepsp']
    b8.DYSPSP = record['dyspsp']
    b8.AXIALPSP = record['axialpsp']
    b8.GAITPSP = record['gaitpsp']
    b8.APRAXSP = record['apraxsp']
    b8.APRAXL = record['apraxl']
    b8.CORTSENL = record['cortsenl']
    b8.ATAXL = record['ataxl']
    b8.ALIENLML = record['alienlml']
    b8.DYSTONL = record['dystonl']
    b8.MYOCLLT = record['myocllt']
    b8.APRAXR = record['apraxr']
    b8.CORTSENR = record['cortsenr']
    b8.ATAXR = record['ataxr']
    b8.ALIENLMR = record['alienlmr']
    b8.DYSTONR = record['dystonr']
    b8.MYOCLRT = record['myoclrt']
    b8.ALSFIND = record['alsfind']
    b8.GAITNPH = record['gaitnph']
    b8.OTHNEUR = record['othneur']
    b8.OTHNEURX = record['othneurx']
    packet.append(b8)


def add_b9(record, packet):
    b9 = ivp_forms.FormB9()
    b9.DECSUB = record['decsub']
    b9.DECIN = record['decin']
    b9.DECCLCOG = record['decclcog']
    b9.COGMEM = record['cogmem']
    b9.COGORI = record['cogori']
    b9.COGJUDG = record['cogjudg']
    b9.COGLANG = record['coglang']
    b9.COGVIS = record['cogvis']
    b9.COGATTN = record['cogattn']
    b9.COGFLUC = record['cogfluc']
    b9.COGFLAGO = record['cogflago']
    b9.COGOTHR = record['cogothr']
    b9.COGOTHRX = record['cogothrx']
    b9.COGFPRED = record['cogfpred']
    b9.COGFPREX = record['cogfprex']
    b9.COGMODE = record['cogmode']
    b9.COGMODEX = record['cogmodex']
    b9.DECAGE = record['decage']
    b9.DECCLBE = record['decclbe']
    b9.BEAPATHY = record['beapathy']
    b9.BEDEP = record['bedep']
    b9.BEVHALL = record['bevhall']
    b9.BEVWELL = record['bevwell']
    b9.BEVHAGO = record['bevhago']
    b9.BEAHALL = record['beahall']
    b9.BEDEL = record['bedel']
    b9.BEDISIN = record['bedisin']
    b9.BEIRRIT = record['beirrit']
    b9.BEAGIT = record['beagit']
    b9.BEPERCH = record['beperch']
    b9.BEREM = record['berem']
    b9.BEREMAGO = record['beremago']
    b9.BEANX = record['beanx']
    b9.BEOTHR = record['beothr']
    b9.BEOTHRX = record['beothrx']
    b9.BEFPRED = record['befpred']
    b9.BEFPREDX = record['befpredx']
    b9.BEMODE = record['bemode']
    b9.BEMODEX = record['bemodex']
    b9.BEAGE = record['beage']
    b9.DECCLMOT = record['decclmot']
    b9.MOGAIT = record['mogait']
    b9.MOFALLS = record['mofalls']
    b9.MOTREM = record['motrem']
    b9.MOSLOW = record['moslow']
    b9.MOFRST = record['mofrst']
    b9.MOMODE = record['momode']
    b9.MOMODEX = record['momodex']
    b9.MOMOPARK = record['momopark']
    b9.PARKAGE = record['parkage']
    b9.MOMOALS = record['momoals']
    b9.ALSAGE = record['alsage']
    b9.MOAGE = record['moage']
    b9.COURSE = record['course']
    b9.FRSTCHG = record['frstchg']
    b9.LBDEVAL = record['lbdeval']
    b9.FTLDEVAL = record['ftldeval']
    packet.append(b9)


def add_c1s_or_c2(record, packet):
    c2 = ivp_forms.FormC2()
    c2_filled_fields = 0
    c2_field_mapping = {
        'MOCACOMP': 'mocacomp',
        'MOCAREAS': 'mocareas',
        'MOCALOC': 'mocaloc',
        'MOCALAN': 'mocalan',
        'MOCALANX': 'mocalanx',
        'MOCAVIS': 'mocavis',
        'MOCAHEAR': 'mocahear',
        'MOCATOTS': 'mocatots',
        'MOCATRAI': 'mocatrai',
        'MOCACUBE': 'mocacube',
        'MOCACLOC': 'mocacloc',
        'MOCACLON': 'mocaclon',
        'MOCACLOH': 'mocacloh',
        'MOCANAMI': 'mocanami',
        'MOCAREGI': 'mocaregi',
        'MOCADIGI': 'mocadigi',
        'MOCALETT': 'mocalett',
        'MOCASER7': 'mocaser7',
        'MOCAREPE': 'mocarepe',
        'MOCAFLUE': 'mocaflue',
        'MOCAABST': 'mocaabst',
        'MOCARECN': 'mocarecn',
        'MOCARECC': 'mocarecc',
        'MOCARECR': 'mocarecr',
        'MOCAORDT': 'mocaordt',
        'MOCAORMO': 'mocaormo',
        'MOCAORYR': 'mocaoryr',
        'MOCAORDY': 'mocaordy',
        'MOCAORPL': 'mocaorpl',
        'MOCAORCT': 'mocaorct',
        'NPSYCLOC': 'npsycloc_c2',
        'NPSYLAN': 'npsylan_c2',
        'NPSYLANX': 'npsylanx_c2',
        'CRAFTVRS': 'craftvrs',
        'CRAFTURS': 'crafturs',
        'UDSBENTC': 'udsbentc',
        'DIGFORCT': 'digforct',
        'DIGFORSL': 'digforsl',
        'DIGBACCT': 'digbacct',
        'DIGBACLS': 'digbacls',
        'ANIMALS': 'animals_c2',
        'VEG': 'veg_c2',
        'TRAILA': 'traila_c2',
        'TRAILARR': 'trailarr_c2',
        'TRAILALI': 'trailali_c2',
        'TRAILB': 'trailb_c2',
        'TRAILBRR': 'trailbrr_c2',
        'TRAILBLI': 'trailbli_c2',
        'CRAFTDVR': 'craftdvr',
        'CRAFTDRE': 'craftdre',
        'CRAFTDTI': 'craftdti',
        'CRAFTCUE': 'craftcue',
        'UDSBENTD': 'udsbentd',
        'UDSBENRS': 'udsbenrs',
        'MINTTOTS': 'minttots',
        'MINTTOTW': 'minttotw',
        'MINTSCNG': 'mintscng',
        'MINTSCNC': 'mintscnc',
        'MINTPCNG': 'mintpcng',
        'MINTPCNC': 'mintpcnc',
        'UDSVERFC': 'udsverfc',
        'UDSVERFN': 'udsverfn',
        'UDSVERNF': 'udsvernf',
        'UDSVERLC': 'udsverlc',
        'UDSVERLR': 'udsverlr',
        'UDSVERLN': 'udsverln',
        'UDSVERTN': 'udsvertn',
        'UDSVERTE': 'udsverte',
        'UDSVERTI': 'udsverti',
        'COGSTAT': 'cogstat_c2'
    }
    for key, value in c2_field_mapping.items():
        try:
            if record[value].strip():
                setattr(c2, key, record[value])
                c2_filled_fields += 1
        except KeyError:
            pass

    c1s = ivp_forms.FormC1S()
    c1s_filled_fields = 0
    c1s_field_mapping = {
        'MMSELOC': 'c1s_1a_mmseloc',
        'MMSELAN': 'c1s_1a1_mmselan',
        'MMSELANX': 'c1s_1a2_mmselanx',
        'MMSEORDA': 'c1s_1b1_mmseorda',
        'MMSEORLO': 'c1s_1b2_mmseorlo',
        'PENTAGON': 'c1s_1c_pentagon',
        'MMSE': 'c1s_1d_mmse',
        'NPSYCLOC': 'c1s_2_npsycloc',
        'NPSYLAN': 'c1s_2a_npsylan',
        'NPSYLANX': 'c1s_2a1_npsylanx',
        'LOGIMO': 'c1s_3amo_logimo',
        'LOGIDAY': 'c1s_3ady_logiday',
        'LOGIYR': 'c1s_3ayr_logiyr',
        'LOGIPREV': 'c1s_3a1_logiprev',
        'LOGIMEM': 'c1s_3b_logimem',
        'DIGIF': 'c1s_4a_digif',
        'DIGIFLEN': 'c1s_4b_digiflen',
        'DIGIB': 'c1s_5a_digib',
        'DIGIBLEN': 'c1s_5b_digiblen',
        'ANIMALS': 'c1s_6a_animals',
        'VEG': 'c1s_6b_veg',
        'TRAILA': 'c1s_7a_traila',
        'TRAILARR': 'c1s_7a1_trailarr',
        'TRAILALI': 'c1s_7a2_trailali',
        'TRAILB': 'c1s_7b_trailb',
        'TRAILBRR': 'c1s_7b1_trailbrr',
        'TRAILBLI': 'c1s_7b2_trailbli',
        'WAIS': 'c1s_8a_wais',
        'MEMUNITS': 'c1s_9a_memunits',
        'MEMTIME': 'c1s_9b_memtime',
        'BOSTON': 'c1s_10a_boston',
        'COGSTAT': 'c1s_11a_cogstat'
    }
    for key, value in c1s_field_mapping.items():
        try:
            if record[value].strip():
                setattr(c1s, key, record[value])
                c1s_filled_fields += 1
        except KeyError:
            pass

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
    d1 = ivp_forms.FormD1()
    d1.DXMETHOD = record['dxmethod']
    d1.NORMCOG = record['normcog']
    d1.DEMENTED = record['demented']
    d1.AMNDEM = record['amndem']
    d1.PCA = record['pca']
    d1.PPASYN = record['ppasyn']
    d1.PPASYNT = record['ppasynt']
    d1.FTDSYN = record['ftdsyn']
    d1.LBDSYN = record['lbdsyn']
    d1.NAMNDEM = record['namndem']
    d1.MCIAMEM = record['mciamem']
    d1.MCIAPLUS = record['mciaplus']
    d1.MCIAPLAN = record['mciaplan']
    d1.MCIAPATT = record['mciapatt']
    d1.MCIAPEX = record['mciapex']
    d1.MCIAPVIS = record['mciapvis']
    d1.MCINON1 = record['mcinon1']
    d1.MCIN1LAN = record['mcin1lan']
    d1.MCIN1ATT = record['mcin1att']
    d1.MCIN1EX = record['mcin1ex']
    d1.MCIN1VIS = record['mcin1vis']
    d1.MCINON2 = record['mcinon2']
    d1.MCIN2LAN = record['mcin2lan']
    d1.MCIN2ATT = record['mcin2att']
    d1.MCIN2EX = record['mcin2ex']
    d1.MCIN2VIS = record['mcin2vis']
    d1.IMPNOMCI = record['impnomci']
    d1.AMYLPET = record['amylpet']
    d1.AMYLCSF = record['amylcsf']
    d1.FDGAD = record['fdgad']
    d1.HIPPATR = record['hippatr']
    d1.TAUPETAD = record['taupetad']
    d1.CSFTAU = record['csftau']
    d1.FDGFTLD = record['fdgftld']
    d1.TPETFTLD = record['tpetftld']
    d1.MRFTLD = record['mrftld']
    d1.DATSCAN = record['datscan']
    d1.OTHBIOM = record['othbiom']
    d1.OTHBIOMX = record['othbiomx']
    d1.IMAGLINF = record['imaglinf']
    d1.IMAGLAC = record['imaglac']
    d1.IMAGMACH = record['imagmach']
    d1.IMAGMICH = record['imagmich']
    d1.IMAGMWMH = record['imagmwmh']
    d1.IMAGEWMH = record['imagewmh']
    d1.ADMUT = record['admut']
    d1.FTLDMUT = record['ftldmut']
    d1.OTHMUT = record['othmut']
    d1.OTHMUTX = record['othmutx']
    d1.ALZDIS = record['alzdis']
    d1.ALZDISIF = record['alzdisif']
    d1.LBDIS = record['lbdis']
    d1.LBDIF = record['lbdif']
    d1.PARK = record['park']
    d1.MSA = record['msa']
    d1.MSAIF = record['msaif']
    d1.PSP = record['psp']
    d1.PSPIF = record['pspif']
    d1.CORT = record['cort']
    d1.CORTIF = record['cortif']
    d1.FTLDMO = record['ftldmo']
    d1.FTLDMOIF = record['ftldmoif']
    d1.FTLDNOS = record['ftldnos']
    d1.FTLDNOIF = record['ftldnoif']
    d1.FTLDSUBT = record['ftldsubt']
    d1.FTLDSUBX = record['ftldsubx']
    d1.CVD = record['cvd']
    d1.CVDIF = record['cvdif']
    d1.PREVSTK = record['prevstk']
    d1.STROKDEC = record['strokdec']
    d1.STKIMAG = record['stkimag']
    d1.INFNETW = record['infnetw']
    d1.INFWMH = record['infwmh']
    d1.ESSTREM = record['esstrem']
    d1.ESSTREIF = record['esstreif']
    d1.DOWNS = record['downs']
    d1.DOWNSIF = record['downsif']
    d1.HUNT = record['hunt']
    d1.HUNTIF = record['huntif']
    d1.PRION = record['prion']
    d1.PRIONIF = record['prionif']
    d1.BRNINJ = record['brninj']
    d1.BRNINJIF = record['brninjif']
    d1.BRNINCTE = record['brnincte']
    d1.HYCEPH = record['hyceph']
    d1.HYCEPHIF = record['hycephif']
    d1.EPILEP = record['epilep']
    d1.EPILEPIF = record['epilepif']
    d1.NEOP = record['neop']
    d1.NEOPIF = record['neopif']
    d1.NEOPSTAT = record['neopstat']
    d1.HIV = record['hiv']
    d1.HIVIF = record['hivif']
    d1.OTHCOG = record['othcog']
    d1.OTHCOGIF = record['othcogif']
    d1.OTHCOGX = record['othcogx']
    d1.DEP = record['dep']
    d1.DEPIF = record['depif']
    d1.DEPTREAT = record['deptreat']
    d1.BIPOLDX = record['bipoldx']
    d1.BIPOLDIF = record['bipoldif']
    d1.SCHIZOP = record['schizop']
    d1.SCHIZOIF = record['schizoif']
    d1.ANXIET = record['anxiet']
    d1.ANXIETIF = record['anxietif']
    d1.DELIR = record['delir']
    d1.DELIRIF = record['delirif']
    d1.PTSDDX = record['ptsddx']
    d1.PTSDDXIF = record['ptsddxif']
    d1.OTHPSY = record['othpsy']
    d1.OTHPSYIF = record['othpsyif']
    d1.OTHPSYX = record['othpsyx']
    d1.ALCDEM = record['alcdem']
    d1.ALCDEMIF = record['alcdemif']
    d1.ALCABUSE = record['alcabuse']
    d1.IMPSUB = record['impsub']
    d1.IMPSUBIF = record['impsubif']
    d1.DYSILL = record['dysill']
    d1.DYSILLIF = record['dysillif']
    d1.MEDS = record['meds']
    d1.MEDSIF = record['medsif']
    d1.COGOTH = record['cogoth']
    d1.COGOTHIF = record['cogothif']
    d1.COGOTHX = record['cogothx']
    d1.COGOTH2 = record['cogoth2']
    d1.COGOTH2F = record['cogoth2f']
    d1.COGOTH2X = record['cogoth2x']
    d1.COGOTH3 = record['cogoth3']
    d1.COGOTH3F = record['cogoth3f']
    d1.COGOTH3X = record['cogoth3x']
    packet.append(d1)


def add_d2(record, packet):
    d2 = ivp_forms.FormD2()
    d2.CANCER = record['cancer']
    d2.CANCSITE = record['cancsite']
    d2.DIABET = record['diabet']
    d2.MYOINF = record['myoinf']
    d2.CONGHRT = record['conghrt']
    d2.AFIBRILL = record['afibrill']
    d2.HYPERT = record['hypert']
    d2.ANGINA = record['angina']
    d2.HYPCHOL = record['hypchol']
    d2.VB12DEF = record['vb12def']
    d2.THYDIS = record['thydis']
    d2.ARTH = record['arth']
    d2.ARTYPE = record['artype']
    d2.ARTYPEX = record['artypex']
    d2.ARTUPEX = record['artupex']
    d2.ARTLOEX = record['artloex']
    d2.ARTSPIN = record['artspin']
    d2.ARTUNKN = record['artunkn']

    d2.URINEINC = record['urineinc']
    d2.BOWLINC = record['bowlinc']
    d2.SLEEPAP = record['sleepap']
    d2.REMDIS = record['remdis']
    d2.HYPOSOM = record['hyposom']
    d2.SLEEPOTH = record['sleepoth']
    d2.SLEEPOTX = record['sleepotx']
    d2.ANGIOCP = record['angiocp']
    d2.ANGIOPCI = record['angiopci']
    d2.PACEMAKE = record['pacemake']
    d2.HVALVE = record['hvalve']
    d2.ANTIENC = record['antienc']
    d2.ANTIENCX = record['antiencx']
    d2.OTHCOND = record['othcond']
    d2.OTHCONDX = record['othcondx']
    packet.append(d2)

    add_z1_or_z1x(record, packet)
    update_header(record, packet)

    return packet


def add_c1s_or_c2(record, packet):
    # Among C1S and C2 forms, one must be filled, one must be empty. After 2017/10/23, must be C2
    if (int(record['visityr'])>2017) or (int(record['visityr'])==2017 and int(record['visitmo'])>10) or \
       (int(record['visityr'])==2017 and int(record['visitmo'])==10 and int(record['visitday'])>=23):
        c2 = ivp_forms.FormC2()
        c2.MOCACOMP = record['mocacomp']
        c2.MOCAREAS = record['mocareas']
        c2.MOCALOC = record['mocaloc']
        c2.MOCALAN = record['mocalan']
        c2.MOCALANX = record['mocalanx']
        c2.MOCAVIS = record['mocavis']
        c2.MOCAHEAR = record['mocahear']
        c2.MOCATOTS = record['mocatots']
        c2.MOCATRAI = record['mocatrai']
        c2.MOCACUBE = record['mocacube']
        c2.MOCACLOC = record['mocacloc']
        c2.MOCACLON = record['mocaclon']
        c2.MOCACLOH = record['mocacloh']
        c2.MOCANAMI = record['mocanami']
        c2.MOCAREGI = record['mocaregi']
        c2.MOCADIGI = record['mocadigi']
        c2.MOCALETT = record['mocalett']
        c2.MOCASER7 = record['mocaser7']
        c2.MOCAREPE = record['mocarepe']
        c2.MOCAFLUE = record['mocaflue']
        c2.MOCAABST = record['mocaabst']
        c2.MOCARECN = record['mocarecn']
        c2.MOCARECC = record['mocarecc']
        c2.MOCARECR = record['mocarecr']
        c2.MOCAORDT = record['mocaordt']
        c2.MOCAORMO = record['mocaormo']
        c2.MOCAORYR = record['mocaoryr']
        c2.MOCAORDY = record['mocaordy']
        c2.MOCAORPL = record['mocaorpl']
        c2.MOCAORCT = record['mocaorct']
        c2.NPSYCLOC = record['npsycloc_c2']
        c2.NPSYLAN = record['npsylan_c2']
        c2.NPSYLANX = record['npsylanx_c2']
        c2.CRAFTVRS = record['craftvrs']
        c2.CRAFTURS = record['crafturs']
        c2.UDSBENTC = record['udsbentc']
        c2.DIGFORCT = record['digforct']
        c2.DIGFORSL = record['digforsl']
        c2.DIGBACCT = record['digbacct']
        c2.DIGBACLS = record['digbacls']
        c2.ANIMALS = record['animals_c2']
        c2.VEG = record['veg_c2']
        c2.TRAILA = record['traila_c2']
        c2.TRAILARR = record['trailarr_c2']
        c2.TRAILALI = record['trailali_c2']
        c2.TRAILB = record['trailb_c2']
        c2.TRAILBRR = record['trailbrr_c2']
        c2.TRAILBLI = record['trailbli_c2']
        c2.CRAFTDVR = record['craftdvr']
        c2.CRAFTDRE = record['craftdre']
        c2.CRAFTDTI = record['craftdti']
        c2.CRAFTCUE = record['craftcue']
        c2.UDSBENTD = record['udsbentd']
        c2.UDSBENRS = record['udsbenrs']
        c2.MINTTOTS = record['minttots']
        c2.MINTTOTW = record['minttotw']
        c2.MINTSCNG = record['mintscng']
        c2.MINTSCNC = record['mintscnc']
        c2.MINTPCNG = record['mintpcng']
        c2.MINTPCNC = record['mintpcnc']
        c2.UDSVERFC = record['udsverfc']
        c2.UDSVERFN = record['udsverfn']
        c2.UDSVERNF = record['udsvernf']
        c2.UDSVERLC = record['udsverlc']
        c2.UDSVERLR = record['udsverlr']
        c2.UDSVERLN = record['udsverln']
        c2.UDSVERTN = record['udsvertn']
        c2.UDSVERTE = record['udsverte']
        c2.UDSVERTI = record['udsverti']
        c2.COGSTAT = record['cogstat_c2']
        packet.append(c2)
    else:
        c1s = ivp_forms.FormC1S()
        c1s.MMSELOC = record['c1s_1a_mmseloc'] #check for blank
        c1s.MMSELAN = record['c1s_1a1_mmselan']
        c1s.MMSELANX = record['c1s_1a2_mmselanx']
        c1s.MMSEORDA = record['c1s_1b1_mmseorda']
        c1s.MMSEORLO = record['c1s_1b2_mmseorlo']
        c1s.PENTAGON = record['c1s_1c_pentagon']
        c1s.MMSE = record['c1s_1d_mmse']
        c1s.NPSYCLOC = record['c1s_2_npsycloc']
        c1s.NPSYLAN = record['c1s_2a_npsylan']
        c1s.NPSYLANX = record['c1s_2a1_npsylanx']
        c1s.LOGIMO = record['c1s_3amo_logimo']
        c1s.LOGIDAY = record['c1s_3ady_logiday']
        c1s.LOGIYR = record['c1s_3ayr_logiyr']
        c1s.LOGIPREV = record['c1s_3a1_logiprev']
        c1s.LOGIMEM = record['c1s_3b_logimem']
        c1s.DIGIF = record['c1s_4a_digif']
        c1s.DIGIFLEN = record['c1s_4b_digiflen']
        c1s.DIGIB = record['c1s_5a_digib']
        c1s.DIGIBLEN = record['c1s_5b_digiblen']
        c1s.ANIMALS = record['c1s_6a_animals']
        c1s.VEG = record['c1s_6b_veg']
        c1s.TRAILA = record['c1s_7a_traila']
        c1s.TRAILARR = record['c1s_7a1_trailarr']
        c1s.TRAILALI = record['c1s_7a2_trailali']
        c1s.TRAILB = record['c1s_7b_trailb']
        c1s.TRAILBRR = record['c1s_7b1_trailbrr']
        c1s.TRAILBLI = record['c1s_7b2_trailbli']
        c1s.WAIS = record['c1s_8a_wais']
        c1s.MEMUNITS = record['c1s_9a_memunits']
        c1s.MEMTIME = record['c1s_9b_memtime']
        c1s.BOSTON = record['c1s_10a_boston']
        c1s.COGSTAT = record['c1s_11a_cogstat'] #check for blank
        packet.append(c1s)


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
