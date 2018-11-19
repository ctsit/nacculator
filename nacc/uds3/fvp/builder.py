###############################################################################
# Copyright 2015-2016 University of Florida. All rights reserved.
# This file is part of UF CTS-IT's NACCulator project.
# Use of this source code is governed by the license found in the LICENSE file.
###############################################################################

from nacc.uds3 import blanks
import forms as fvp_forms
from nacc.uds3 import packet as fvp_packet

def build_uds3_fvp_form(record):
    """ Converts REDCap CSV data into a packet (list of FVP Form objects) """
    packet = fvp_packet.Packet()
    
    #Set up the forms.
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

    # Among C1S and C2 forms, one must be filled, one must be empty. After 2017/10/23, must be C2
    post_c2 = False
    if (int(record['visityr'])>2017) or \
       (int(record['visityr'])==2017 and int(record['visitmo'])>10) or \
       (int(record['visityr'])==2017 and int(record['visitmo'])==10 and
            int(record['visitday'])>=23):
        post_c2 = True

    if post_c2:
        if(len(record['c1s_1a_mmseloc'].strip())==0 or len(record['c1s_11a_cogstat'].strip())==0):
            ptid = record['ptid']
            message = "Could not parse packet as C2 form is missing data"
            message = message + " for PTID : " + ("unknown" if not ptid else ptid)
            raise Exception(message)
        else:
            addC2(record, packet)
    else:
        if(len(record['mocacomp'].strip())==0 or len(record['cogstat_c2'].strip())==0):
            ptid = record['ptid']
            message = "Could not parse packet as C1S form is missing data"
            message = message + " for PTID : " + ("unknown" if not ptid else ptid)
            raise Exception(message)
        else:
            addC1S(record, packet)

    if len(record['eng_preferred_language'].strip()) != 0:
        addCLS(record, packet)

        if ['fu_clslang'] == 1:    # CLS lang completed
            if len(record['eng_percentage_spanish'].strip()) == 0:
                pct_spn = 0
            else:
                pct_spn = int(record['eng_percentage_spanish'])

            if len(record['eng_percentage_english'].strip()) == 0:
                pct_eng = 0
            else:
                pct_eng = int(record['eng_percentage_english'])

            post_cls = True
            if (record['visityr'] < '2017') or \
               (record['visityr'] == '2017' and int(record['visitmo']) < 6):
                post_cls = False

            bad_pct = False
            if (pct_eng + pct_spn)!=100:
                bad_pct = True

            if (post_cls and bad_pct):
                ptid = record['ptid']
                message = "Could not parse packet as language proficiency percentages do not equal 100"
                message = message + " for PTID : " + \
                    ("unknown" if not ptid else ptid)
                raise Exception(message)

            if not post_cls and (pct_spn != 0 or pct_eng != 0):
                ptid = record['ptid']
                message = "Could not parse packet as CLS forms should not be in packets from before June 1, 2017"
                message = message + " for PTID : " + \
                    ("unknown" if not ptid else ptid)
                raise Exception(message)

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

    post_Z1X = False
    if (int(record['visityr'])>2018) or \
       (int(record['visityr'])==2018 and int(record['visitmo'])>4) or \
       (int(record['visityr'])==2018 and int(record['visitmo'])==4 and
            int(record['visitday'])>=2):
        post_Z1X = True

    if post_Z1X:
        if(len(record['a1lang'].strip())==0 or len(record['clssubmitted'].strip())==0):
            ptid = record['ptid']
            message = "Could not parse packet as Z1X form is missing data"
            message = message + " for PTID : " + ("unknown" if not ptid else ptid)
            raise Exception(message)
        else:
            addZ1X(record, packet)
    else:
        if(len(record['a2sub'].strip())==0 or len(record['b7sub'].strip())==0):
            ptid = record['ptid']
            message = "Could not parse packet as Z1 form is missing data"
            message = message + " for PTID : " + ("unknown" if not ptid else ptid)
            raise Exception(message)
        else:
            addZ1(record, packet)


    update_header(record, packet)
    return packet

def addCLS(record, packet):
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


def addZ1(record, packet):
    z1 = fvp_forms.FormZ1()
    z1.A2SUB     = record['fu_a2sub']
    z1.A2NOT     = record['fu_a2not']
    z1.A2COMM    = record['fu_a2comm']
    z1.A3SUB     = record['fu_a3sub']
    z1.A3NOT     = record['fu_a3not']
    z1.A3COMM    = record['fu_a3comm']
    z1.A4SUB     = record['fu_a4sub']
    z1.A4NOT     = record['fu_a4not']
    z1.A4COMM    = record['fu_a4comm']
    z1.B1SUB     = record['fu_b1sub']
    z1.B1NOT     = record['fu_b1not']
    z1.B1COMM    = record['fu_b1comm']
    z1.B5SUB     = record['fu_b5sub']
    z1.B5NOT     = record['fu_b5not']
    z1.B5COMM    = record['fu_b5comm']
    z1.B6SUB     = record['fu_b6sub']
    z1.B6NOT     = record['fu_b6not']
    z1.B6COMM    = record['fu_b6comm']
    z1.B7SUB     = record['fu_b7sub']
    z1.B7NOT     = record['fu_b7not']
    z1.B7COMM    = record['fu_b7comm']
    packet.insert(0,z1)


def addZ1X(record, packet):
    z1x = fvp_forms.FormZ1X()
    z1x.LANGA1 = record['fu_a1lang']
    z1x.LANGA2 = record['fu_a2lang']
    z1x.A2SUB = record['fu_a2sub_73fdc7']
    z1x.A2NOT = record['fu_a2not_fd65a7']
    z1x.LANGA3 = record['fu_a3lang']
    z1x.A3SUB = record['fu_a3sub_c2a68b']
    z1x.A3NOT = record['fu_a3not_f7c411']
    z1x.LANGA4 = record['fu_a4lang']
    z1x.A4SUB = record['fu_a4sub_143f22']
    z1x.A4NOT = record['fu_a4not_b95e64']
    z1x.LANGB1 = record['fu_b1lang']
    z1x.B1SUB = record['fu_b1sub_c03500']
    z1x.B1NOT = record['fu_b1not_0a7e9f']
    z1x.LANGB4 = record['fu_b4lang']
    z1x.LANGB5 = record['fu_b5lang']
    z1x.B5SUB = record['fu_b5sub_51a694']
    z1x.B5NOT = record['b5not_fvpz1x']
    z1x.LANGB6 = record['fu_b6lang']
    z1x.B6SUB = record['fu_b6sub_db439d']
    z1x.B6NOT = record['fu_b6not_310244']
    z1x.LANGB7 = record['fu_b7lang']
    z1x.B7SUB = record['fu_b7sub_21a95f']
    z1x.B7NOT = record['fu_b7not_dccb30']
    z1x.LANGB8 = record['fu_b8lang']
    z1x.LANGB9 = record['fu_b9lang']
    z1x.LANGC2 = record['fu_c2lang']
    z1x.LANGD1 = record['fu_d1lang']
    z1x.LANGD2 = record['fu_d2lang']
    z1x.LANGA3A = record['fu_a3alang']
    z1x.FTDA3AFS = record['fu_a3asubmitted']
    z1x.FTDA3AFR = record['fu_a3anot']
    z1x.LANGB3F = record['fu_b3flang']
    z1x.LANGB9F = record['fu_b9flang']
    z1x.LANGC1F = record['fu_c1flang']
    z1x.LANGC2F = record['fu_c2flang']
    z1x.LANGC3F = record['fu_c3flang']
    z1x.LANGC4F = record['fu_c4flang']
    z1x.FTDC4FS = record['fu_c4fsubmitted']
    z1x.FTDC4FR = record['fu_c4fnot']
    z1x.FTDC5FS = record['fu_c5fsubmitted']
    z1x.FTDC5FR = record['fu_c5fnot']
    z1x.FTDC6FS = record['fu_c6fsubmitted']
    z1x.FTDC6FR = record['fu_c6fnot']
    z1x.LANGE2F = record['fu_e2flang']
    z1x.LANGE3F = record['fu_e3flang']
    z1x.LANGCLS = record['fu_clslang']
    z1x.CLSSUB  = record['fu_clssubmitted']
    packet.insert(0, z1x)


def addC1S(record, packet):
    c1s = ivp_forms.FormC1S()
    c1s.MMSELOC = record['c1s_1a_mmseloc']
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
    c1s.COGSTAT = record['c1s_11a_cogstat']
    packet.append(c1s)

def addC2(record, packet):
    c2 = fvp_forms.FormC2()
    c2.MOCACOMP  = record['fu_mocacomp']
    c2.MOCAREAS  = record['fu_mocareas']
    c2.MOCALOC   = record['fu_mocaloc']
    c2.MOCALAN   = record['fu_mocalan']
    c2.MOCALANX  = record['fu_mocalanx']
    c2.MOCAVIS   = record['fu_mocavis']
    c2.MOCAHEAR  = record['fu_mocahear']
    c2.MOCATOTS  = record['fu_mocatots']
    c2.MOCATRAI  = record['fu_mocatrai']
    c2.MOCACUBE  = record['fu_mocacube']
    c2.MOCACLOC  = record['fu_mocacloc']
    c2.MOCACLON  = record['fu_mocaclon']
    c2.MOCACLOH  = record['fu_mocacloh']
    c2.MOCANAMI  = record['fu_mocanami']
    c2.MOCAREGI  = record['fu_mocaregi']
    c2.MOCADIGI  = record['fu_mocadigi']
    c2.MOCALETT  = record['fu_mocalett']
    c2.MOCASER7  = record['fu_mocaser7']
    c2.MOCAREPE  = record['fu_mocarepe']
    c2.MOCAFLUE  = record['fu_mocaflue']
    c2.MOCAABST  = record['fu_mocaabst']
    c2.MOCARECN  = record['fu_mocarecn']
    c2.MOCARECC  = record['fu_mocarecc']
    c2.MOCARECR  = record['fu_mocarecr']
    c2.MOCAORDT  = record['fu_mocaordt']
    c2.MOCAORMO  = record['fu_mocaormo']
    c2.MOCAORYR  = record['fu_mocaoryr']
    c2.MOCAORDY  = record['fu_mocaordy']
    c2.MOCAORPL  = record['fu_mocaorpl']
    c2.MOCAORCT  = record['fu_mocaorct']
    c2.NPSYCLOC  = record['fu_npsycloc_c2'] #TODO
    c2.NPSYLAN   = record['fu_npsylan_c2'] #TODO
    c2.NPSYLANX  = record['fu_npsylanx_c2'] #TODO
    c2.CRAFTVRS  = record['fu_craftvrs']
    c2.CRAFTURS  = record['fu_crafturs']
    c2.UDSBENTC  = record['fu_udsbentc']
    c2.DIGFORCT  = record['fu_digforct']
    c2.DIGFORSL  = record['fu_digforsl']
    c2.DIGBACCT  = record['fu_digbacct']
    c2.DIGBACLS  = record['fu_digbacls']
    c2.ANIMALS   = record['fu_animals_c2'] #TODO
    c2.VEG       = record['fu_veg_c2'] #TODO
    c2.TRAILA    = record['fu_traila_c2'] #TODO
    c2.TRAILARR  = record['fu_trailarr_c2'] #TODO
    c2.TRAILALI  = record['fu_trailali_c2'] #TODO
    c2.TRAILB    = record['fu_trailb_c2'] #TODO
    c2.TRAILBRR  = record['fu_trailbrr_c2'] #TODO
    c2.TRAILBLI  = record['fu_trailbli_c2'] #TODO
    c2.CRAFTDVR  = record['fu_craftdvr']
    c2.CRAFTDRE  = record['fu_craftdre']
    c2.CRAFTDTI  = record['fu_craftdti']
    c2.CRAFTCUE  = record['fu_craftcue']
    c2.UDSBENTD  = record['fu_udsbentd']
    c2.UDSBENRS  = record['fu_udsbenrs']
    c2.MINTTOTS  = record['fu_minttots']
    c2.MINTTOTW  = record['fu_minttotw']
    c2.MINTSCNG  = record['fu_mintscng']
    c2.MINTSCNC  = record['fu_mintscnc']
    c2.MINTPCNG  = record['fu_mintpcng']
    c2.MINTPCNC  = record['fu_mintpcnc']
    c2.UDSVERFC  = record['fu_udsverfc']
    c2.UDSVERFN  = record['fu_udsverfn']
    c2.UDSVERNF  = record['fu_udsvernf']
    c2.UDSVERLC  = record['fu_udsverlc']
    c2.UDSVERLR  = record['fu_udsverlr']
    c2.UDSVERLN  = record['fu_udsverln']
    c2.UDSVERTN  = record['fu_udsvertn']
    c2.UDSVERTE  = record['fu_udsverte']
    c2.UDSVERTI  = record['fu_udsverti']
    c2.COGSTAT   = record['fu_cogstat_c2'] #TODO
    packet.append(c2)

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
