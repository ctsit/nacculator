import unittest

from nacc.uds3 import packet
from nacc.uds3.ivp import builder as ivp_builder
from nacc.uds3.fvp import builder as fvp_builder


class TestFTLDFormSkip(unittest.TestCase):

    # def test_c1s_ivp_skip(self):
    #     """ If the IVP C1S is not present in the csv, it should be skipped
    #     without throwing an error """
    #     record = make_blank_ivp()
    #     record['a2_sub'] = '1'

    #     ipacket = packet.Packet()
    #     ivp_builder.add_z1_or_z1x(record, ipacket)
    #     self.assertEqual(ipacket['A2SUB'], '1')

    # def test_c1s_fvp_skip(self):
    #     """ If the FVP C1S is not present in the csv, it should be skipped
    #     without throwing an error """
    #     record = make_blank_fvp()
    #     record['a2_sub'] = '1'

    #     fpacket = packet.Packet()
    #     fvp_builder.add_z1_or_z1x(record, fpacket)
    #     self.assertEqual(ipacket['A2SUB'], '1')

    def test_ivp_b4_not_skipped(self):
        """ Form B4 is required and should never be skipped. Testing B4 in
        particular because it is in the middle of the "add form" logic rather
        than outside the try/catch and if statements. """
        record = make_blank_ivp_B4()
        record['langa1'] = '1'

        ipacket = packet.Packet()
        ivp_builder.add_z1_or_z1x(record, ipacket)
        self.assertEqual(ipacket['LANGA1'], '1')

    def test_fvp_b4_not_skipped(self):
        """ Form B4 is required and should never be skipped. Testing B4 in
        particular because it is in the middle of the "add form" logic rather
        than outside the try/catch and if statements. """
        record = make_blank_fvp_B4()
        record['langa1'] = '1'

        fpacket = packet.Packet()
        fvp_builder.add_z1_or_z1x(record, fpacket)
        self.assertEqual(ipacket['LANGA1'], '1')

    def test_z1_added_to_fvp_when_filled(self):
        """ If the Z1 form is present, make sure it is added """
        record = make_blank_fvp()
        record['fu_a2_sub'] = '1'

        fpacket = packet.Packet()
        fvp_builder.add_z1_or_z1x(record, fpacket)
        self.assertEqual(fpacket['A2SUB'], '1')

    def test_z1x_added_to_fvp_when_filled(self):
        """ If the Z1 form is absent from the csv, it should simply
        be skipped without throwing an error """
        record = make_blank_fvp_Z1X()
        record['fu_langa1'] = '1'

        fpacket = packet.Packet()
        fvp_builder.add_z1_or_z1x(record, fpacket)
        self.assertEqual(fpacket['LANGA1'], '1')


def make_blank_ivp():
    return {
        'visitmo': '1',
        'visitday': '1',
        'visityr': '2017',
        # Z1
        'a2_sub': '',
        'a2_not': '',
        'a2_comm': '',
        'a3_sub': '',
        'a3_not': '',
        'a3_comm': '',
        'a4_sub': '',
        'a4_not': '',
        'a4_comm': '',
        'b1_sub': '',
        'b1_not': '',
        'b1_comm': '',
        'b5_sub': '',
        'b5_not': '',
        'b5_comm': '',
        'b6_sub': '',
        'b6_not': '',
        'b6_comm': '',
        'b7_sub': '',
        'b7_not': '',
        'b7_comm': '',
        'ivp_z1_complete': '2',
        # Z1X
        'langa1': '',
        'langa2': '',
        'a2sub': '',
        'a2not': '',
        'langa3': '',
        'a3sub': '',
        'a3not': '',
        'langa4': '',
        'a4sub': '',
        'a4not': '',
        'langa5': '',
        'langb1': '',
        'b1sub': '',
        'b1not': '',
        'langb4': '',
        'langb5': '',
        'b5sub': '',
        'b5not': '',
        'langb6': '',
        'b6sub': '',
        'b6not': '',
        'langb7': '',
        'b7sub': '',
        'b7not': '',
        'langb8': '',
        'langb9': '',
        'langc2': '',
        'langd1': '',
        'langd2': '',
        'langa3a': '',
        'ftda3afs': '',
        'ftda3afr': '',
        'langb3f': '',
        'langb9f': '',
        'langc1f': '',
        'langc2f': '',
        'langc3f': '',
        'langc4f': '',
        'ftdc4fs': '',
        'ftdc4fr': '',
        'ftdc5fs': '',
        'ftdc5fr': '',
        'ftdc6fs': '',
        'ftdc6fr': '',
        'lange2f': '',
        'lange3f': '',
        'langcls': '',
        'clssub': '',
        'ivp_z1x_complete': '2'
    }


def make_blank_ivp_Z1X():
    return {
        'visitmo': '1',
        'visitday': '1',
        'visityr': '2019',
        # Z1X
        'langa1': '',
        'langa2': '',
        'a2sub': '',
        'a2not': '',
        'langa3': '',
        'a3sub': '',
        'a3not': '',
        'langa4': '',
        'a4sub': '',
        'a4not': '',
        'langa5': '',
        'langb1': '',
        'b1sub': '',
        'b1not': '',
        'langb4': '',
        'langb5': '',
        'b5sub': '',
        'b5not': '',
        'langb6': '',
        'b6sub': '',
        'b6not': '',
        'langb7': '',
        'b7sub': '',
        'b7not': '',
        'langb8': '',
        'langb9': '',
        'langc2': '',
        'langd1': '',
        'langd2': '',
        'langa3a': '',
        'ftda3afs': '',
        'ftda3afr': '',
        'langb3f': '',
        'langb9f': '',
        'langc1f': '',
        'langc2f': '',
        'langc3f': '',
        'langc4f': '',
        'ftdc4fs': '',
        'ftdc4fr': '',
        'ftdc5fs': '',
        'ftdc5fr': '',
        'ftdc6fs': '',
        'ftdc6fr': '',
        'lange2f': '',
        'lange3f': '',
        'langcls': '',
        'clssub': '',
        'ivp_z1x_complete': '2'
    }


def make_blank_fvp():
    return {
        'visitmo': '1',
        'visitday': '1',
        'visityr': '2017',
        # Z1
        'fu_a2_sub': '',
        'fu_a2_not': '',
        'fu_a2_comm': '',
        'fu_a3_sub': '',
        'fu_a3_not': '',
        'fu_a3_comm': '',
        'fu_a4_sub': '',
        'fu_a4_not': '',
        'fu_a4_comm': '',
        'fu_b1_sub': '',
        'fu_b1_not': '',
        'fu_b1_comm': '',
        'fu_b5_sub': '',
        'fu_b5_not': '',
        'fu_b5_comm': '',
        'fu_b6_sub': '',
        'fu_b6_not': '',
        'fu_b6_comm': '',
        'fu_b7_sub': '',
        'fu_b7_not': '',
        'fu_b7_comm': '',
        'fvp_z1_complete': '2',
        # Z1X
        'fu_langa1': '',
        'fu_langa2': '',
        'fu_a2sub': '',
        'fu_a2not': '',
        'fu_langa3': '',
        'fu_a3sub': '',
        'fu_a3not': '',
        'fu_langa4': '',
        'fu_a4sub': '',
        'fu_a4not': '',
        'fu_langb1': '',
        'fu_b1sub': '',
        'fu_b1not': '',
        'fu_langb4': '',
        'fu_langb5': '',
        'fu_b5sub': '',
        'fu_b5not': '',
        'fu_langb6': '',
        'fu_b6sub': '',
        'fu_b6not': '',
        'fu_langb7': '',
        'fu_b7sub': '',
        'fu_b7not': '',
        'fu_langb8': '',
        'fu_langb9': '',
        'fu_langc2': '',
        'fu_langd1': '',
        'fu_langd2': '',
        'fu_langa3a': '',
        'fu_ftda3afs': '',
        'fu_ftda3afr': '',
        'fu_langb3f': '',
        'fu_langb9f': '',
        'fu_langc1f': '',
        'fu_langc2f': '',
        'fu_langc3f': '',
        'fu_langc4f': '',
        'fu_ftdc4fs': '',
        'fu_ftdc4fr': '',
        'fu_ftdc5fs': '',
        'fu_ftdc5fr': '',
        'fu_ftdc6fs': '',
        'fu_ftdc6fr': '',
        'fu_lange2f': '',
        'fu_lange3f': '',
        'fu_langcls': '',
        'fu_clssub': '',
        'fvp_z1x_complete': '2'
    }


def make_blank_fvp_Z1X():
    return {
        'visitmo': '1',
        'visitday': '1',
        'visityr': '2019',
        # Z1X
        'fu_langa1': '',
        'fu_langa2': '',
        'fu_a2sub': '',
        'fu_a2not': '',
        'fu_langa3': '',
        'fu_a3sub': '',
        'fu_a3not': '',
        'fu_langa4': '',
        'fu_a4sub': '',
        'fu_a4not': '',
        'fu_langb1': '',
        'fu_b1sub': '',
        'fu_b1not': '',
        'fu_langb4': '',
        'fu_langb5': '',
        'fu_b5sub': '',
        'fu_b5not': '',
        'fu_langb6': '',
        'fu_b6sub': '',
        'fu_b6not': '',
        'fu_langb7': '',
        'fu_b7sub': '',
        'fu_b7not': '',
        'fu_langb8': '',
        'fu_langb9': '',
        'fu_langc2': '',
        'fu_langd1': '',
        'fu_langd2': '',
        'fu_langa3a': '',
        'fu_ftda3afs': '',
        'fu_ftda3afr': '',
        'fu_langb3f': '',
        'fu_langb9f': '',
        'fu_langc1f': '',
        'fu_langc2f': '',
        'fu_langc3f': '',
        'fu_langc4f': '',
        'fu_ftdc4fs': '',
        'fu_ftdc4fr': '',
        'fu_ftdc5fs': '',
        'fu_ftdc5fr': '',
        'fu_ftdc6fs': '',
        'fu_ftdc6fr': '',
        'fu_lange2f': '',
        'fu_lange3f': '',
        'fu_langcls': '',
        'fu_clssub': '',
        'fvp_z1x_complete': '2'
    }


if __name__ == "__main__":
    unittest.main()
