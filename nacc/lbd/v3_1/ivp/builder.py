###############################################################################
# Copyright 2015-2020 University of Florida. All rights reserved.
# This file is part of UF CTS-IT's NACCulator project.
# Use of this source code is governed by the license found in the LICENSE file.
###############################################################################

from nacc.lbd.v3_1.ivp import forms as lbd_short_ivp_forms
from nacc.uds3 import packet as lbd_short_ivp_packet


def build_lbd_short_ivp_form(record):
    ''' Converts REDCap CSV data into a packet (list of IVP Form objects) '''
    packet = lbd_short_ivp_packet.Packet()

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
        if record['lbdb2ls'] == '1':
            add_b2l(record, packet)
    except KeyError:
        if record['lbudspch'] is not None:
            add_b2l(record, packet)
    add_b3l(record, packet)
    add_b4l(record, packet)
    add_b5l(record, packet)
    try:
        if record['lbdb6ls'] == '1':
            add_b6l(record, packet)
    except KeyError:
        if record['lbspcgim'] is not None:
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
    Z1X = lbd_short_ivp_forms.FormZ1X()
    Z1X.LANGA1   = record['langa1']
    Z1X.LANGA2   = record['langa2']
    Z1X.A2SUB    = record['a2sub']
    Z1X.A2NOT    = record['a2not']
    Z1X.LANGA3   = record['langa3']
    Z1X.A3SUB    = record['a3sub']
    Z1X.A3NOT    = record['a3not']
    Z1X.LANGA4   = record['langa4']
    Z1X.A4SUB    = record['a4sub']
    Z1X.A4NOT    = record['a4not']
    Z1X.LANGA5   = record['langa5']
    Z1X.LANGB1   = record['langb1']
    Z1X.B1SUB    = record['b1sub']
    Z1X.B1NOT    = record['b1not']
    Z1X.LANGB4   = record['langb4']
    Z1X.LANGB5   = record['langb5']
    Z1X.B5SUB    = record['b5sub']
    Z1X.B5NOT    = record['b5not']
    Z1X.LANGB6   = record['langb6']
    Z1X.B6SUB    = record['b6sub']
    Z1X.B6NOT    = record['b6not']
    Z1X.LANGB7   = record['langb7']
    Z1X.B7SUB    = record['b7sub']
    Z1X.B7NOT    = record['b7not']
    Z1X.LANGB8   = record['langb8']
    Z1X.LANGB9   = record['langb9']
    Z1X.LANGC2   = record['langc2']
    Z1X.LANGD1   = record['langd1']
    Z1X.LANGD2   = record['langd2']
    try:
        Z1X.LANGA3A  = record['langa3a']
        Z1X.FTDA3AFS = record['ftda3afs']
        Z1X.FTDA3AFR = record['ftda3afr']
        Z1X.LANGB3F  = record['langb3f']
        Z1X.LANGB9F  = record['langb9f']
        Z1X.LANGC1F  = record['langc1f']
        Z1X.LANGC2F  = record['langc2f']
        Z1X.LANGC3F  = record['langc3f']
        Z1X.LANGC4F  = record['langc4f']
        Z1X.FTDC4FS  = record['ftdc4fs']
        Z1X.FTDC4FR  = record['ftdc4fr']
        Z1X.LANGC5F  = record['langc5f']
        Z1X.FTDC5FS  = record['ftdc5fs']
        Z1X.FTDC5FR  = record['ftdc5fr']
        Z1X.LANGC6F  = record['langc6f']
        Z1X.FTDC6FS  = record['ftdc6fs']
        Z1X.FTDC6FR  = record['ftdc6fr']
        Z1X.LANGE2F  = record['lange2f']
        Z1X.LANGE3F  = record['lange3f']
        Z1X.LANGCLS  = record['langcls']
        Z1X.CLSSUB   = record['clssub']
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
        Z1X.B2LSUB  = record['b2lsub']
        Z1X.B2LNOT  = record['b2lnot']
        Z1X.B6LSUB  = record['b6lsub']
        Z1X.B6LNOT  = record['b6lnot']
    except KeyError:
        if record['lbudspch'] is not None:
            Z1X.B2LSUB = '1'
            Z1X.B2LNOT = ''
        if record['lbspcgim'] is not None:
            Z1X.B6LSUB = '1'
            Z1X.B6LNOT = ''
    packet.insert(0, Z1X)


def add_b1l(record,packet):
    B1L = lbd_short_ivp_forms.FormB1L()
    B1L.LBSSALIV = record['LBSSALIV'.lower()]
    B1L.LBSSWALL = record['LBSSWALL'.lower()]
    B1L.LBSSMeLL = record['LBSSMeLL'.lower()]
    B1L.LBSSWeAt = record['LBSSWeAT'.lower()]
    B1L.LBSCoNSt = record['LBSCoNSt'.lower()]
    B1L.LBSUBLAD = record['LBSUBLAD'.lower()]
    B1L.LBSDZStU = record['LBSDZStU'.lower()]
    B1L.LBSDZStN = record['LBSDZStN'.lower()]
    B1L.LBSFAINt = record['LBSFAINt'.lower()]
    B1L.LBPSyAGe = record['LBPSyAGe'.lower()]
    B1L.LBSStNSy = record['LBSStNSy'.lower()]
    B1L.LBSITSy = record['LBSITSy'.lower()]
    B1L.LBSStNDI = record['LBSStNDI'.lower()]
    B1L.LBSITDI = record['LBSITDI'.lower()]
    B1L.LBSStNHt = record['LBSStNHt'.lower()]
    B1L.LBSITHR = record['LBSITHR'.lower()]
    B1L.LBSAGerM = record['LBSAGerM'.lower()]
    B1L.LBSAGeSM = record['LBSAGeSM'.lower()]
    B1L.LBSAGeGt = record['LBSAGeGt'.lower()]
    B1L.LBSAGeFL = record['LBSAGeFL'.lower()]
    B1L.LBSAGetr = record['LBSAGetr'.lower()]
    B1L.LBSAGeBr = record['LBSAGeBr'.lower()]
    packet.append(B1L)


def add_b2l(record, packet):
    B2L = lbd_short_ivp_forms.FormB2L()
    B2L.LBUDSPCH = record['LBUDSPCH'.lower()]
    B2L.LBUDSALV = record['LBUDSALV'.lower()]
    B2L.LBUDSWAL = record['LBUDSWAL'.lower()]
    B2L.LBUWrIte = record['LBUWrIte'.lower()]
    B2L.LBUDFooD = record['LBUDFooD'.lower()]
    B2L.LBUDreSS = record['LBUDreSS'.lower()]
    B2L.LBUDHyGN = record['LBUDHyGN'.lower()]
    B2L.LBUDtUrN = record['LBUDtUrN'.lower()]
    B2L.LBUDFALL = record['LBUDFALL'.lower()]
    B2L.LBUDFrZ  = record['LBUDFrZ'.lower()]
    B2L.LBUDWALK = record['LBUDWALK'.lower()]
    B2L.LBUDtreM = record['LBUDtreM'.lower()]
    B2L.LBUDSeNS = record['LBUDSeNS'.lower()]
    packet.append(B2L)


def add_b3l(record, packet):
    B3L = lbd_short_ivp_forms.FormB3L()
    B3L.LBUMSPCH = record['LBUMSPCH'.lower()]
    B3L.LBUMSPCX = record['LBUMSPCX'.lower()]
    B3L.LBUMFACe = record['LBUMFACe'.lower()]
    B3L.LBUMFACX = record['LBUMFACX'.lower()]
    B3L.LBUMtrFA = record['LBUMtrFA'.lower()]
    B3L.LBUtrFAX = record['LBUtrFAX'.lower()]
    B3L.LBUMtrrH = record['LBUMtrrH'.lower()]
    B3L.LBUtrrHX = record['LBUtrrHX'.lower()]
    B3L.LBUMtrLH = record['LBUMtrLH'.lower()]
    B3L.LBUtrLHX = record['LBUtrLHX'.lower()]
    B3L.LBUMtrrF = record['LBUMtrrF'.lower()]
    B3L.LBUtrrFX = record['LBUtrrFX'.lower()]
    B3L.LBUMtrLF = record['LBUMtrLF'.lower()]
    B3L.LBUtrLFX = record['LBUtrLFX'.lower()]
    B3L.LBUMAtrH = record['LBUMAtrH'.lower()]
    B3L.LBUAtrHX = record['LBUAtrHX'.lower()]
    B3L.LBUMAtLH = record['LBUMAtLH'.lower()]
    B3L.LBUAtLHX = record['LBUAtLHX'.lower()]
    B3L.LBUMrGNK = record['LBUMrGNK'.lower()]
    B3L.LBUrGNKX = record['LBUrGNKX'.lower()]
    B3L.LBUMrGrU = record['LBUMrGrU'.lower()]
    B3L.LBUrGrUX = record['LBUrGrUX'.lower()]
    B3L.LBUMrGLU = record['LBUMrGLU'.lower()]
    B3L.LBUrGLUX = record['LBUrGLUX'.lower()]
    B3L.LBUMrGrL = record['LBUMrGrL'.lower()]
    B3L.LBUrGrLX = record['LBUrGrLX'.lower()]
    B3L.LBUMrGLL = record['LBUMrGLL'.lower()]
    B3L.LBUrGLLX = record['LBUrGLLX'.lower()]
    B3L.LBUMFtrH = record['LBUMFtrH'.lower()]
    B3L.LBUFtrHX = record['LBUFtrHX'.lower()]
    B3L.LBUMFtLH = record['LBUMFtLH'.lower()]
    B3L.LBUFtLHX = record['LBUFtLHX'.lower()]
    B3L.LBUMHMrH = record['LBUMHMrH'.lower()]
    B3L.LBUHMrHX = record['LBUHMrHX'.lower()]
    B3L.LBUMHMLH = record['LBUMHMLH'.lower()]
    B3L.LBUHMLHX = record['LBUHMLHX'.lower()]
    B3L.LBUMPSrH = record['LBUMPSrH'.lower()]
    B3L.LBUPSrHX = record['LBUPSrHX'.lower()]
    B3L.LBUMPSLH = record['LBUMPSLH'.lower()]
    B3L.LBUPSLHX = record['LBUPSLHX'.lower()]
    B3L.LBUMLGrL = record['LBUMLGrL'.lower()]
    B3L.LBULGrLX = record['LBULGrLX'.lower()]
    B3L.LBUMLGLL = record['LBUMLGLL'.lower()]
    B3L.LBULGLLX = record['LBULGLLX'.lower()]
    B3L.LBUMrISe = record['LBUMrISe'.lower()]
    B3L.LBUMrISX = record['LBUMrISX'.lower()]
    B3L.LBUMPoSt = record['LBUMPoSt'.lower()]
    B3L.LBUMPoSX = record['LBUMPoSX'.lower()]
    B3L.LBUMGAIt = record['LBUMGAIt'.lower()]
    B3L.LBUMGAIX = record['LBUMGAIX'.lower()]
    B3L.LBUPStBL = record['LBUPStBL'.lower()]
    B3L.LBUPStBX = record['LBUPStBX'.lower()]
    B3L.LBUMBrAD = record['LBUMBrAD'.lower()]
    B3L.LBUMBrAX = record['LBUMBrAX'.lower()]
    B3L.LBUMHNyr = record['LBUMHNyr'.lower()]
    B3L.LBUMHNyX = record['LBUMHNyX'.lower()]
    packet.append(B3L)


def add_b4l(record, packet):
    B4L = lbd_short_ivp_forms.FormB4L()
    B4L.LBDeLUS  = record['LBDeLUS'.lower()]
    B4L.LBDHUrt  = record['LBDHUrt'.lower()]
    B4L.LBDSteAL = record['LBDSteAL'.lower()]
    B4L.LBDAFFr  = record['LBDAFFr'.lower()]
    B4L.LBDGUeSt = record['LBDGUeSt'.lower()]
    B4L.LBDIMPoS = record['LBDIMPoS'.lower()]
    B4L.LBDHoMe  = record['LBDHoMe'.lower()]
    B4L.LBDABAND = record['LBDABAND'.lower()]
    B4L.LBDPreS  = record['LBDPreS'.lower()]
    B4L.LBDotHer = record['LBDotHer'.lower()]
    B4L.LBHALL   = record['LBHALL'.lower()]
    B4L.LBHVoICe = record['LBHVoICe'.lower()]
    B4L.LBHPeoPL = record['LBHPeoPL'.lower()]
    B4L.LBHNotPr = record['LBHNotPr'.lower()]
    B4L.LBHoDor  = record['LBHoDor'.lower()]
    B4L.LBHFeeL  = record['LBHFeeL'.lower()]
    B4L.LBHtASte = record['LBHtASte'.lower()]
    B4L.LBHotSeN = record['LBHotSeN'.lower()]
    B4L.LBANXIet = record['LBANXIet'.lower()]
    B4L.LBANeVNt = record['LBANeVNt'.lower()]
    B4L.LBANreLX = record['LBANreLX'.lower()]
    B4L.LBANBrtH = record['LBANBrtH'.lower()]
    B4L.LBANBUtt = record['LBANBUtt'.lower()]
    B4L.LBANPLAC = record['LBANPLAC'.lower()]
    B4L.LBANSePr = record['LBANSePr'.lower()]
    B4L.LBANotHr = record['LBANotHr'.lower()]
    B4L.LBAPAtHy = record['LBAPAtHy'.lower()]
    B4L.LBAPSPNt = record['LBAPSPNt'.lower()]
    B4L.LBAPCoNV = record['LBAPCoNV'.lower()]
    B4L.LBAPAFF  = record['LBAPAFF'.lower()]
    B4L.LBAPCHor = record['LBAPCHor'.lower()]
    B4L.LBAPINt  = record['LBAPINt'.lower()]
    B4L.LBAPFAML = record['LBAPFAML'.lower()]
    B4L.LBAPINtr = record['LBAPINtr'.lower()]
    B4L.LBAPotH  = record['LBAPotH'.lower()]
    packet.append(B4L)


def add_b5l(record, packet):
    B5L = lbd_short_ivp_forms.FormB5L()
    B5L.LBMLtHrG = record['LBMLtHrG'.lower()]
    B5L.LBMSLeeP = record['LBMSLeeP'.lower()]
    B5L.LBMDISrG = record['LBMDISrG'.lower()]
    B5L.LBMStAre = record['LBMStAre'.lower()]
    packet.append(B5L)


def add_b6l(record, packet):
    B6L = lbd_short_ivp_forms.FormB6L()
    B6L.LBSPCGIM = record['LBSPCGIM'.lower()]
    B6L.LBSPDrM  = record['LBSPDrM'.lower()]
    B6L.LBSPyrS  = record['LBSPyrS'.lower()]
    B6L.LBSPMoS  = record['LBSPMoS'.lower()]
    B6L.LBSPINJS = record['LBSPINJS'.lower()]
    B6L.LBSPINJP = record['LBSPINJP'.lower()]
    B6L.LBSPCHAS = record['LBSPCHAS'.lower()]
    B6L.LBSPMoVe = record['LBSPMoVe'.lower()]
    B6L.LBSPLeGS = record['LBSPLeGS'.lower()]
    B6L.LBSPNerV = record['LBSPNerv'.lower()]
    B6L.LBSPUrGL = record['LBSPUrGL'.lower()]
    B6L.LBSPSeNS = record['LBSPSeNS'.lower()]
    B6L.LBSPWorS = record['LBSPWorS'.lower()]
    B6L.LBSPWALK = record['LBSPWALK'.lower()]
    B6L.LBSPAWAK = record['LBSPAWAK'.lower()]
    B6L.LBSPBrtH = record['LBSPBrtH'.lower()]
    B6L.LBSPtrt  = record['LBSPtrt'.lower()]
    B6L.LBSPCrMP = record['LBSPCrMP'.lower()]
    B6L.LBSPALrt = record['LBSPALrt'.lower()]
    packet.append(B6L)


def add_b7l(record, packet):
    B7L = lbd_short_ivp_forms.FormB7L()
    B7L.LBSCLIV  = record['LBSCLIV'.lower()]
    B7L.LBSCSLP  = record['LBSCSLP'.lower()]
    B7L.LBSCBeHV = record['LBSCBeHV'.lower()]
    B7L.LBSCDrM  = record['LBSCDrM'.lower()]
    B7L.LBSCyrS  = record['LBSCyrS'.lower()]
    B7L.LBSCMoS  = record['LBSCMoS'.lower()]
    B7L.LBSCINJS = record['LBSCINJS'.lower()]
    B7L.LBSCINJP = record['LBSCINJP'.lower()]
    B7L.LBSCCHAS = record['LBSCCHAS'.lower()]
    B7L.LBSCMoVe = record['LBSCMoVe'.lower()]
    B7L.LBSCLeGS = record['LBSCLeGS'.lower()]
    B7L.LBSCNerV = record['LBSCNerV'.lower()]
    B7L.LBSCSeNS = record['LBSCSeNS'.lower()]
    B7L.LBSCWorS = record['LBSCWorS'.lower()]
    B7L.LBSCWALK = record['LBSCWALK'.lower()]
    B7L.LBSCAWAK = record['LBSCAWAK'.lower()]
    B7L.LBSCBrtH = record['LBSCBrtH'.lower()]
    B7L.LBSCtrt  = record['LBSCtrt'.lower()]
    B7L.LBSCCrMP = record['LBSCCrMP'.lower()]
    B7L.LBSCALrt = record['LBSCALrt'.lower()]
    packet.append(B7L)


def add_b9l(record, packet):
    B9L = lbd_short_ivp_forms.FormB9L()
    B9L.CoNSFALL = record['CoNSFALL'.lower()]
    B9L.CoNSWKoF = record['CoNSWKoF'.lower()]
    B9L.CoNSLyAW = record['CoNSLyAW'.lower()]
    B9L.CoNSWKer = record['CoNSWKer'.lower()]
    B9L.CoNSLttL = record['CoNSLttL'.lower()]
    B9L.SCCorAte = record['SCCorAte'.lower()]
    B9L.CoDSUNeX = record['CoDSUNeX'.lower()]
    B9L.CoDSSItP = record['CoDSSItP'.lower()]
    B9L.CoDSWAtV = record['CoDSWAtV'.lower()]
    B9L.CoDStALK = record['CoDStALK'.lower()]
    B9L.CoDSAWDy = record['CoDSAWDy'.lower()]
    B9L.CoDSFLDy = record['CoDSFLDy'.lower()]
    packet.append(B9L)


def add_c1l(record, packet):
    C1L = lbd_short_ivp_forms.FormC1L()
    C1L.LBNPFACe = record['LBNPFACe'.lower()]
    C1L.LBNPNoIS = record['LBNPNoIS'.lower()]
    C1L.LBNPtCor = record['LBNPtCor'.lower()]
    C1L.LBNPPArD = record['LBNPPArD'.lower()]
    packet.append(C1L)


def add_d1l(record, packet):
    D1L = lbd_short_ivp_forms.FormD1L()
    D1L.LBCDSCoG = record['LBCDSCoG'.lower()]
    D1L.LBCCMeM  = record['LBCCMeM'.lower()]
    D1L.LBCCLANG = record['LBCCLANG'.lower()]
    D1L.LBCCAtt  = record['LBCCAtt'.lower()]
    D1L.LBCCeXDe = record['LBCCeXDe'.lower()]
    D1L.LBCCVIS  = record['LBCCVIS'.lower()]
    D1L.LBCDSMoV = record['LBCDSMoV'.lower()]
    D1L.LBCMBrAD = record['LBCMBrAD'.lower()]
    D1L.LBCMrIGD = record['LBCMrIGD'.lower()]
    D1L.LBCMrtrM = record['LBCMrtrM'.lower()]
    D1L.LBCMPtrM = record['LBCMPtrM'.lower()]
    D1L.LBCMAtrM = record['LBCMAtrM'.lower()]
    D1L.LBCMMyoC = record['LBCMMyoC'.lower()]
    D1L.LBCMGAIt = record['LBCMGAIt'.lower()]
    D1L.LBCMPINS = record['LBCMPINS'.lower()]
    D1L.LBCDSBeV = record['LBCDSBeV'.lower()]
    D1L.LBCBDeP  = record['LBCBDeP'.lower()]
    D1L.LBCBAPA  = record['LBCBAPA'.lower()]
    D1L.LBCBANX  = record['LBCBANX'.lower()]
    D1L.LBCBHALL = record['LBCBHALL'.lower()]
    D1L.LBCBDeL  = record['LBCBDeL'.lower()]
    D1L.LBCDSAUt = record['LBCDSAUt'.lower()]
    D1L.LBCAreM  = record['LBCAreM'.lower()]
    D1L.LBCAAPN  = record['LBCAAPN'.lower()]
    D1L.LBCALGSL = record['LBCALGSL'.lower()]
    D1L.LBCArSLe = record['LBCArSLe'.lower()]
    D1L.LBCADtSL = record['LBCADtSL'.lower()]
    D1L.LBCACGFL = record['LBCACGFL'.lower()]
    D1L.LBCAHyPt = record['LBCAHyPt'.lower()]
    D1L.LBCACoNS = record['LBCACoNS'.lower()]
    D1L.LBCAHyPS = record['LBCAHyPS'.lower()]
    D1L.LBCAFALL = record['LBCAFALL'.lower()]
    D1L.LBCASyNC = record['LBCASyNC'.lower()]
    D1L.LBCASNAP = record['LBCASNAP'.lower()]
    D1L.LBCoGSt  = record['LBCoGSt'.lower()]
    D1L.LBCoGDX  = record['LBCoGDX'.lower()]
    packet.append(D1L)


def add_e1l(record, packet):
    E1L = lbd_short_ivp_forms.FormE1L()
    E1L.LBGLrrK2 = record['LBGLrrK2'.lower()]
    E1L.LBGLrKIS = record['LBGLrKIS'.lower()]
    E1L.LBGPArK2 = record['LBGPArK2'.lower()]
    E1L.LBGPK2IS = record['LBGPK2IS'.lower()]
    E1L.LBGPArK7 = record['LBGPArK7'.lower()]
    E1L.LBGPK7IS = record['LBGPK7IS'.lower()]
    E1L.LBGPINK1 = record['LBGPINK1'.lower()]
    E1L.LBGPNKIS = record['LBGPNKIS'.lower()]
    E1L.LBGSNCA  = record['LBGSNCA'.lower()]
    E1L.LBGSNCIS = record['LBGSNCIS'.lower()]
    E1L.LBGGBA   = record['LBGGBA'.lower()]
    E1L.LBGGBAIS = record['LBGGBAIS'.lower()]
    E1L.LBGotHr  = record['LBGotHr'.lower()]
    E1L.LBGotHIS = record['LBGotHIS'.lower()]
    E1L.LBGotHX  = record['LBGotHX'.lower()]
    packet.append(E1L)


def add_e2l(record, packet):
    E2L = lbd_short_ivp_forms.FormE2L()
    E2L.LBISMrI  = record['LBISMrI'.lower()]
    E2L.LBISMHIP = record['LBISMHIP'.lower()]
    E2L.LBISMAVL = record['LBISMAVL'.lower()]
    E2L.LBIFPet  = record['LBIFPet'.lower()]
    E2L.LBIFPoCC = record['LBIFPoCC'.lower()]
    E2L.LBIFPtPP = record['LBIFPtPP'.lower()]
    E2L.LBIFPISL = record['LBIFPISL'.lower()]
    E2L.LBIFPAVL = record['LBIFPAVL'.lower()]
    E2L.LBIAPet  = record['LBIAPet'.lower()]
    E2L.LBIAPAVL = record['LBIAPAVL'.lower()]
    E2L.LBItPet  = record['LBItPet'.lower()]
    E2L.LBItPAVL = record['LBItPAVL'.lower()]
    E2L.LBIDAtS  = record['LBIDAtS'.lower()]
    E2L.LBIDSABN = record['LBIDSABN'.lower()]
    packet.append(E2L)


def add_e3l(record, packet):
    E3L = lbd_short_ivp_forms.FormE3L()
    E3L.LBoPoLyS = record['LBoPoLyS'.lower()]
    E3L.LBoPoPoS = record['LBoPoPoS'.lower()]
    E3L.LBoPoAVL = record['LBoPoAVL'.lower()]
    E3L.LBoCMIBG = record['LBoCMIBG'.lower()]
    E3L.LBoCMPoS = record['LBoCMPoS'.lower()]
    E3L.LBoCMAVL = record['LBoCMAVL'.lower()]
    E3L.LBoANoS  = record['LBoANoS'.lower()]
    E3L.LBoANPoS = record['LBoANPoS'.lower()]
    E3L.LBoANAVL = record['LBoANAVL'.lower()]
    E3L.LBoANVer = record['LBoANVer'.lower()]
    E3L.LBoANotH = record['LBoANotH'.lower()]
    E3L.LBoCGAIt = record['LBoCGAIt'.lower()]
    E3L.LBoCGPoS = record['LBoCGPoS'.lower()]
    E3L.LBoCGAVL = record['LBoCGAVL'.lower()]
    packet.append(E3L)

    update_header(record, packet)
    return packet


def update_header(record, packet):
    for header in packet:
        if header.form_name == "Z1X":
            header.PACKET = "I"
            header.FORMID = header.form_name
            header.FORMVER = 3
        else:
            header.PACKET = "IL"
            header.FORMID = header.form_name
            header.FORMVER = 3.1
        header.ADCID = record['adcid']
        header.PTID = record['ptid']
        header.VISITMO = record['visitmo']
        header.VISITDAY = record['visitday']
        header.VISITYR = record['visityr']
        header.VISITNUM = record['visitnum']
        header.INITIALS = record['initials']
