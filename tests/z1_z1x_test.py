import unittest

from nacc.uds3 import packet
from nacc.uds3.ivp import builder as ivp_builder
from nacc.uds3.fvp import builder as fvp_builder

class TestC1SC2(unittest.TestCase):

    def test_z1_added_to_ivp_when_filled(self):
        """ If header is from before April 2, 2018, the Z1 form should be added """
        record = make_blank_ivp()
        record['visityr'] = '2016'
        record['a2sub'] = '1'
        record['b7comm'] = '1'

        ipacket = packet.Packet()
        ivp_builder.add_z1_or_z1x(record, ipacket)
        self.assertEqual(ipacket['A2SUB'], '1')

    def test_z1x_added_to_ivp_when_filled(self):
        """ If header is from after April 2, 2018, the Z1X form should be added """
        record = make_blank_ivp()
        record['visityr'] = '2019'
        record['a1lang'] = '1'
        record['clssubmitted'] = '1'

        ipacket = packet.Packet()
        ivp_builder.add_z1_or_z1x(record, ipacket)
        self.assertEqual(ipacket['LANGA1'], '1')

    def test_z1_added_to_fvp_when_filled(self):
        """ If header is from before April 2, 2018, the Z1 form should be added """
        record = make_blank_fvp()
        record['visityr'] = '2016'
        record['fu_a2sub'] = '1'
        record['fu_b7comm'] = '1'

        fpacket = packet.Packet()
        fvp_builder.add_z1_or_z1x(record, fpacket)
        self.assertEqual(fpacket['A2SUB'], '1')

    def test_z1x_added_to_fvp_when_filled(self):
        """ If header is from after April 2, 2018, the Z1X form should be added """
        record = make_blank_fvp()
        record['visityr'] = '2019'
        record['fu_a1lang'] = '1'
        record['fu_clssubmitted'] = '1'

        fpacket = packet.Packet()
        fvp_builder.add_z1_or_z1x(record, fpacket)
        self.assertEqual(fpacket['LANGA1'], '1')

def make_blank_ivp():
    return {
        'visitmo': '',
        'visitday': '',
        'visityr': '',
        # Z1
        'a2sub': '',
        'a2not': '',
        'a2comm': '',
        'a3sub': '',
        'a3not': '',
        'a3comm': '',
        'a4sub': '',
        'a4not': '',
        'a4comm': '',
        'b1sub': '',
        'b1not': '',
        'b1comm': '',
        'b5sub': '',
        'b5not': '',
        'b5comm': '',
        'b6sub': '',
        'b6not': '',
        'b6comm': '',
        'b7sub': '',
        'b7not': '',
        'b7comm': '',
        # Z1X
        'a1lang': '',
        'a2lang': '',
        'a2sub_095a3b': '',
        'a2not_21e87d': '',
        'a3lang': '',
        'a3sub_2b0d69': '',
        'a3not_c7cb57': '',
        'a4lang': '',
        'a4sub_2c437c': '',
        'a4not_c4e53e': '',
        'a5lang': '',
        'b1lang': '',
        'b1sub_3c9b3b': '',
        'b1not_8b7733': '',
        'b4lang': '',
        'b5lang': '',
        'b5sub_712f66': '',
        'b5not_a4b779': '',
        'b6lang': '',
        'b6sub_35db4c': '',
        'b6not_06dff0': '',
        'b7lang': '',
        'b7sub_7e2220': '',
        'b7not_2dfac5': '',
        'b8lang': '',
        'b9lang': '',
        'c2lang': '',
        'd1lang': '',
        'd2lang': '',
        'a3alang': '',
        'a3asubmitted': '',
        'a3anot': '',
        'b3flang': '',
        'b9flang': '',
        'c1flang': '',
        'c2flang': '',
        'c3flang': '',
        'c4flang': '',
        'c4fsubmitted': '',
        'c4fnot': '',
        'c5fsubmitted': '',
        'c5fnot': '',
        'c6fsubmitted': '',
        'c6fnot': '',
        'e2flang': '',
        'e3flang': '',
        'clslang': '',
        'clssubmitted': ''
    }


def make_blank_fvp():
    return {
        'visitmo': '',
        'visitday': '',
        'visityr': '',
        # Z1
        'fu_a2sub': '',
        'fu_a2not': '',
        'fu_a2comm': '',
        'fu_a3sub': '',
        'fu_a3not': '',
        'fu_a3comm': '',
        'fu_a4sub': '',
        'fu_a4not': '',
        'fu_a4comm': '',
        'fu_b1sub': '',
        'fu_b1not': '',
        'fu_b1comm': '',
        'fu_b5sub': '',
        'fu_b5not': '',
        'fu_b5comm': '',
        'fu_b6sub': '',
        'fu_b6not': '',
        'fu_b6comm': '',
        'fu_b7sub': '',
        'fu_b7not': '',
        'fu_b7comm': '',
        # Z1X
        'fu_a1lang': '',
        'fu_a2lang': '',
        'fu_a2sub_73fdc7': '',
        'fu_a2not_fd65a7': '',
        'fu_a3lang': '',
        'fu_a3sub_c2a68b': '',
        'fu_a3not_f7c411': '',
        'fu_a4lang': '',
        'fu_a4sub_143f22': '',
        'fu_a4not_b95e64': '',
        'fu_b1lang': '',
        'fu_b1sub_c03500': '',
        'fu_b1not_0a7e9f': '',
        'fu_b4lang': '',
        'fu_b5lang': '',
        'fu_b5sub_51a694': '',
        'b5not_fvpz1x': '',
        'fu_b6lang': '',
        'fu_b6sub_db439d': '',
        'fu_b6not_310244': '',
        'fu_b7lang': '',
        'fu_b7sub_21a95f': '',
        'fu_b7not_dccb30': '',
        'fu_b8lang': '',
        'fu_b9lang': '',
        'fu_c2lang': '',
        'fu_d1lang': '',
        'fu_d2lang': '',
        'fu_a3alang': '',
        'fu_a3asubmitted': '',
        'fu_a3anot': '',
        'fu_b3flang': '',
        'fu_b9flang': '',
        'fu_c1flang': '',
        'fu_c2flang': '',
        'fu_c3flang': '',
        'fu_c4flang': '',
        'fu_c4fsubmitted': '',
        'fu_c4fnot': '',
        'fu_c5fsubmitted': '',
        'fu_c5fnot': '',
        'fu_c6fsubmitted': '',
        'fu_c6fnot': '',
        'fu_e2flang': '',
        'fu_e3flang': '',
        'fu_clslang': '',
        'fu_clssubmitted': ''
    }

if __name__ == "__main__":
    unittest.main()
