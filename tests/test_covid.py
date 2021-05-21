import unittest

from nacc.cv import builder as cv_builder


class TestCOVID(unittest.TestCase):
    # add tests in class
    def test_cv_date(self):
        """ Tests parse_date in builder.py """
        date = ['12/31/2020', '12-31-2020', '2020/12/31', '2020-12-31']
        date_parsed = ['12', '31', '2020', '12', '31', '2020', '12', '31',
                       '2020', '12', '31', '2020']
        record = make_blank_cv()
        out = []
        for x in date:
            record['visitmo'] = cv_builder.parse_date(x, 'M')
            record['visitday'] = cv_builder.parse_date(x, 'D')
            record['visityr'] = cv_builder.parse_date(x, 'Y')
            out += [str(record['visitmo']), str(record['visitday']),
                    str(record['visityr'])]
        self.assertEqual(date_parsed, out)

    def test_cv_f2_try(self):
        """ Verify the Form F2 try/catch logic with correct fields """

        record = make_blank_cv()
        record['c19t1mo'] = '01'
        record['c19t1dy'] = '01'
        record['c19t1yr'] = '2020'
        record['c19t2mo'] = '02'
        record['c19t2dy'] = '02'
        record['c19t2yr'] = '2020'
        record['c19t3mo'] = '03'
        record['c19t3dy'] = '03'
        record['c19t3yr'] = '2020'
        record['c19h1mo'] = '04'
        record['c19h1dy'] = '04'
        record['c19h1yr'] = '2020'
        record['c19h2mo'] = '05'
        record['c19h2dy'] = '05'
        record['c19h2yr'] = '2020'
        record['c19h3mo'] = '06'
        record['c19h3dy'] = '06'
        record['c19h3yr'] = '2020'

        result = cv_builder.build_cv_form(record)

        self.assertEqual(result['C19T1MO'], '01')
        self.assertEqual(result['C19T1DY'], '01')
        self.assertEqual(result['C19T1YR'], '2020')
        self.assertEqual(result['C19T2MO'], '02')
        self.assertEqual(result['C19T2DY'], '02')
        self.assertEqual(result['C19T2YR'], '2020')
        self.assertEqual(result['C19T3MO'], '03')
        self.assertEqual(result['C19T3DY'], '03')
        self.assertEqual(result['C19T3YR'], '2020')
        self.assertEqual(result['C19H1MO'], '04')
        self.assertEqual(result['C19H1DY'], '04')
        self.assertEqual(result['C19H1YR'], '2020')
        self.assertEqual(result['C19H2MO'], '05')
        self.assertEqual(result['C19H2DY'], '05')
        self.assertEqual(result['C19H2YR'], '2020')
        self.assertEqual(result['C19H3MO'], '06')
        self.assertEqual(result['C19H3DY'], '06')
        self.assertEqual(result['C19H3YR'], '2020')

    def test_cv_f2_catch(self):
        """ Verify the Form F2 try/catch logic with date as a single field """

        record = make_blank_cv()
        record['c19t1'] = '2020-01-01'
        record['c19t2'] = '2020-02-02'
        record['c19t3'] = '2020-03-03'
        record['c19h1'] = '2020-04-04'
        record['c19h2'] = '2020-05-05'
        record['c19h3'] = '2020-06-06'

        result = cv_builder.build_cv_form(record)

        self.assertEqual(result['C19T1MO'], '01')
        self.assertEqual(result['C19T1DY'], '01')
        self.assertEqual(result['C19T1YR'], '2020')
        self.assertEqual(result['C19T2MO'], '02')
        self.assertEqual(result['C19T2DY'], '02')
        self.assertEqual(result['C19T2YR'], '2020')
        self.assertEqual(result['C19T3MO'], '03')
        self.assertEqual(result['C19T3DY'], '03')
        self.assertEqual(result['C19T3YR'], '2020')
        self.assertEqual(result['C19H1MO'], '04')
        self.assertEqual(result['C19H1DY'], '04')
        self.assertEqual(result['C19H1YR'], '2020')
        self.assertEqual(result['C19H2MO'], '05')
        self.assertEqual(result['C19H2DY'], '05')
        self.assertEqual(result['C19H2YR'], '2020')
        self.assertEqual(result['C19H3MO'], '06')
        self.assertEqual(result['C19H3DY'], '06')
        self.assertEqual(result['C19H3YR'], '2020')


def make_blank_cv():
    return {
        'adcid': '2',
        'ptid': '000001',
        'date': '2020-12-12',
        'c19_initials': '',
        'c19tvis': '',
        'c19tphon': '',
        'c19ttab': '',
        'c19tlap': '',
        'c19tcomp': '',
        'c19toth': '',
        'c19tothx': '',
        'c19temai': '',
        'c19tiphn': '',
        'c19titab': '',
        'c19tilap': '',
        'c19ticom': '',
        'c19tiwed': '',
        'c19tishd': '',
        'c19tioth': '',
        'c19tiotx': '',
        'c19sympt': '',
        'c19syotx': '',
        'c19test': '2',
        'c19t1typ': '',
        'c19t2typ': '',
        'c19t3typ': '',
        'c19diag': '',
        'c19hosp': '2',
        'c19h1dys': '',
        'c19h2dys': '',
        'c19h3dys': '',
        'c19worry': '',
        'c19iso': '',
        'c19dis': '',
        'c19inc': '',
        'c19ctrl': '',
        'c19mh': '',
        'c19cmem': '',
        'c19cdep': '',
        'c19canx': '',
        'c19cbeh': '',
        'c19coth': '',
        'c19othx': '',
        'c19res': '',
        'c19coiso': '',
        'c19codis': '',
        'c19coinc': '',
        'c19coctl': '',
        'c19conn': '',
        'c19care': '',
        'c19kfam': '',
        'c19kage': '',
        'c19kact': '',
        'c19kove': '',
        'c19kfac': '',
        'c19kapp': '',
        'c19koth': '',
        'c19kothx': '',
        'c19core': '',
        'c19copre': '',
        'c19cospx': '',
    }


if __name__ == "__main__":
    unittest.main()
