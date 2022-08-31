###############################################################################
# Copyright 2015-2020 University of Florida. All rights reserved.
# This file is part of UF CTS-IT's NACCulator project.
# Use of this source code is governed by the license found in the LICENSE file.
###############################################################################

from nacc.lbd.v3_1.fvp import forms as lbd_short_fvp_forms
from nacc.uds3 import packet as lbd_short_fvp_packet


def build_lbd_short_fvp_form(record):
    ''' Converts REDCap CSV data into a packet (list of FVP Form objects) '''
    packet = lbd_short_fvp_packet.Packet()

    # Set up the forms..........

    # This form cannot precede June 1, 2017.
    if not (int(record['visityr']) > 2017) or \
            (int(record['visityr']) == 2017 and int(record['visitmo']) > 6) \
            or (int(record['visityr']) == 2017 and int(record['visitmo']) == 6
                and int(record['visitday']) >= 1):
        raise ValueError('Visit date cannot precede June 1, 2017.')

    add_z1x(record, packet)
    # Forms B1L, B3L, B4L, B5L, B7L, B9L, C1L, E1L, E2L, E3L, D1L are REQUIRED.
    # Forms B2L and B6L are OPTIONAL and must be specifically marked as present
    # for nacculator to process them
    add_b1l(record, packet)
    try:
        if record['fu_lbdb2ls'] == '1':
            add_b2l(record, packet)
    except KeyError:
        if record['fu_lbudspch'] is not None:
            add_b2l(record, packet)
    add_b3l(record, packet)
    add_b4l(record, packet)
    add_b5l(record, packet)
    try:
        if record['fu_lbdb6ls'] == '1':
            add_b6l(record, packet)
    except KeyError:
        if record['fu_lbspcgim'] is not None:
            add_b6l(record, packet)
    add_b7l(record, packet)
    add_b9l(record, packet)
    add_c1l(record, packet)
    add_d1l(record, packet)
    add_e1l(record, packet)
    add_e2l(record, packet)
    add_e3l(record, packet)
    update_header(record, packet)

    return packet


def add_z1x(record, packet):
    Z1X = lbd_short_fvp_forms.FormZ1X()
    Z1X.LANGA1   = record['fu_langa1']
    Z1X.LANGA2   = record['fu_langa2']
    Z1X.A2SUB    = record['fu_a2sub']
    Z1X.A2NOT    = record['fu_a2not']
    Z1X.LANGA3   = record['fu_langa3']
    Z1X.A3SUB    = record['fu_a3sub']
    Z1X.A3NOT    = record['fu_a3not']
    Z1X.LANGA4   = record['fu_langa4']
    Z1X.A4SUB    = record['fu_a4sub']
    Z1X.A4NOT    = record['fu_a4not']
    Z1X.LANGB1   = record['fu_langb1']
    Z1X.B1SUB    = record['fu_b1sub']
    Z1X.B1NOT    = record['fu_b1not']
    Z1X.LANGB4   = record['fu_langb4']
    Z1X.LANGB5   = record['fu_langb5']
    Z1X.B5SUB    = record['fu_b5sub']
    Z1X.B5NOT    = record['fu_b5not']
    Z1X.LANGB6   = record['fu_langb6']
    Z1X.B6SUB    = record['fu_b6sub']
    Z1X.B6NOT    = record['fu_b6not']
    Z1X.LANGB7   = record['fu_langb7']
    Z1X.B7SUB    = record['fu_b7sub']
    Z1X.B7NOT    = record['fu_b7not']
    Z1X.LANGB8   = record['fu_langb8']
    Z1X.LANGB9   = record['fu_langb9']
    Z1X.LANGC2   = record['fu_langc2']
    Z1X.LANGD1   = record['fu_langd1']
    Z1X.LANGD2   = record['fu_langd2']
    try:
        Z1X.LANGA3A  = record['fu_langa3a']
        Z1X.FTDA3AFS = record['fu_ftda3afs']
        Z1X.FTDA3AFR = record['fu_ftda3afr']
        Z1X.LANGB3F  = record['fu_langb3f']
        Z1X.LANGB9F  = record['fu_langb9f']
        Z1X.LANGC1F  = record['fu_langc1f']
        Z1X.LANGC2F  = record['fu_langc2f']
        Z1X.LANGC3F  = record['fu_langc3f']
        Z1X.LANGC4F  = record['fu_langc4f']
        Z1X.FTDC4FS  = record['fu_ftdc4fs']
        Z1X.FTDC4FR  = record['fu_ftdc4fr']
        Z1X.LANGC5F  = record['fu_langc5f']
        Z1X.FTDC5FS  = record['fu_ftdc5fs']
        Z1X.FTDC5FR  = record['fu_ftdc5fr']
        Z1X.LANGC6F  = record['fu_langc6f']
        Z1X.FTDC6FS  = record['fu_ftdc6fs']
        Z1X.FTDC6FR  = record['fu_ftdc6fr']
        Z1X.LANGE2F  = record['fu_lange2f']
        Z1X.LANGE3F  = record['fu_lange3f']
        Z1X.LANGCLS  = record['fu_langcls']
        Z1X.CLSSUB   = record['fu_clssub']
    except KeyError:
        Z1X.LANGA3A  = ''
        Z1X.FTDA3AFS = ''
        Z1X.FTDA3AFR = ''
        Z1X.LANGB3F  = ''
        Z1X.LANGB9F  = ''
        Z1X.LANGC1F  = ''
        Z1X.LANGC2F  = ''
        Z1X.LANGC3F  = ''
        Z1X.LANGC4F  = ''
        Z1X.FTDC4FS  = ''
        Z1X.FTDC4FR  = ''
        Z1X.LANGC5F  = ''
        Z1X.FTDC5FS  = ''
        Z1X.FTDC5FR  = ''
        Z1X.LANGC6F  = ''
        Z1X.FTDC6FS  = ''
        Z1X.FTDC6FR  = ''
        Z1X.LANGE2F  = ''
        Z1X.LANGE3F  = ''
        Z1X.LANGCLS  = ''
        Z1X.CLSSUB   = '0'
    # for REDCap projects that don't have the LBD questions added to their Z1X,
    # we just see if there's info in the B2L and B6L forms and fill in
    # accordingly.
    try:
        Z1X.B2LSUB  = record['fu_b2lsub']
        Z1X.B2LNOT  = record['fu_b2lnot']
        Z1X.B6LSUB  = record['fu_b6lsub']
        Z1X.B6LNOT  = record['fu_b6lnot']
    except KeyError:
        if record['fu_lbudspch'] is not None:
            Z1X.B2LSUB = '1'
            Z1X.B2LNOT = ''
        if record['fu_lbspcgim'] is not None:
            Z1X.B6LSUB = '1'
            Z1X.B6LNOT = ''
    packet.insert(0, Z1X)


def add_b1l(record, packet):
    B1L = lbd_short_fvp_forms.FormB1L()
    B1L.LBSSALIV = record['fu_LBSSALIV'.lower()]
    B1L.LBSSWALL = record['fu_lBSSWALL'.lower()]
    B1L.LBSSMeLL = record['fu_LBSSMeLL'.lower()]
    B1L.LBSSWeAt = record['fu_LBSSWeAT'.lower()]
    B1L.LBSCoNSt = record['fu_LBSCoNST'.lower()]
    B1L.LBSUBLAD = record['fu_LBSUBLAD'.lower()]
    B1L.LBSDZStU = record['fu_LBSDZStU'.lower()]
    B1L.LBSDZStN = record['fu_LBSDZStN'.lower()]
    B1L.LBSFAINt = record['fu_LBSFAINt'.lower()]
    B1L.LBPSyAGe = record['fu_LBPSyAGe'.lower()]
    B1L.LBSStNSy = record['fu_LBSStNSy'.lower()]
    B1L.LBSITSy = record['fu_LBSITSy'.lower()]
    B1L.LBSStNDI = record['fu_LBSStNDI'.lower()]
    B1L.LBSITDI = record['fu_LBSITDI'.lower()]
    B1L.LBSStNHt = record['fu_LBSStNHt'.lower()]
    B1L.LBSITHR = record['fu_LBSITHR'.lower()]
    B1L.LBSAGerM = record['fu_LBSAGerM'.lower()]
    B1L.LBSAGeSM = record['fu_LBSAGeSM'.lower()]
    B1L.LBSAGeGt = record['fu_LBSAGeGt'.lower()]
    B1L.LBSAGeFL = record['fu_LBSAGeFL'.lower()]
    B1L.LBSAGetr = record['fu_LBSAGetr'.lower()]
    B1L.LBSAGeBr = record['fu_LBSAGeBr'.lower()]
    packet.append(B1L)


def add_b2l(record,packet):
    B2L = lbd_short_fvp_forms.FormB2L()
    B2L.LBUDSPCH = record['fu_LBUDSPCH'.lower()]
    B2L.LBUDSALV = record['fu_LBUDSALV'.lower()]
    B2L.LBUDSWAL = record['fu_LBUDSWAL'.lower()]
    B2L.LBUWrIte = record['fu_LBUWrIte'.lower()]
    B2L.LBUDFooD = record['fu_LBUDFooD'.lower()]
    B2L.LBUDreSS = record['fu_LBUDreSS'.lower()]
    B2L.LBUDHyGN = record['fu_LBUDHyGN'.lower()]
    B2L.LBUDtUrN = record['fu_LBUDtUrN'.lower()]
    B2L.LBUDFALL = record['fu_LBUDFALL'.lower()]
    B2L.LBUDFrZ  = record['fu_LBUDFrZ'.lower()]
    B2L.LBUDWALK = record['fu_LBUDWALK'.lower()]
    B2L.LBUDtreM = record['fu_LBUDtreM'.lower()]
    B2L.LBUDSeNS = record['fu_LBUDSeNS'.lower()]
    packet.append(B2L)


def add_b3l(record,packet):
    B3L = lbd_short_fvp_forms.FormB3L()
    B3L.LBUMSPCH = record['fu_LBUMSPCH'.lower()]
    B3L.LBUMSPCX = record['fu_LBUMSPCX'.lower()]
    B3L.LBUMFACe = record['fu_LBUMFACe'.lower()]
    B3L.LBUMFACX = record['fu_LBUMFACX'.lower()]
    B3L.LBUMtrFA = record['fu_LBUMtrFA'.lower()]
    B3L.LBUtrFAX = record['fu_LBUtrFAX'.lower()]
    B3L.LBUMtrrH = record['fu_LBUMtrrH'.lower()]
    B3L.LBUtrrHX = record['fu_LBUtrrHX'.lower()]
    B3L.LBUMtrLH = record['fu_LBUMtrLH'.lower()]
    B3L.LBUtrLHX = record['fu_LBUtrLHX'.lower()]
    B3L.LBUMtrrF = record['fu_LBUMtrrF'.lower()]
    B3L.LBUtrrFX = record['fu_LBUtrrFX'.lower()]
    B3L.LBUMtrLF = record['fu_LBUMtrLF'.lower()]
    B3L.LBUtrLFX = record['fu_LBUtrLFX'.lower()]
    B3L.LBUMAtrH = record['fu_LBUMAtrH'.lower()]
    B3L.LBUAtrHX = record['fu_LBUAtrHX'.lower()]
    B3L.LBUMAtLH = record['fu_LBUMAtLH'.lower()]
    B3L.LBUAtLHX = record['fu_LBUAtLHX'.lower()]
    B3L.LBUMrGNK = record['fu_LBUMrGNK'.lower()]
    B3L.LBUrGNKX = record['fu_LBUrGNKX'.lower()]
    B3L.LBUMrGrU = record['fu_LBUMrGrU'.lower()]
    B3L.LBUrGrUX = record['fu_LBUrGrUX'.lower()]
    B3L.LBUMrGLU = record['fu_LBUMrGLU'.lower()]
    B3L.LBUrGLUX = record['fu_LBUrGLUX'.lower()]
    B3L.LBUMrGrL = record['fu_LBUMrGrL'.lower()]
    B3L.LBUrGrLX = record['fu_LBUrGrLX'.lower()]
    B3L.LBUMrGLL = record['fu_LBUMrGLL'.lower()]
    B3L.LBUrGLLX = record['fu_LBUrGLLX'.lower()]
    B3L.LBUMFtrH = record['fu_LBUMFtrH'.lower()]
    B3L.LBUFtrHX = record['fu_LBUFtrHX'.lower()]
    B3L.LBUMFtLH = record['fu_LBUMFtLH'.lower()]
    B3L.LBUFtLHX = record['fu_LBUFtLHX'.lower()]
    B3L.LBUMHMrH = record['fu_LBUMHMrH'.lower()]
    B3L.LBUHMrHX = record['fu_LBUHMrHX'.lower()]
    B3L.LBUMHMLH = record['fu_LBUMHMLH'.lower()]
    B3L.LBUHMLHX = record['fu_LBUHMLHX'.lower()]
    B3L.LBUMPSrH = record['fu_LBUMPSrH'.lower()]
    B3L.LBUPSrHX = record['fu_LBUPSrHX'.lower()]
    B3L.LBUMPSLH = record['fu_LBUMPSLH'.lower()]
    B3L.LBUPSLHX = record['fu_LBUPSLHX'.lower()]
    B3L.LBUMLGrL = record['fu_LBUMLGrL'.lower()]
    B3L.LBULGrLX = record['fu_LBULGrLX'.lower()]
    B3L.LBUMLGLL = record['fu_LBUMLGLL'.lower()]
    B3L.LBULGLLX = record['fu_LBULGLLX'.lower()]
    B3L.LBUMrISe = record['fu_LBUMrISe'.lower()]
    B3L.LBUMrISX = record['fu_LBUMrISX'.lower()]
    B3L.LBUMPoSt = record['fu_LBUMPoSt'.lower()]
    B3L.LBUMPoSX = record['fu_LBUMPoSX'.lower()]
    B3L.LBUMGAIt = record['fu_LBUMGAIt'.lower()]
    B3L.LBUMGAIX = record['fu_LBUMGAIX'.lower()]
    B3L.LBUPStBL = record['fu_LBUPStBL'.lower()]
    B3L.LBUPStBX = record['fu_LBUPStBX'.lower()]
    B3L.LBUMBrAD = record['fu_LBUMBrAD'.lower()]
    B3L.LBUMBrAX = record['fu_LBUMBrAX'.lower()]
    B3L.LBUMHNyr = record['fu_LBUMHNyr'.lower()]
    B3L.LBUMHNyX = record['fu_LBUMHNyX'.lower()]
    packet.append(B3L)


def add_b4l(record,packet):
    B4L = lbd_short_fvp_forms.FormB4L()
    B4L.LBDeLUS  = record['fu_LBDeLUS'.lower()]
    B4L.LBDHUrt  = record['fu_LBDHUrt'.lower()]
    B4L.LBDSteAL = record['fu_LBDSteAL'.lower()]
    B4L.LBDAFFr  = record['fu_LBDAFFr'.lower()]
    B4L.LBDGUeSt = record['fu_LBDGUeSt'.lower()]
    B4L.LBDIMPoS = record['fu_LBDIMPoS'.lower()]
    B4L.LBDHoMe  = record['fu_LBDHoMe'.lower()]
    B4L.LBDABAND = record['fu_LBDABAND'.lower()]
    B4L.LBDPreS  = record['fu_LBDPreS'.lower()]
    B4L.LBDotHer = record['fu_LBDotHer'.lower()]
    B4L.LBHALL   = record['fu_LBHALL'.lower()]
    B4L.LBHVoICe = record['fu_LBHVoICe'.lower()]
    B4L.LBHPeoPL = record['fu_LBHPeoPL'.lower()]
    B4L.LBHNotPr = record['fu_LBHNotPr'.lower()]
    B4L.LBHoDor  = record['fu_LBHoDor'.lower()]
    B4L.LBHFeeL  = record['fu_LBHFeeL'.lower()]
    B4L.LBHtASte = record['fu_LBHtASte'.lower()]
    B4L.LBHotSeN = record['fu_LBHotSeN'.lower()]
    B4L.LBANXIet = record['fu_LBANXIet'.lower()]
    B4L.LBANeVNt = record['fu_LBANeVNt'.lower()]
    B4L.LBANreLX = record['fu_LBANreLX'.lower()]
    B4L.LBANBrtH = record['fu_LBANBrtH'.lower()]
    B4L.LBANBUtt = record['fu_LBANBUtt'.lower()]
    B4L.LBANPLAC = record['fu_LBANPLAC'.lower()]
    B4L.LBANSePr = record['fu_LBANSePr'.lower()]
    B4L.LBANotHr = record['fu_LBANotHr'.lower()]
    B4L.LBAPAtHy = record['fu_LBAPAtHy'.lower()]
    B4L.LBAPSPNt = record['fu_LBAPSPNt'.lower()]
    B4L.LBAPCoNV = record['fu_LBAPCoNV'.lower()]
    B4L.LBAPAFF  = record['fu_LBAPAFF'.lower()]
    B4L.LBAPCHor = record['fu_LBAPCHor'.lower()]
    B4L.LBAPINt  = record['fu_LBAPINt'.lower()]
    B4L.LBAPFAML = record['fu_LBAPFAML'.lower()]
    B4L.LBAPINtr = record['fu_LBAPINtr'.lower()]
    B4L.LBAPotH  = record['fu_LBAPotH'.lower()]
    packet.append(B4L)


def add_b5l(record,packet):
    B5L = lbd_short_fvp_forms.FormB5L()
    B5L.LBMLtHrG = record['fu_LBMLtHrG'.lower()]
    B5L.LBMSLeeP = record['fu_LBMSLeeP'.lower()]
    B5L.LBMDISrG = record['fu_LBMDISrG'.lower()]
    B5L.LBMStAre = record['fu_LBMStAre'.lower()]
    packet.append(B5L)


def add_b6l(record,packet):
    B6L = lbd_short_fvp_forms.FormB6L()
    B6L.LBSPCGIM = record['fu_LBSPCGIM'.lower()]
    B6L.LBSPDrM  = record['fu_LBSPDrM'.lower()]
    B6L.LBSPyrS  = record['fu_LBSPyrS'.lower()]
    B6L.LBSPMoS  = record['fu_LBSPMoS'.lower()]
    B6L.LBSPINJS = record['fu_LBSPINJS'.lower()]
    B6L.LBSPINJP = record['fu_LBSPINJP'.lower()]
    B6L.LBSPCHAS = record['fu_LBSPCHAS'.lower()]
    B6L.LBSPMoVe = record['fu_LBSPMoVe'.lower()]
    B6L.LBSPLeGS = record['fu_LBSPLeGS'.lower()]
    B6L.LBSPNerV = record['fu_LBSPNerv'.lower()]
    B6L.LBSPUrGL = record['fu_LBSPUrGL'.lower()]
    B6L.LBSPSeNS = record['fu_LBSPSeNS'.lower()]
    B6L.LBSPWorS = record['fu_LBSPWorS'.lower()]
    B6L.LBSPWALK = record['fu_LBSPWALK'.lower()]
    B6L.LBSPAWAK = record['fu_LBSPAWAK'.lower()]
    B6L.LBSPBrtH = record['fu_LBSPBrtH'.lower()]
    B6L.LBSPtrt  = record['fu_LBSPtrt'.lower()]
    B6L.LBSPCrMP = record['fu_LBSPCrMP'.lower()]
    B6L.LBSPALrt = record['fu_LBSPALrt'.lower()]
    packet.append(B6L)


def add_b7l(record,packet):
    B7L = lbd_short_fvp_forms.FormB7L()
    B7L.LBSCLIV  = record['fu_LBSCLIV'.lower()]
    B7L.LBSCSLP  = record['fu_LBSCSLP'.lower()]
    B7L.LBSCBeHV = record['fu_LBSCBeHV'.lower()]
    B7L.LBSCDrM  = record['fu_LBSCDrM'.lower()]
    B7L.LBSCyrS  = record['fu_LBSCyrS'.lower()]
    B7L.LBSCMoS  = record['fu_LBSCMoS'.lower()]
    B7L.LBSCINJS = record['fu_LBSCINJS'.lower()]
    B7L.LBSCINJP = record['fu_LBSCINJP'.lower()]
    B7L.LBSCCHAS = record['fu_LBSCCHAS'.lower()]
    B7L.LBSCMoVe = record['fu_LBSCMoVe'.lower()]
    B7L.LBSCLeGS = record['fu_LBSCLeGS'.lower()]
    B7L.LBSCNerV = record['fu_LBSCNerV'.lower()]
    B7L.LBSCSeNS = record['fu_LBSCSeNS'.lower()]
    B7L.LBSCWorS = record['fu_LBSCWorS'.lower()]
    B7L.LBSCWALK = record['fu_LBSCWALK'.lower()]
    B7L.LBSCAWAK = record['fu_LBSCAWAK'.lower()]
    B7L.LBSCBrtH = record['fu_LBSCBrtH'.lower()]
    B7L.LBSCtrt  = record['fu_LBSCtrt'.lower()]
    B7L.LBSCCrMP = record['fu_LBSCCrMP'.lower()]
    B7L.LBSCALrt = record['fu_LBSCALrt'.lower()]
    packet.append(B7L)


def add_b9l(record,packet):
    B9L = lbd_short_fvp_forms.FormB9L()
    B9L.CoNSFALL = record['fu_CoNSFALL'.lower()]
    B9L.CoNSWKoF = record['fu_CoNSWKoF'.lower()]
    B9L.CoNSLyAW = record['fu_CoNSLyAW'.lower()]
    B9L.CoNSWKer = record['fu_CoNSWKer'.lower()]
    B9L.CoNSLttL = record['fu_CoNSLttL'.lower()]
    B9L.SCCorAte = record['fu_SCCorAte'.lower()]
    B9L.CoDSUNeX = record['fu_CoDSUNeX'.lower()]
    B9L.CoDSSItP = record['fu_CoDSSItP'.lower()]
    B9L.CoDSWAtV = record['fu_CoDSWAtV'.lower()]
    B9L.CoDStALK = record['fu_CoDStALK'.lower()]
    B9L.CoDSAWDy = record['fu_CoDSAWDy'.lower()]
    B9L.CoDSFLDy = record['fu_CoDSFLDy'.lower()]
    packet.append(B9L)


def add_c1l(record,packet):
    C1L = lbd_short_fvp_forms.FormC1L()
    C1L.LBNPFACe = record['fu_LBNPFACe'.lower()]
    C1L.LBNPNoIS = record['fu_LBNPNoIS'.lower()]
    C1L.LBNPtCor = record['fu_LBNPtCor'.lower()]
    C1L.LBNPPArD = record['fu_LBNPPArD'.lower()]
    packet.append(C1L)


def add_d1l(record,packet):
    D1L = lbd_short_fvp_forms.FormD1L()
    D1L.LBCDSCoG = record['fu_LBCDSCoG'.lower()]
    D1L.LBCCMeM  = record['fu_LBCCMeM'.lower()]
    D1L.LBCCLANG = record['fu_LBCCLANG'.lower()]
    D1L.LBCCAtt  = record['fu_LBCCAtt'.lower()]
    D1L.LBCCeXDe = record['fu_LBCCeXDe'.lower()]
    D1L.LBCCVIS  = record['fu_LBCCVIS'.lower()]
    D1L.LBCDSMoV = record['fu_LBCDSMoV'.lower()]
    D1L.LBCMBrAD = record['fu_LBCMBrAD'.lower()]
    D1L.LBCMrIGD = record['fu_LBCMrIGD'.lower()]
    D1L.LBCMrtrM = record['fu_LBCMrtrM'.lower()]
    D1L.LBCMPtrM = record['fu_LBCMPtrM'.lower()]
    D1L.LBCMAtrM = record['fu_LBCMAtrM'.lower()]
    D1L.LBCMMyoC = record['fu_LBCMMyoC'.lower()]
    D1L.LBCMGAIt = record['fu_LBCMGAIt'.lower()]
    D1L.LBCMPINS = record['fu_LBCMPINS'.lower()]
    D1L.LBCDSBeV = record['fu_LBCDSBeV'.lower()]
    D1L.LBCBDeP  = record['fu_LBCBDeP'.lower()]
    D1L.LBCBAPA  = record['fu_LBCBAPA'.lower()]
    D1L.LBCBANX  = record['fu_LBCBANX'.lower()]
    D1L.LBCBHALL = record['fu_LBCBHALL'.lower()]
    D1L.LBCBDeL  = record['fu_LBCBDeL'.lower()]
    D1L.LBCDSAUt = record['fu_LBCDSAUt'.lower()]
    D1L.LBCAreM  = record['fu_LBCAreM'.lower()]
    D1L.LBCAAPN  = record['fu_LBCAAPN'.lower()]
    D1L.LBCALGSL = record['fu_LBCALGSL'.lower()]
    D1L.LBCArSLe = record['fu_LBCArSLe'.lower()]
    D1L.LBCADtSL = record['fu_LBCADtSL'.lower()]
    D1L.LBCACGFL = record['fu_LBCACGFL'.lower()]
    D1L.LBCAHyPt = record['fu_LBCAHyPt'.lower()]
    D1L.LBCACoNS = record['fu_LBCACoNS'.lower()]
    D1L.LBCAHyPS = record['fu_LBCAHyPS'.lower()]
    D1L.LBCAFALL = record['fu_LBCAFALL'.lower()]
    D1L.LBCASyNC = record['fu_LBCASyNC'.lower()]
    D1L.LBCASNAP = record['fu_LBCASNAP'.lower()]
    D1L.LBCoGSt  = record['fu_LBCoGSt'.lower()]
    D1L.LBCoGDX  = record['fu_LBCoGDX'.lower()]
    packet.append(D1L)


def add_e1l(record,packet):
    E1L = lbd_short_fvp_forms.FormE1L()
    E1L.LBGNeWGN = record['fu_LBGNeWGN'.lower()]
    E1L.LBGLrrK2 = record['fu_LBGLrrK2'.lower()]
    E1L.LBGLrKiS = record['fu_LBGLrKiS'.lower()]
    E1L.LBGPArK2 = record['fu_LBGPArK2'.lower()]
    E1L.LBGPK2iS = record['fu_LBGPK2iS'.lower()]
    E1L.LBGPArK7 = record['fu_LBGPArK7'.lower()]
    E1L.LBGPK7iS = record['fu_LBGPK7iS'.lower()]
    E1L.LBGPiNK1 = record['fu_LBGPiNK1'.lower()]
    E1L.LBGPNKiS = record['fu_LBGPNKiS'.lower()]
    E1L.LBGSNCA  = record['fu_LBGSNCA'.lower()]
    E1L.LBGSNCiS = record['fu_LBGSNCiS'.lower()]
    E1L.LBGGBA   = record['fu_LBGGBA'.lower()]
    E1L.LBGGBAiS = record['fu_LBGGBAiS'.lower()]
    E1L.LBGotHr  = record['fu_LBGotHr'.lower()]
    E1L.LBGotHiS = record['fu_LBGotHiS'.lower()]
    E1L.LBGotHX  = record['fu_LBGotHX'.lower()]
    packet.append(E1L)


def add_e2l(record,packet):
    E2L = lbd_short_fvp_forms.FormE2L()
    E2L.LBISMrI  = record['fu_LBISMrI'.lower()]
    E2L.LBISMHIP = record['fu_LBISMHIP'.lower()]
    E2L.LBISMAVL = record['fu_LBISMAVL'.lower()]
    E2L.LBIFPet  = record['fu_LBIFPet'.lower()]
    E2L.LBIFPoCC = record['fu_LBIFPoCC'.lower()]
    E2L.LBIFPtPP = record['fu_LBIFPtPP'.lower()]
    E2L.LBIFPISL = record['fu_LBIFPISL'.lower()]
    E2L.LBIFPAVL = record['fu_LBIFPAVL'.lower()]
    E2L.LBIAPet  = record['fu_LBIAPet'.lower()]
    E2L.LBIAPAVL = record['fu_LBIAPAVL'.lower()]
    E2L.LBItPet  = record['fu_LBItPet'.lower()]
    E2L.LBItPAVL = record['fu_LBItPAVL'.lower()]
    E2L.LBIDAtS  = record['fu_LBIDAtS'.lower()]
    E2L.LBIDSABN = record['fu_LBIDSABN'.lower()]
    packet.append(E2L)


def add_e3l(record,packet):
    E3L = lbd_short_fvp_forms.FormE3L()
    E3L.LBoPoLyS = record['fu_LBoPoLyS'.lower()]
    E3L.LBoPoPoS = record['fu_LBoPoPoS'.lower()]
    E3L.LBoPoAVL = record['fu_LBoPoAVL'.lower()]
    E3L.LBoCMIBG = record['fu_LBoCMIBG'.lower()]
    E3L.LBoCMPoS = record['fu_LBoCMPoS'.lower()]
    E3L.LBoCMAVL = record['fu_LBoCMAVL'.lower()]
    E3L.LBoANoS  = record['fu_LBoANoS'.lower()]
    E3L.LBoANPoS = record['fu_LBoANPoS'.lower()]
    E3L.LBoANAVL = record['fu_LBoANAVL'.lower()]
    E3L.LBoANVer = record['fu_LBoANVer'.lower()]
    E3L.LBoANotH = record['fu_LBoANotH'.lower()]
    E3L.LBoCGAIt = record['fu_LBoCGAIt'.lower()]
    E3L.LBoCGPoS = record['fu_LBoCGPoS'.lower()]
    E3L.LBoCGAVL = record['fu_LBoCGAVL'.lower()]
    packet.append(E3L)

    update_header(record, packet)
    return packet


def update_header(record, packet):
    for header in packet:
        if header.form_name == "Z1X":
            header.PACKET = "F"
            header.FORMID = header.form_name
            header.FORMVER = 3
        else:
            header.PACKET = "FL"
            header.FORMID = header.form_name
            header.FORMVER = 3.1
        header.ADCID = record['adcid']
        header.PTID = record['ptid']
        header.VISITMO = record['visitmo']
        header.VISITDAY = record['visitday']
        header.VISITYR = record['visityr']
        header.VISITNUM = record['visitnum']
        header.INITIALS = record['initials']
