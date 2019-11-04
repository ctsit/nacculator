#!/usr/bin/env python3
###############################################################################
# Copyright 2015-2016 University of Florida. All rights reserved.
# This file is part of UF CTS-IT's NACCulator project.
# Use of this source code is governed by the license found in the LICENSE file.
###############################################################################

from nacc.uds3 import blanks
# from nacc.uds3 import clsform
from nacc.lbd.fvp import forms as lbd_fvp_forms
from nacc.uds3 import packet as lbd_fvp_packet
import sys
import re


def build_uds3_lbd_fvp_form(record):
    # Converts REDCap CSV data into a packet (list of FVP Form objects)
    packet = lbd_fvp_packet.Packet()

    # Set up the forms..........

    # This form cannot precede June 1, 2017. 
    if (int(record['visityr'])>2017) or (int(record['visityr'])==2017 and int(record['visitmo'])>6) or \
       (int(record['visityr'])==2017 and int(record['visitmo'])==6 and int(record['visitday'])>=1):
        B1L = lbd_fvp_forms.FormB1L()
        B1L.LBSSALIV = record['fu_LBSSALIV'.lower()]
        B1L.LBSSWALL = record['fu_lBSSWALL'.lower()]
        B1L.LBSINSeX = record['fu_LBSINSeX'.lower()]
        B1L.LBSPrSeX = record['fu_LBSPrSeX'.lower()]
        B1L.LBSWeIGH = record['fu_LBSWeIGH'.lower()]
        B1L.LBSSMeLL = record['fu_LBSSMeLL'.lower()]
        B1L.LBSSWeAt = record['fu_LBSSWeAT'.lower()]
        B1L.LBStoLCD = record['fu_LBStoLCD'.lower()]
        B1L.LBStoLHt = record['fu_LBStoLHt'.lower()]
        B1L.LBSDBVIS = record['fu_LBSDBVIS'.lower()]
        B1L.LBSCoNSt = record['fu_LBSCoNST'.lower()]
        B1L.LBSHDStL = record['fu_LBSHDStL'.lower()]
        B1L.LBSLSStL = record['fu_LBSLSStL'.lower()]
        B1L.LBSUBLAD = record['fu_LBSUBLAD'.lower()]
        B1L.LBSUStrM = record['fu_LBSUStrM'.lower()]
        B1L.LBSUPASS = record['fu_LBSUPASS'.lower()]
        B1L.LBSDZStU = record['fu_LBSDZStU'.lower()]
        B1L.LBSDZStN = record['fu_LBSDZStN'.lower()]
        B1L.LBSFAINt = record['fu_LBSFAINt'.lower()]
        B1L.LBSPSyM  = record['fu_LBSPSyM'.lower()]
        B1L.LBPSyAGe = record['fu_LBPSyAGe'.lower()]
        B1L.LBSSUPSy = record['fu_LBSSUPSy'.lower()]
        B1L.LBSSUPDI = record['fu_LBSSUPDI'.lower()]
        B1L.LBSSUPHt = record['fu_LBSSUPHt'.lower()]
        B1L.LBSStNSy = record['fu_LBSStNSy'.lower()]
        B1L.LBSStNDI = record['fu_LBSStNDI'.lower()]
        B1L.LBSStNHt = record['fu_LBSStNHt'.lower()]
        B1L.LBSAGerM = record['fu_LBSAGerM'.lower()]
        B1L.LBSAGeSM = record['fu_LBSAGeSM'.lower()]
        B1L.LBSAGeGt = record['fu_LBSAGeGt'.lower()]
        B1L.LBSAGeFL = record['fu_LBSAGeFL'.lower()]
        B1L.LBSAGetr = record['fu_LBSAGetr'.lower()]
        B1L.LBSAGeBr = record['fu_LBSAGeBr'.lower()]
        B1L.LBSSCLAU = record['fu_LBSSCLAU'.lower()]
        B1L.LBSSCLVr = record['fu_LBSSCLVr'.lower()]
        B1L.LBSSCLot = record['fu_LBSSCLot'.lower()]
        B1L.LBSSCor  = record['fu_LBSSCor'.lower()]
        packet.append(B1L)

        B2L = lbd_fvp_forms.FormB2L()
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

        B3L = lbd_fvp_forms.FormB3L()
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

        B4L = lbd_fvp_forms.FormB4L()
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
        B4L.LBDeLFrQ = record['fu_LBDeLFrQ'.lower()]
        B4L.LBDeLSeV = record['fu_LBDeLSeV'.lower()]
        B4L.LBDeLDSt = record['fu_LBDeLDSt'.lower()]
        B4L.LBHALL   = record['fu_LBHALL'.lower()]
        B4L.LBHVoICe = record['fu_LBHVoICe'.lower()]
        B4L.LBHPeoPL = record['fu_LBHPeoPL'.lower()]
        B4L.LBHNotPr = record['fu_LBHNotPr'.lower()]
        B4L.LBHoDor  = record['fu_LBHoDor'.lower()]
        B4L.LBHFeeL  = record['fu_LBHFeeL'.lower()]
        B4L.LBHtASte = record['fu_LBHtASte'.lower()]
        B4L.LBHotSeN = record['fu_LBHotSeN'.lower()]
        B4L.LBHALFrQ = record['fu_LBHALFrQ'.lower()]
        B4L.LBHALSeV = record['fu_LBHALSeV'.lower()]
        B4L.LBHALDSt = record['fu_LBHALDSt'.lower()]
        B4L.LBANXIet = record['fu_LBANXIet'.lower()]
        B4L.LBANeVNt = record['fu_LBANeVNt'.lower()]
        B4L.LBANreLX = record['fu_LBANreLX'.lower()]
        B4L.LBANBrtH = record['fu_LBANBrtH'.lower()]
        B4L.LBANBUtt = record['fu_LBANBUtt'.lower()]
        B4L.LBANPLAC = record['fu_LBANPLAC'.lower()]
        B4L.LBANSePr = record['fu_LBANSePr'.lower()]
        B4L.LBANotHr = record['fu_LBANotHr'.lower()]
        B4L.LBANXFrQ = record['fu_LBANXFrQ'.lower()]
        B4L.LBANXSeV = record['fu_LBANXSeV'.lower()]
        B4L.LBANXDSt = record['fu_LBANXDSt'.lower()]
        B4L.LBAPAtHy = record['fu_LBAPAtHy'.lower()]
        B4L.LBAPSPNt = record['fu_LBAPSPNt'.lower()]
        B4L.LBAPCoNV = record['fu_LBAPCoNV'.lower()]
        B4L.LBAPAFF  = record['fu_LBAPAFF'.lower()]
        B4L.LBAPCHor = record['fu_LBAPCHor'.lower()]
        B4L.LBAPINt  = record['fu_LBAPINt'.lower()]
        B4L.LBAPFAML = record['fu_LBAPFAML'.lower()]
        B4L.LBAPINtr = record['fu_LBAPINtr'.lower()]
        B4L.LBAPotH  = record['fu_LBAPotH'.lower()]
        B4L.LBAPAFrQ = record['fu_LBAPAFrQ'.lower()]
        B4L.LBAPASeV = record['fu_LBAPASeV'.lower()]
        B4L.LBAPADSt = record['fu_LBAPADSt'.lower()]
        B4L.LBDoPAM  = record['fu_LBDoPAM'.lower()]
        B4L.LBDAGe   = record['fu_LBDAGe'.lower()]
        B4L.LBDDrUG1 = record['fu_LBDDrUG1'.lower()]
        B4L.LBDDoSe1 = record['fu_LBDDoSe1'.lower()]
        B4L.LBDAGe2  = record['fu_LBDAGe2'.lower()]
        B4L.LBDDrUG2 = record['fu_LBDDrUG2'.lower()]
        B4L.LBDDoSe2 = record['fu_LBDDoSe2'.lower()]
        B4L.LBDeLAGe = record['fu_LBDeLAGe'.lower()]
        B4L.LBDeLMeD = record['fu_LBDeLMeD'.lower()]
        B4L.LBDeLMD1 = record['fu_LBDeLMD1'.lower()]
        B4L.LBDeLMD2 = record['fu_LBDeLMD2'.lower()]
        B4L.LBHALAGe = record['fu_LBHALAGe'.lower()]
        B4L.LBHALMeD = record['fu_LBHALMeD'.lower()]
        B4L.LBHALMD1 = record['fu_LBHALMD1'.lower()]
        B4L.LBHALMD2 = record['fu_LBHALMD2'.lower()]
        B4L.LBANXAGe = record['fu_LBANXAGe'.lower()]
        B4L.LBANXMeD = record['fu_LBANXMeD'.lower()]
        B4L.LBANXMD1 = record['fu_LBANXMD1'.lower()]
        B4L.LBANXMD2 = record['fu_LBANXMD2'.lower()]
        B4L.LBAPAAGe = record['fu_LBAPAAGe'.lower()]
        B4L.LBAPAMeD = record['fu_LBAPAMeD'.lower()]
        B4L.LBAPAMD1 = record['fu_LBAPAMD1'.lower()]
        B4L.LBAPAMD2 = record['fu_LBAPAMD2'.lower()]
        packet.append(B4L)

        B5L = lbd_fvp_forms.FormB5L()
        B5L.LBMLtHrG = record['fu_LBMLtHrG'.lower()]
        B5L.LBMSLeeP = record['fu_LBMSLeeP'.lower()]
        B5L.LBMDISrG = record['fu_LBMDISrG'.lower()]
        B5L.LBMStAre = record['fu_LBMStAre'.lower()]
        packet.append(B5L)

        B6L = lbd_fvp_forms.FormB6L()
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

        B7L = lbd_fvp_forms.FormB7L()
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

        B8L = lbd_fvp_forms.FormB8L()
        B8L.PACoGIMP = record['fu_PACoGIMP'.lower()]
        B8L.PANSFALL = record['fu_PANSFALL'.lower()]
        B8L.PANSWKoF = record['fu_PANSWKoF'.lower()]
        B8L.PANSLyAW = record['fu_PANSLyAW'.lower()]
        B8L.PANSWKer = record['fu_PANSWKer'.lower()]
        B8L.PANSLttL = record['fu_PANSLttL'.lower()]
        B8L.SCPArAte = record['fu_SCPArAte'.lower()]
        B8L.PADSUNeX = record['fu_PADSUNeX'.lower()]
        B8L.PADSSItP = record['fu_PADSSItP'.lower()]
        B8L.PADSWAtV = record['fu_PADSWAtV'.lower()]
        B8L.PADStALK = record['fu_PADStALK'.lower()]
        B8L.PADSAWDy = record['fu_PADSAWDy'.lower()]
        B8L.PADSFLDy = record['fu_PADSFLDy'.lower()]
        packet.append(B8L)

        B9L = lbd_fvp_forms.FormB9L()
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
        B9L.SCCoFrSt = record['fu_SCCoFrSt'.lower()]
        B9L.SCCoAGeN = record['fu_SCCoAGeN'.lower()]
        B9L.SCCoAGeD = record['fu_SCCoAGeD'.lower()]
        B9L.SCCoCoMP = record['fu_SCCoCoMP'.lower()]
        B9L.SCCoSCVr = record['fu_SCCoSCVr'.lower()]
        B9L.SCCootH  = record['fu_SCCootH'.lower()]
        B9L.SCCoSCor = record['fu_SCCoSCor'.lower()]
        packet.append(B9L)

        C1L = lbd_fvp_forms.FormC1L()
        C1L.LBNSWorD = record['fu_LBNSWorD'.lower()]
        C1L.LBNSCoLr = record['fu_LBNSCoLr'.lower()]
        C1L.LBNSCLWD = record['fu_LBNSCLWD'.lower()]
        C1L.LBNPFACe = record['fu_LBNPFACe'.lower()]
        C1L.LBNPNoIS = record['fu_LBNPNoIS'.lower()]
        C1L.LBNPtCor = record['fu_LBNPtCor'.lower()]
        C1L.LBNPPArD = record['fu_LBNPPArD'.lower()]
        packet.append(C1L)

        D1L = lbd_fvp_forms.FormD1L()
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
        
        E1L = lbd_fvp_forms.FormE1L()
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

        E2L = lbd_fvp_forms.FormE2L()
        E2L.LBISMrI  = record['fu_LBISMrI'.lower()]
        E2L.LBISMMo  = record['fu_LBISMMo'.lower()]
        E2L.LBISMDy  = record['fu_LBISMDy'.lower()]
        E2L.LBISMyr  = record['fu_LBISMyr'.lower()]
        E2L.LBISMQAV = record['fu_LBISMQAV'.lower()]
        E2L.LBISMHIP = record['fu_LBISMHIP'.lower()]
        E2L.LBISMAVL = record['fu_LBISMAVL'.lower()]
        E2L.LBISMDCM = record['fu_LBISMDCM'.lower()]
        E2L.LBISMFMt = record['fu_LBISMFMt'.lower()]
        E2L.LBISMADN = record['fu_LBISMADN'.lower()]
        E2L.LBISMVer = record['fu_LBISMVer'.lower()]
        E2L.LBISMMAN = record['fu_LBISMMAN'.lower()]
        E2L.LBISMoM  = record['fu_LBISMoM'.lower()]
        E2L.LBISMStr = record['fu_LBISMStr'.lower()]
        E2L.LBISMoS  = record['fu_LBISMoS'.lower()]
        E2L.LBIFPet  = record['fu_LBIFPet'.lower()]
        E2L.LBIFPMo  = record['fu_LBIFPMo'.lower()]
        E2L.LBIFPDy  = record['fu_LBIFPDy'.lower()]
        E2L.LBIFPyr  = record['fu_LBIFPyr'.lower()]
        E2L.LBIFPQAV = record['fu_LBIFPQAV'.lower()]
        E2L.LBIFPoCC = record['fu_LBIFPoCC'.lower()]
        E2L.LBIFPtPP = record['fu_LBIFPtPP'.lower()]
        E2L.LBIFPISL = record['fu_LBIFPISL'.lower()]
        E2L.LBIFPAVL = record['fu_LBIFPAVL'.lower()]
        E2L.LBIFPDCM = record['fu_LBIFPDCM'.lower()]
        E2L.LBIFPFMt = record['fu_LBIFPFMt'.lower()]
        E2L.LBIFPADN = record['fu_LBIFPADN'.lower()]
        E2L.LBIFPVer = record['fu_LBIFPVer'.lower()]
        E2L.LBIFPMAN = record['fu_LBIFPMAN'.lower()]
        E2L.LBIFPoM  = record['fu_LBIFPoM'.lower()]
        E2L.LBIAPet  = record['fu_LBIAPet'.lower()]
        E2L.LBIAPMo  = record['fu_LBIAPMo'.lower()]
        E2L.LBIAPDy  = record['fu_LBIAPDy'.lower()]
        E2L.LBIAPyr  = record['fu_LBIAPyr'.lower()]
        E2L.LBIAPQAV = record['fu_LBIAPQAV'.lower()]
        E2L.LBIAPAVL = record['fu_LBIAPAVL'.lower()]
        E2L.LBIAPDCM = record['fu_LBIAPDCM'.lower()]
        E2L.LBIAPFMt = record['fu_LBIAPFMt'.lower()]
        E2L.LBIAPLIG = record['fu_LBIAPLIG'.lower()]
        E2L.LBIAPoL  = record['fu_LBIAPoL'.lower()]
        E2L.LBIAPADN = record['fu_LBIAPADN'.lower()]
        E2L.LBIAPVer = record['fu_LBIAPVer'.lower()]
        E2L.LBIAPMAN = record['fu_LBIAPMAN'.lower()]
        E2L.LBIAPoM  = record['fu_LBIAPoM'.lower()]
        E2L.LBItPet  = record['fu_LBItPet'.lower()]
        E2L.LBItPMo  = record['fu_LBItPMo'.lower()]
        E2L.LBItPDy  = record['fu_LBItPDy'.lower()]
        E2L.LBItPyr  = record['fu_LBItPyr'.lower()]
        E2L.LBItPQAV = record['fu_LBItPQAV'.lower()]
        E2L.LBItPAVL = record['fu_LBItPAVL'.lower()]
        E2L.LBItPDCM = record['fu_LBItPDCM'.lower()]
        E2L.LBItPFMt = record['fu_LBItPFMt'.lower()]
        E2L.LBItPLIG = record['fu_LBItPLIG'.lower()]
        E2L.LBItPoL  = record['fu_LBItPoL'.lower()]
        E2L.LBItPADN = record['fu_LBItPADN'.lower()]
        E2L.LBItPVer = record['fu_LBItPVer'.lower()]
        E2L.LBItPMAN = record['fu_LBItPMAN'.lower()]
        E2L.LBItPoM  = record['fu_LBItPoM'.lower()]
        E2L.LBIDAtS  = record['fu_LBIDAtS'.lower()]
        E2L.LBIDSMo  = record['fu_LBIDSMo'.lower()]
        E2L.LBIDSDy  = record['fu_LBIDSDy'.lower()]
        E2L.LBIDSyr  = record['fu_LBIDSyr'.lower()]
        E2L.LBIDSQAV = record['fu_LBIDSQAV'.lower()]
        E2L.LBIDSABN = record['fu_LBIDSABN'.lower()]
        packet.append(E2L)

        E3L = lbd_fvp_forms.FormE3L()
        E3L.LBoPoLyS = record['fu_LBoPoLyS'.lower()]
        E3L.LBoPoSMo = record['fu_LBoPoSMo'.lower()]
        E3L.LBoPoSDy = record['fu_LBoPoSDy'.lower()]
        E3L.LBoPoSyr = record['fu_LBoPoSyr'.lower()]
        E3L.LBoPoPoS = record['fu_LBoPoPoS'.lower()]
        E3L.LBoPoAVL = record['fu_LBoPoAVL'.lower()]
        E3L.LBoCMIBG = record['fu_LBoCMIBG'.lower()]
        E3L.LBoCMMo  = record['fu_LBoCMMo'.lower()]
        E3L.LBoCMDy  = record['fu_LBoCMDy'.lower()]
        E3L.LBoCMyr  = record['fu_LBoCMyr'.lower()]
        E3L.LBoCMPoS = record['fu_LBoCMPoS'.lower()]
        E3L.LBoCMAVL = record['fu_LBoCMAVL'.lower()]
        E3L.LBoANoS  = record['fu_LBoANoS'.lower()]
        E3L.LBoANMo  = record['fu_LBoANMo'.lower()]
        E3L.LBoANDy  = record['fu_LBoANDy'.lower()]
        E3L.LBoANyr  = record['fu_LBoANyr'.lower()]
        E3L.LBoANPoS = record['fu_LBoANPoS'.lower()]
        E3L.LBoANAVL = record['fu_LBoANAVL'.lower()]
        E3L.LBoANVer = record['fu_LBoANVer'.lower()]
        E3L.LBoANotH = record['fu_LBoANotH'.lower()]
        E3L.LBoeeG   = record['fu_LBOeeG'.lower()]
        E3L.LBoeGMo  = record['fu_LBoeGMo'.lower()]
        E3L.LBoeGDy  = record['fu_LBoeGDy'.lower()]
        E3L.LBoeGyr  = record['fu_LBoeGyr'.lower()]
        E3L.LBoeGPoS = record['fu_LBoeGPoS'.lower()]
        E3L.LBoeGAVL = record['fu_LBoeGAVL'.lower()]
        E3L.LBoMSLt  = record['fu_LBoMSLt'.lower()]
        E3L.LBoMSMo  = record['fu_LBoMSMo'.lower()]
        E3L.LBoMSDy  = record['fu_LBoMSDy'.lower()]
        E3L.LBoMSyr  = record['fu_LBoMSyr'.lower()]
        E3L.LBoMSPoS = record['fu_LBoMSPoS'.lower()]
        E3L.LBoMSAVL = record['fu_LBoMSAVL'.lower()]
        E3L.LBotILt  = record['fu_LBotILt'.lower()]
        E3L.LBotLMo  = record['fu_LBotLMo'.lower()]
        E3L.LBotLDy  = record['fu_LBotLDY'.lower()]
        E3L.LBotLyr  = record['fu_LBotLyr'.lower()]
        E3L.LBotLPoS = record['fu_LBotLPoS'.lower()]
        E3L.LBotLAVL = record['fu_LBotLAVL'.lower()]
        E3L.LBoQSArt = record['fu_LBoQSArt'.lower()]
        E3L.LBoQSMo  = record['fu_LBoQSMo'.lower()]
        E3L.LBoQSDy  = record['fu_LBoQSDy'.lower()]
        E3L.LBoQSyr  = record['fu_LBoQSyr'.lower()]
        E3L.LBoQSPoS = record['fu_LBoQSPoS'.lower()]
        E3L.LBoSGAVL = record['fu_LBoSGAVL'.lower()]
        E3L.LBotHerM = record['fu_LBotHerM'.lower()]
        E3L.LBotHMo  = record['fu_LBotHMo'.lower()]
        E3L.LBotHDy  = record['fu_LBotHDy'.lower()]
        E3L.LBotHyr  = record['fu_LBotHyr'.lower()]
        E3L.LBotHPoS = record['fu_LBotHPoS'.lower()]
        E3L.LBotHAVL = record['fu_LBotHAVL'.lower()]
        E3L.LBoCGAIt = record['fu_LBoCGAIt'.lower()]
        E3L.LBoCGMo  = record['fu_LBoCGMo'.lower()]
        E3L.LBoCGDy  = record['fu_LBoCGDy'.lower()]
        E3L.LBoCGyr  = record['fu_LBoCGyr'.lower()]
        E3L.LBoCGPoS = record['fu_LBoCGPoS'.lower()]
        E3L.LBoCGAVL = record['fu_LBoCGAVL'.lower()]
        packet.append(E3L)

        update_header(record,packet)
    else: raise ValueError('Visit date cannot precede June 1, 2017.')

    return packet


def update_header(record, packet):
    for header in packet:
        header.PACKET = "FL"
        header.FORMID = header.form_name
        header.FORMVER = 3
        header.ADCID = record['adcid']
        header.PTID = record['ptid']
        header.VISITMO = record['visitmo']
        header.VISITDAY = record['visitday']
        header.VISITYR = record['visityr']
        header.VISITNUM = record['visitnum']
        header.INITIALS = record['initials']
