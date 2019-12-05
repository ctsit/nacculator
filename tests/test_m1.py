import unittest

from nacc.uds3.m import builder as m_builder
from nacc.uds3 import blanks
from nacc.uds3 import packet as m_packet
from nacc.uds3.m import forms as m_form


class TestM1(unittest.TestCase):
    # add tests in class
    def test_m1_death_date_accept(self):
        """ death date format interpreter accept correct dates """
        date = ['12/12/2012', '12-12-2012', '2012/12/12', '2012-12-12']
        date_parsed = ['12', '12', '2012', '12', '12', '2012', '12', '12', '2012', '12', '12', '2012']
        record = make_blank_m()
        out = []
        for x in date:
            record['DECEASED'] = '1'
            record['DEATHMO'] = m_builder.parse_date(x, 'M')
            record['DEATHDY'] = m_builder.parse_date(x, 'D')
            record['DEATHYR'] = m_builder.parse_date(x, 'Y')
            out += [str(record['DEATHMO']), str(record['DEATHDY']), str(record['DEATHYR'])]
        self.assertEqual(date_parsed, out)

    def test_m1_death_date_reject(self):
        """ death date format interpreter rejects wrong dates """
        date = ['12/12/2012', '12-1212', '12/2012/12', '2012-12-12']
        date_parsed = ['12', '12', '2012', '12', '12', '2012', '12', '12', '2012', '12', '12', '2012']
        record = make_blank_m()
        out = []
        with self.assertRaises(ValueError):
            for x in date:
                record['DECEASED'] = '1'
                record['DEATHMO'] = m_builder.parse_date(x, 'M')
                record['DEATHDY'] = m_builder.parse_date(x, 'D')
                record['DEATHYR'] = m_builder.parse_date(x, 'Y')
                out += [str(record['DEATHMO']), str(record['DEATHDY']), str(record['DEATHYR'])]
        self.assertNotEqual(date_parsed, out)

    @unittest.skip("'0' is outside of the inclusive_range for 'FTLDREAS', 'FTLDREAX' should be left blank if FTLDREAS is filled regardless of 'DECEASED' or 'DISCONT' status")
    def test_m1_blank_if_dead(self):
        ''' If dead should be blank '''
        packet = m_packet.Packet()
        m = m_form.FormM()
        # record[]= data
        m.DECEASED = '1'
        m.CHANGEMO = '02'
        m.CHANGEDY = '28'
        m.CHANGEYR = '2008'
        m.PROTOCOL = '2'
        m.ACONSENT = '0'
        m.RECOGIM = '0'
        m.REPHYILL = '0'
        m.REREFUSE = '0'
        m.RENAVAIL = '0'
        m.RENURSE = '0'
        m.REJOIN = '0'
        m.FTLDDISC = '0'
        m.FTLDREAS = '0'
        m.FTLDREAX = '0'
        m.DISCONT = '0'
        packet.append(m)
        blanks.set_zeros_to_blanks(packet)

        self.assertEqual(packet['RENURSE'], '')
        self.assertEqual(packet['RECOGIM'], '')
        self.assertEqual(packet['REPHYILL'], '')
        self.assertEqual(packet['REREFUSE'], '')
        self.assertEqual(packet['RENAVAIL'], '')
        self.assertEqual(packet['FTLDDISC'], '')
        self.assertEqual(packet['AUTOPSY'], '')
        self.assertEqual(packet['FTLDREAS'], '')

    @unittest.skip("'0' is outside of the inclusive_range for 'FTLDREAS', 'FTLDREAX' should be left blank if FTLDREAS is filled regardless of 'DECEASED' or 'DISCONT' status")
    def test_m1_blank_if_discont(self):
        ''' If discontinued should be blank '''
        packet = m_packet.Packet()
        m = m_form.FormM()
        # record[]= data
        m.DISCONT = '1'
        m.DECEASED = '0'
        m.CHANGEMO = '02'
        m.CHANGEDY = '28'
        m.CHANGEYR = '2008'
        m.PROTOCOL = '2'
        m.ACONSENT = '0'
        m.RECOGIM = '0'
        m.REPHYILL = '0'
        m.REREFUSE = '0'
        m.RENAVAIL = '0'
        m.RENURSE = '0'
        m.REJOIN = '0'
        m.FTLDDISC = '0'
        m.FTLDREAS = '0'
        m.FTLDREAX = '0'
        packet.append(m)
        blanks.set_zeros_to_blanks(packet)

        self.assertEqual(packet['RENURSE'], '')
        self.assertEqual(packet['RECOGIM'], '')
        self.assertEqual(packet['REPHYILL'], '')
        self.assertEqual(packet['REREFUSE'], '')
        self.assertEqual(packet['RENAVAIL'], '')
        self.assertEqual(packet['FTLDDISC'], '')
        self.assertEqual(packet['AUTOPSY'], '')
        self.assertEqual(packet['FTLDREAS'], '')


def make_blank_m():
    return {
        'visitmo': '',
        'visitday': '',
        'visityr': '',
        'CHANGEMO': '',
        'CHANGEDY': '',
        'CHANGEYR': '',
        'PROTOCOL': '',
        'ACONSENT': '',
        'RECOGIM': '',
        'REPHYILL': '',
        'REREFUSE': '',
        'RENAVAIL': '',
        'RENURSE': '',
        'NURSEMO': '',
        'NURSEDY': '',
        'NURSEYR': '',
        'REJOIN': '',
        'FTLDDISC': '',
        'FTLDREAS': '',
        'FTLDREAx': '',
        'DECEASED': '',
        'DISCONT': '',
        'DEATHMO': '',
        'DEATHDY': '',
        'DEATHYR': '',
        'AUTOPSY': '',
        'DISCMO': '',
        'DISCDAY': '',
        'DISCYR': '',
        'DROPREAS': '',
    }

    def make_filled_m():
        # default dead
        return {
            'visitmo': '01',
            'visitday': '01',
            'visityr': '2000',
            'CHANGEMO': '02',
            'CHANGEDY': '03',
            'CHANGEYR': '2000',
            'PROTOCOL': '',
            'ACONSENT': '',
            'RECOGIM': '',
            'REPHYILL': '',
            'REREFUSE': '',
            'RENAVAIL': '',
            'RENURSE': '',
            'NURSEMO': '',
            'NURSEDY': '',
            'NURSEYR': '',
            'REJOIN': '',
            'FTLDDISC': '',
            'FTLDREAS': '',
            'FTLDREAx': '',
            'DECEASED': '1',
            'DISCONT': '',
            'DEATHMO': '01',
            'DEATHDY': '01',
            'DEATHYR': '2000',
            'AUTOPSY': '1',
            'DISCMO': '',
            'DISCDAY': '',
            'DISCYR': '',
            'DROPREAS': '',
        }


if __name__ == "__main__":
    unittest.main()
