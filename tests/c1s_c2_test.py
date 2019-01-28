import unittest

from nacc.uds3 import packet
from nacc.uds3.ivp import builder as ivp_builder
from nacc.uds3.fvp import builder as fvp_builder

class TestC1SC2(unittest.TestCase):

    def test_c1s_added_to_ivp_when_filled(self):
        """ If header is from before October 23, 2017, the C1S form should be added """
        record = make_blank_ivp()
        record['visityr'] = '2016'
        record['c1s_1a_mmseloc'] = '1'
        record['c1s_11a_cogstat'] = '1'

        ipacket = packet.Packet()
        ivp_builder.add_c1s_or_c2(record, ipacket)
        self.assertEqual(ipacket['MMSELOC'], '1')

    def test_c2_added_to_ivp_when_filled(self):
        """ If header is from after October 23, 2017, the C2 form should be added """
        record = make_blank_ivp()
        record['visityr'] = '2018'
        record['mocacomp'] = '1'
        record['cogstat_c2'] = '1'

        ipacket = packet.Packet()
        ivp_builder.add_c1s_or_c2(record, ipacket)
        self.assertEqual(ipacket['MOCACOMP'], '1')

    def test_c1s_added_to_fvp_when_filled(self):
        """ If header is from before October 23, 2017, the C1S form should be added """
        record = make_blank_fvp()
        record['visityr'] = '2016'
        record['fu_mmsecomp'] = '1'
        record['fu_cogstat'] = '1'

        fpacket = packet.Packet()
        fvp_builder.add_c1s_or_c2(record, fpacket)
        self.assertEqual(fpacket['MMSECOMP'], '1')

    def test_c2_added_to_fvp_when_filled(self):
        """ If header is from after October 23, 2017, the C2 form should be added """
        record = make_blank_fvp()
        record['visityr'] = '2018'
        record['fu_mocacomp'] = '1'
        record['fu_cogstat_c2'] = '1'

        fpacket = packet.Packet()
        fvp_builder.add_c1s_or_c2(record, fpacket)
        self.assertEqual(fpacket['MOCACOMP'], '1')

def make_blank_ivp():
    return {
        'visitmo': '',
        'visitday': '',
        'visityr': '',
        # C1
        'c1s_1a_mmseloc': '',
        'c1s_1a1_mmselan': '',
        'c1s_1a2_mmselanx': '',
        'c1s_1b1_mmseorda': '',
        'c1s_1b2_mmseorlo': '',
        'c1s_1c_pentagon': '',
        'c1s_1d_mmse': '',
        'c1s_2_npsycloc': '',
        'c1s_2a_npsylan': '',
        'c1s_2a1_npsylanx': '',
        'c1s_3amo_logimo': '',
        'c1s_3ady_logiday': '',
        'c1s_3ayr_logiyr': '',
        'c1s_3a1_logiprev': '',
        'c1s_3b_logimem': '',
        'c1s_4a_digif': '',
        'c1s_4b_digiflen': '',
        'c1s_5a_digib': '',
        'c1s_5b_digiblen': '',
        'c1s_6a_animals': '',
        'c1s_6b_veg': '',
        'c1s_7a_traila': '',
        'c1s_7a1_trailarr': '',
        'c1s_7a2_trailali': '',
        'c1s_7b_trailb': '',
        'c1s_7b1_trailbrr': '',
        'c1s_7b2_trailbli': '',
        'c1s_8a_wais': '',
        'c1s_9a_memunits': '',
        'c1s_9b_memtime': '',
        'c1s_10a_boston': '',
        'c1s_11a_cogstat': '',
        # C2
        'mocacomp': '',
        'mocareas': '',
        'mocaloc': '',
        'mocalan': '',
        'mocalanx': '',
        'mocavis': '',
        'mocahear': '',
        'mocatots': '',
        'mocatrai': '',
        'mocacube': '',
        'mocacloc': '',
        'mocaclon': '',
        'mocacloh': '',
        'mocanami': '',
        'mocaregi': '',
        'mocadigi': '',
        'mocalett': '',
        'mocaser7': '',
        'mocarepe': '',
        'mocaflue': '',
        'mocaabst': '',
        'mocarecn': '',
        'mocarecc': '',
        'mocarecr': '',
        'mocaordt': '',
        'mocaormo': '',
        'mocaoryr': '',
        'mocaordy': '',
        'mocaorpl': '',
        'mocaorct': '',
        'npsycloc_c2': '',
        'npsylan_c2': '',
        'npsylanx_c2': '',
        'craftvrs': '',
        'crafturs': '',
        'udsbentc': '',
        'digforct': '',
        'digforsl': '',
        'digbacct': '',
        'digbacls': '',
        'animals_c2': '',
        'veg_c2': '',
        'traila_c2': '',
        'trailarr_c2': '',
        'trailali_c2': '',
        'trailb_c2': '',
        'trailbrr_c2': '',
        'trailbli_c2': '',
        'craftdvr': '',
        'craftdre': '',
        'craftdti': '',
        'craftcue': '',
        'udsbentd': '',
        'udsbenrs': '',
        'minttots': '',
        'minttotw': '',
        'mintscng': '',
        'mintscnc': '',
        'mintpcng': '',
        'mintpcnc': '',
        'udsverfc': '',
        'udsverfn': '',
        'udsvernf': '',
        'udsverlc': '',
        'udsverlr': '',
        'udsverln': '',
        'udsvertn': '',
        'udsverte': '',
        'udsverti': '',
        'cogstat_c2': ''

    }


def make_blank_fvp():
    return {
        'visitmo': '',
        'visitday': '',
        'visityr': '',
        # C1S
        'fu_mmsecomp': '',
        'fu_mmsereas': '',
        'fu_mmseloc': '',
        'fu_mmselan': '',
        'fu_mmselanx': '',
        'fu_mmsevis': '',
        'fu_mmsehear': '',
        'fu_mmseorda': '',
        'fu_mmseorlo': '',
        'fu_pentagon': '',
        'fu_mmse': '',
        'fu_npsycloc': '',
        'fu_npsylan': '',
        'fu_npsylanx': '',
        'fu_logimo': '',
        'fu_logiday': '',
        'fu_logiyr': '',
        'fu_logiprev': '',
        'fu_logimem': '',
        'fu_udsbentc_c1': '',
        'fu_digif': '',
        'fu_digiflen': '',
        'fu_digib': '',
        'fu_digiblen': '',
        'fu_animals': '',
        'fu_veg': '',
        'fu_traila': '',
        'fu_trailarr': '',
        'fu_trailali': '',
        'fu_trailb': '',
        'fu_trailbrr': '',
        'fu_trailbli': '',
        'fu_memunits': '',
        'fu_memtime': '',
        'fu_udsbentd_c1': '',
        'fu_udsbenrs_c1': '',
        'fu_boston': '',
        'fu_udsverfc_c1': '',
        'fu_udsverfn_c1': '',
        'fu_udsvernf_c1': '',
        'fu_udsverlc_c1': '',
        'fu_udsverlr_c1': '',
        'fu_udsverln_c1': '',
        'fu_udsvertn_c1': '',
        'fu_udsverte_c1': '',
        'fu_udsverti_c1': '',
        'fu_cogstat': '',
        # C2
        'fu_mocacomp': '',
        'fu_mocareas': '',
        'fu_mocaloc': '',
        'fu_mocalan': '',
        'fu_mocalanx': '',
        'fu_mocavis': '',
        'fu_mocahear': '',
        'fu_mocatots': '',
        'fu_mocatrai': '',
        'fu_mocacube': '',
        'fu_mocacloc': '',
        'fu_mocaclon': '',
        'fu_mocacloh': '',
        'fu_mocanami': '',
        'fu_mocaregi': '',
        'fu_mocadigi': '',
        'fu_mocalett': '',
        'fu_mocaser7': '',
        'fu_mocarepe': '',
        'fu_mocaflue': '',
        'fu_mocaabst': '',
        'fu_mocarecn': '',
        'fu_mocarecc': '',
        'fu_mocarecr': '',
        'fu_mocaordt': '',
        'fu_mocaormo': '',
        'fu_mocaoryr': '',
        'fu_mocaordy': '',
        'fu_mocaorpl': '',
        'fu_mocaorct': '',
        'fu_npsycloc_c2': '',
        'fu_npsylan_c2': '',
        'fu_npsylanx_c2': '',
        'fu_craftvrs': '',
        'fu_crafturs': '',
        'fu_udsbentc': '',
        'fu_digforct': '',
        'fu_digforsl': '',
        'fu_digbacct': '',
        'fu_digbacls': '',
        'fu_animals_c2': '',
        'fu_veg_c2': '',
        'fu_traila_c2': '',
        'fu_trailarr_c2': '',
        'fu_trailali_c2': '',
        'fu_trailb_c2': '',
        'fu_trailbrr_c2': '',
        'fu_trailbli_c2': '',
        'fu_craftdvr': '',
        'fu_craftdre': '',
        'fu_craftdti': '',
        'fu_craftcue': '',
        'fu_udsbentd': '',
        'fu_udsbenrs': '',
        'fu_minttots': '',
        'fu_minttotw': '',
        'fu_mintscng': '',
        'fu_mintscnc': '',
        'fu_mintpcng': '',
        'fu_mintpcnc': '',
        'fu_udsverfc': '',
        'fu_udsverfn': '',
        'fu_udsvernf': '',
        'fu_udsverlc': '',
        'fu_udsverlr': '',
        'fu_udsverln': '',
        'fu_udsvertn': '',
        'fu_udsverte': '',
        'fu_udsverti': '',
        'fu_cogstat_c2': ''

    }

if __name__ == "__main__":
    unittest.main()
