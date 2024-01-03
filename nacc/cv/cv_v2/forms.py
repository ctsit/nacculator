# Generated using the NACCulator form generator tool.
import nacc.uds3


def header_fields_v1():
    fields = {}
    fields["PACKET"] = nacc.uds3.Field(name="PACKET", typename="Char", position=(1, 2), length=2, inclusive_range=None, allowable_values=[], blanks=[])
    fields["FORMID"] = nacc.uds3.Field(name="FORMID", typename="Char", position=(4, 6), length=3, inclusive_range=None, allowable_values=[], blanks=[])
    fields["FORMVER"] = nacc.uds3.Field(name="FORMVER", typename="Num", position=(8, 10), length=3, inclusive_range=('1', '1'), allowable_values=[], blanks=[])
    fields["ADCID"] = nacc.uds3.Field(name="ADCID", typename="Num", position=(12, 13), length=2, inclusive_range=('2', '65'), allowable_values=[], blanks=[])
    fields["PTID"] = nacc.uds3.Field(name="PTID", typename="Char", position=(15, 24), length=10, inclusive_range=None, allowable_values=[], blanks=[])
    fields["VISITMO"] = nacc.uds3.Field(name="VISITMO", typename="Num", position=(26, 27), length=2, inclusive_range=('1', '12'), allowable_values=[], blanks=[])
    fields["VISITDAY"] = nacc.uds3.Field(name="VISITDAY", typename="Num", position=(29, 30), length=2, inclusive_range=('1', '31'), allowable_values=[], blanks=[])
    fields["VISITYR"] = nacc.uds3.Field(name="VISITYR", typename="Num", position=(32, 35), length=4, inclusive_range=('2020', '2021'), allowable_values=[], blanks=[])
    fields["INITIALS"] = nacc.uds3.Field(name="INITIALS", typename="Char", position=(41, 43), length=3, inclusive_range=None, allowable_values=[], blanks=[])
    return fields


def header_fields_v2():
    fields = {}
    fields["PACKET"] = nacc.uds3.Field(name="PACKET", typename="Char", position=(1, 2), length=2, inclusive_range=None, allowable_values=[], blanks=[])
    fields["FORMID"] = nacc.uds3.Field(name="FORMID", typename="Char", position=(4, 6), length=3, inclusive_range=None, allowable_values=[], blanks=[])
    fields["FORMVER"] = nacc.uds3.Field(name="FORMVER", typename="Num", position=(8, 10), length=3, inclusive_range=('1', '1'), allowable_values=[], blanks=[])
    fields["ADCID"] = nacc.uds3.Field(name="ADCID", typename="Num", position=(12, 13), length=2, inclusive_range=('2', '65'), allowable_values=[], blanks=[])
    fields["PTID"] = nacc.uds3.Field(name="PTID", typename="Char", position=(15, 24), length=10, inclusive_range=None, allowable_values=[], blanks=[])
    fields["VISITMO"] = nacc.uds3.Field(name="VISITMO", typename="Num", position=(26, 27), length=2, inclusive_range=('1', '12'), allowable_values=[], blanks=[])
    fields["VISITDAY"] = nacc.uds3.Field(name="VISITDAY", typename="Num", position=(29, 30), length=2, inclusive_range=('1', '31'), allowable_values=[], blanks=[])
    fields["VISITYR"] = nacc.uds3.Field(name="VISITYR", typename="Num", position=(32, 35), length=4, inclusive_range=('2020', '2021'), allowable_values=[], blanks=[])
    fields["INITIALS"] = nacc.uds3.Field(name="INITIALS", typename="Char", position=(41, 43), length=3, inclusive_range=None, allowable_values=[], blanks=[])
    fields["C19CDR"] = nacc.uds3.Field(name="C19CDR", typename="Char", position=(45, 45), length=1, inclusive_range=None, allowable_values=['0', '1'], blanks=[])
    fields["C19F2CP"] = nacc.uds3.Field(name="C19F2CP", typename="Char", position=(47, 47), length=1, inclusive_range=None, allowable_values=['1', '2', '3'], blanks=[])
    fields["C19F2D"] = nacc.uds3.Field(name="C19F2D", typename="Char", position=(49, 49), length=3, inclusive_range=None, allowable_values=[], blanks=[])
    return fields


class FormF1_v1(nacc.uds3.FieldBag):
    def __init__(self):
        self.fields = header_fields_v1()
        self.fields["C19TVIS"] = nacc.uds3.Field(name="C19TVIS", typename="Num", position=(45, 45), length=1, inclusive_range=('1', '4'), allowable_values=['1', '2', '3', '4', '8'], blanks=[])
        self.fields["C19TPHON"] = nacc.uds3.Field(name="C19TPHON", typename="Num", position=(47, 47), length=1, inclusive_range=('0', '1'), allowable_values=['0', '1'], blanks=[])
        self.fields["C19TTAB"] = nacc.uds3.Field(name="C19TTAB", typename="Num", position=(49, 49), length=1, inclusive_range=('0', '1'), allowable_values=['0', '1'], blanks=[])
        self.fields["C19TLAP"] = nacc.uds3.Field(name="C19TLAP", typename="Num", position=(51, 51), length=1, inclusive_range=('0', '1'), allowable_values=['0', '1'], blanks=[])
        self.fields["C19TCOMP"] = nacc.uds3.Field(name="C19TCOMP", typename="Num", position=(53, 53), length=1, inclusive_range=('0', '1'), allowable_values=['0', '1'], blanks=[])
        self.fields["C19TOTH"] = nacc.uds3.Field(name="C19TOTH", typename="Num", position=(55, 55), length=1, inclusive_range=('0', '1'), allowable_values=['0', '1'], blanks=[])
        self.fields["C19TOTHX"] = nacc.uds3.Field(name="C19TOTHX", typename="Char", position=(57, 116), length=60, inclusive_range=None, allowable_values=[], blanks=['Blank if 2e C19TOTH is 0'])
        self.fields["C19TEMAI"] = nacc.uds3.Field(name="C19TEMAI", typename="Num", position=(118, 118), length=1, inclusive_range=('0', '1'), allowable_values=['0', '1', '8'], blanks=[])
        self.fields["C19TIPHN"] = nacc.uds3.Field(name="C19TIPHN", typename="Num", position=(120, 120), length=1, inclusive_range=('0', '1'), allowable_values=['0', '1'], blanks=[])
        self.fields["C19TITAB"] = nacc.uds3.Field(name="C19TITAB", typename="Num", position=(122, 122), length=1, inclusive_range=('0', '1'), allowable_values=['0', '1'], blanks=[])
        self.fields["C19TILAP"] = nacc.uds3.Field(name="C19TILAP", typename="Num", position=(124, 124), length=1, inclusive_range=('0', '1'), allowable_values=['0', '1'], blanks=[])
        self.fields["C19TICOM"] = nacc.uds3.Field(name="C19TICOM", typename="Num", position=(126, 126), length=1, inclusive_range=('0', '1'), allowable_values=['0', '1'], blanks=[])
        self.fields["C19TIWED"] = nacc.uds3.Field(name="C19TIWED", typename="Num", position=(128, 128), length=1, inclusive_range=('0', '1'), allowable_values=['0', '1'], blanks=[])
        self.fields["C19TISHD"] = nacc.uds3.Field(name="C19TISHD", typename="Num", position=(130, 130), length=1, inclusive_range=('0', '1'), allowable_values=['0', '1'], blanks=[])
        self.fields["C19TIOTH"] = nacc.uds3.Field(name="C19TIOTH", typename="Num", position=(132, 132), length=1, inclusive_range=('0', '1'), allowable_values=['0', '1'], blanks=[])
        self.fields["C19TIOTX"] = nacc.uds3.Field(name="C19TIOTX", typename="Char", position=(134, 193), length=60, inclusive_range=None, allowable_values=[], blanks=['Blank if 4g C19TIOTH is 0'])


class FormF2_v1(nacc.uds3.FieldBag):
    def __init__(self):
        self.fields = header_fields_v1()
        self.fields["C19SYMPT"] = nacc.uds3.Field(name="C19SYMPT", typename="Num", position=(45, 45), length=1, inclusive_range=('0', '2'), allowable_values=['0', '1', '2', '8', '9'], blanks=[])
        self.fields["C19SYOTX"] = nacc.uds3.Field(name="C19SYOTX", typename="Char", position=(47, 106), length=60, inclusive_range=None, allowable_values=[], blanks=['Blank if 1 C19SYMPT != 2 (Other)'])
        self.fields["C19TEST"] = nacc.uds3.Field(name="C19TEST", typename="Num", position=(108, 108), length=1, inclusive_range=('0', '2'), allowable_values=['0', '1', '2', '8', '9'], blanks=[])
        self.fields["C19T1MO"] = nacc.uds3.Field(name="C19T1MO", typename="Num", position=(110, 111), length=2, inclusive_range=('0', '12'), allowable_values=[], blanks=['Blank if 2 C19TEST is 0', 'Blank if 2 C19TEST is 8', 'Blank if 2 C19TEST is 9'])
        self.fields["C19T1DY"] = nacc.uds3.Field(name="C19T1DY", typename="Num", position=(113, 114), length=2, inclusive_range=('1', '31'), allowable_values=['99'], blanks=['Blank if 2 C19TEST is 0', 'Blank if 2 C19TEST is 8', 'Blank if 2 C19TEST is 9'])
        self.fields["C19T1YR"] = nacc.uds3.Field(name="C19T1YR", typename="Num", position=(116, 119), length=4, inclusive_range=('2020', '2020'), allowable_values=['2020'], blanks=['Blank if 2 C19TEST is 0', 'Blank if 2 C19TEST is 8', 'Blank if 2 C19TEST is 9'])
        self.fields["C19T1TYP"] = nacc.uds3.Field(name="C19T1TYP", typename="Num", position=(121, 121), length=1, inclusive_range=('1', '2'), allowable_values=['1', '2', '8', '9'], blanks=['Blank if 2 C19TEST is 0', 'Blank if 2 C19TEST is 8', 'Blank if 2 C19TEST is 9'])
        self.fields["C19T2MO"] = nacc.uds3.Field(name="C19T2MO", typename="Num", position=(123, 124), length=2, inclusive_range=('0', '12'), allowable_values=[], blanks=['Blank if 2 C19TEST is 0', 'Blank if 2 C19TEST is 8', 'Blank if 2 C19TEST is 9'])
        self.fields["C19T2DY"] = nacc.uds3.Field(name="C19T2DY", typename="Num", position=(126, 127), length=2, inclusive_range=('1', '31'), allowable_values=['99'], blanks=['Blank if 2 C19TEST is 0', 'Blank if 2 C19TEST is 8', 'Blank if 2 C19TEST is 9'])
        self.fields["C19T2YR"] = nacc.uds3.Field(name="C19T2YR", typename="Num", position=(129, 132), length=4, inclusive_range=('2020', '2020'), allowable_values=['2020'], blanks=['Blank if 2 C19TEST is 0', 'Blank if 2 C19TEST is 8', 'Blank if 2 C19TEST is 9'])
        self.fields["C19T2TYP"] = nacc.uds3.Field(name="C19T2TYP", typename="Num", position=(134, 134), length=1, inclusive_range=('1', '2'), allowable_values=['1', '2', '8', '9'], blanks=['Blank if 2 C19TEST is 0', 'Blank if 2 C19TEST is 8', 'Blank if 2 C19TEST is 9'])
        self.fields["C19T3MO"] = nacc.uds3.Field(name="C19T3MO", typename="Num", position=(136, 137), length=2, inclusive_range=('0', '12'), allowable_values=[], blanks=['Blank if 2 C19TEST is 0', 'Blank if 2 C19TEST is 8', 'Blank if 2 C19TEST is 9'])
        self.fields["C19T3DY"] = nacc.uds3.Field(name="C19T3DY", typename="Num", position=(139, 140), length=2, inclusive_range=('1', '31'), allowable_values=['99'], blanks=['Blank if 2 C19TEST is 0', 'Blank if 2 C19TEST is 8', 'Blank if 2 C19TEST is 9'])
        self.fields["C19T3YR"] = nacc.uds3.Field(name="C19T3YR", typename="Num", position=(142, 145), length=4, inclusive_range=('2020', '2020'), allowable_values=['2020'], blanks=['Blank if 2 C19TEST is 0', 'Blank if 2 C19TEST is 8', 'Blank if 2 C19TEST is 9'])
        self.fields["C19T3TYP"] = nacc.uds3.Field(name="C19T3TYP", typename="Num", position=(147, 147), length=1, inclusive_range=('1', '2'), allowable_values=['1', '2', '8', '9'], blanks=['Blank if 2 C19TEST is 0', 'Blank if 2 C19TEST is 8', 'Blank if 2 C19TEST is 9'])
        self.fields["C19DIAG"] = nacc.uds3.Field(name="C19DIAG", typename="Num", position=(149, 149), length=1, inclusive_range=('0', '2'), allowable_values=['0', '1', '2', '8', '9'], blanks=[])
        self.fields["C19HOSP"] = nacc.uds3.Field(name="C19HOSP", typename="Num", position=(151, 151), length=1, inclusive_range=('0', '2'), allowable_values=['0', '1', '2', '8', '9'], blanks=[])
        self.fields["C19H1MO"] = nacc.uds3.Field(name="C19H1MO", typename="Num", position=(153, 154), length=2, inclusive_range=('0', '12'), allowable_values=[], blanks=['Blank if 5 C19HOSP is 0', 'Blank if 5 C19HOSP is 8', 'Blank if 5 C19HOSP is 9'])
        self.fields["C19H1DY"] = nacc.uds3.Field(name="C19H1DY", typename="Num", position=(156, 157), length=2, inclusive_range=('1', '31'), allowable_values=['99'], blanks=['Blank if 5 C19HOSP is 0', 'Blank if 5 C19HOSP is 8', 'Blank if 5 C19HOSP is 9'])
        self.fields["C19H1YR"] = nacc.uds3.Field(name="C19H1YR", typename="Num", position=(159, 162), length=4, inclusive_range=('2020', '2020'), allowable_values=['2020'], blanks=['Blank if 5 C19HOSP is 0', 'Blank if 5 C19HOSP is 8', 'Blank if 5 C19HOSP is 9'])
        self.fields["C19H1DYS"] = nacc.uds3.Field(name="C19H1DYS", typename="Num", position=(164, 166), length=3, inclusive_range=('1', '180'), allowable_values=['1', '180'], blanks=['Blank if 5 C19HOSP is 0', 'Blank if 5 C19HOSP is 8', 'Blank if 5 C19HOSP is 9'])
        self.fields["C19H2MO"] = nacc.uds3.Field(name="C19H2MO", typename="Num", position=(168, 169), length=2, inclusive_range=('0', '12'), allowable_values=[], blanks=['Blank if 5 C19HOSP is 0', 'Blank if 5 C19HOSP is 8', 'Blank if 5 C19HOSP is 9'])
        self.fields["C19H2DY"] = nacc.uds3.Field(name="C19H2DY", typename="Num", position=(171, 172), length=2, inclusive_range=('1', '31'), allowable_values=['99'], blanks=['Blank if 5 C19HOSP is 0', 'Blank if 5 C19HOSP is 8', 'Blank if 5 C19HOSP is 9'])
        self.fields["C19H2YR"] = nacc.uds3.Field(name="C19H2YR", typename="Num", position=(174, 177), length=4, inclusive_range=('2020', '2020'), allowable_values=['2020'], blanks=['Blank if 5 C19HOSP is 0', 'Blank if 5 C19HOSP is 8', 'Blank if 5 C19HOSP is 9'])
        self.fields["C19H2DYS"] = nacc.uds3.Field(name="C19H2DYS", typename="Num", position=(179, 181), length=3, inclusive_range=('1', '180'), allowable_values=[], blanks=['Blank if 5 C19HOSP is 0', 'Blank if 5 C19HOSP is 8', 'Blank if 5 C19HOSP is 9'])
        self.fields["C19H3MO"] = nacc.uds3.Field(name="C19H3MO", typename="Num", position=(183, 184), length=2, inclusive_range=('0', '12'), allowable_values=[], blanks=['Blank if 5 C19HOSP is 0', 'Blank if 5 C19HOSP is 8', 'Blank if 5 C19HOSP is 9'])
        self.fields["C19H3DY"] = nacc.uds3.Field(name="C19H3DY", typename="Num", position=(186, 187), length=2, inclusive_range=('1', '31'), allowable_values=['99'], blanks=['Blank if 5 C19HOSP is 0', 'Blank if 5 C19HOSP is 8', 'Blank if 5 C19HOSP is 9'])
        self.fields["C19H3YR"] = nacc.uds3.Field(name="C19H3YR", typename="Num", position=(189, 192), length=4, inclusive_range=('2020', '2020'), allowable_values=['2020'], blanks=['Blank if 5 C19HOSP is 0', 'Blank if 5 C19HOSP is 8', 'Blank if 5 C19HOSP is 9'])
        self.fields["C19H3DYS"] = nacc.uds3.Field(name="C19H3DYS", typename="Num", position=(194, 196), length=3, inclusive_range=('1', '180'), allowable_values=[], blanks=['Blank if 5 C19HOSP is 0', 'Blank if 5 C19HOSP is 8', 'Blank if 5 C19HOSP is 9'])
        self.fields["C19WORRY"] = nacc.uds3.Field(name="C19WORRY", typename="Num", position=(198, 198), length=1, inclusive_range=('1', '5'), allowable_values=['1', '2', '3', '4', '5', '8'], blanks=[])
        self.fields["C19ISO"] = nacc.uds3.Field(name="C19ISO", typename="Num", position=(200, 200), length=1, inclusive_range=('1', '5'), allowable_values=['1', '2', '3', '4', '5', '8'], blanks=[])
        self.fields["C19DIS"] = nacc.uds3.Field(name="C19DIS", typename="Num", position=(202, 202), length=1, inclusive_range=('1', '5'), allowable_values=['1', '2', '3', '4', '5', '8'], blanks=[])
        self.fields["C19INC"] = nacc.uds3.Field(name="C19INC", typename="Num", position=(204, 204), length=1, inclusive_range=('0', '1'), allowable_values=['0', '1', '8', '9'], blanks=[])
        self.fields["C19CTRL"] = nacc.uds3.Field(name="C19CTRL", typename="Num", position=(206, 206), length=1, inclusive_range=('1', '5'), allowable_values=['1', '2', '3', '4', '5', '8'], blanks=[])
        self.fields["C19MH"] = nacc.uds3.Field(name="C19MH", typename="Num", position=(208, 208), length=1, inclusive_range=('1', '3'), allowable_values=['1', '2', '3', '8'], blanks=[])
        self.fields["C19CMEM"] = nacc.uds3.Field(name="C19CMEM", typename="Num", position=(210, 210), length=1, inclusive_range=('0', '1'), allowable_values=['0', '1', '8'], blanks=['Blank if 12 C19MH is 1', 'Blank if 12 C19MH is 8'])
        self.fields["C19CDEP"] = nacc.uds3.Field(name="C19CDEP", typename="Num", position=(212, 212), length=1, inclusive_range=('0', '1'), allowable_values=['0', '1', '8'], blanks=['Blank if 12 C19MH is 1', 'Blank if 12 C19MH is 8'])
        self.fields["C19CANX"] = nacc.uds3.Field(name="C19CANX", typename="Num", position=(214, 214), length=1, inclusive_range=('0', '1'), allowable_values=['0', '1', '8'], blanks=['Blank if 12 C19MH is 1', 'Blank if 12 C19MH is 8'])
        self.fields["C19CBEH"] = nacc.uds3.Field(name="C19CBEH", typename="Num", position=(216, 216), length=1, inclusive_range=('0', '1'), allowable_values=['0', '1', '8'], blanks=['Blank if 12 C19MH is 1', 'Blank if 12 C19MH is 8'])
        self.fields["C19COTH"] = nacc.uds3.Field(name="C19COTH", typename="Num", position=(218, 218), length=1, inclusive_range=('0', '1'), allowable_values=['0', '1', '8'], blanks=['Blank if 12 C19MH is 1', 'Blank if 12 C19MH is 8'])
        self.fields["C19OTHX"] = nacc.uds3.Field(name="C19OTHX", typename="Char", position=(220, 279), length=60, inclusive_range=None, allowable_values=[], blanks=['Blank if 12 C19MH is 1', 'Blank if 12 C19MH is 8', 'Blank if 13e C19COTH != 1 (Yes)'])
        self.fields["C19RES"] = nacc.uds3.Field(name="C19RES", typename="Num", position=(281, 281), length=1, inclusive_range=('1', '5'), allowable_values=['1', '2', '3', '4', '5', '8'], blanks=[])


class FormF3_v1(nacc.uds3.FieldBag):
    def __init__(self):
        self.fields = header_fields_v1()
        self.fields["C19COISO"] = nacc.uds3.Field(name="C19COISO", typename="Num", position=(45, 45), length=1, inclusive_range=('1', '5'), allowable_values=['1', '2', '3', '4', '5', '8'], blanks=[])
        self.fields["C19CODIS"] = nacc.uds3.Field(name="C19CODIS", typename="Num", position=(47, 47), length=1, inclusive_range=('1', '5'), allowable_values=['1', '2', '3', '4', '5', '8'], blanks=[])
        self.fields["C19COINC"] = nacc.uds3.Field(name="C19COINC", typename="Num", position=(49, 49), length=1, inclusive_range=('0', '1'), allowable_values=['0', '1', '8', '9'], blanks=[])
        self.fields["C19COCTL"] = nacc.uds3.Field(name="C19COCTL", typename="Num", position=(51, 51), length=1, inclusive_range=('1', '5'), allowable_values=['1', '2', '3', '4', '5', '8'], blanks=[])
        self.fields["C19CONN"] = nacc.uds3.Field(name="C19CONN", typename="Num", position=(53, 53), length=1, inclusive_range=('1', '3'), allowable_values=['1', '2', '3', '8'], blanks=[])
        self.fields["C19CARE"] = nacc.uds3.Field(name="C19CARE", typename="Num", position=(55, 55), length=1, inclusive_range=('1', '4'), allowable_values=['1', '2', '3', '4', '8'], blanks=[])
        self.fields["C19KFAM"] = nacc.uds3.Field(name="C19KFAM", typename="Num", position=(57, 57), length=1, inclusive_range=('0', '1'), allowable_values=['0', '1', '8'], blanks=[])
        self.fields["C19KAGE"] = nacc.uds3.Field(name="C19KAGE", typename="Num", position=(59, 59), length=1, inclusive_range=('0', '1'), allowable_values=['0', '1', '8'], blanks=[])
        self.fields["C19KACT"] = nacc.uds3.Field(name="C19KACT", typename="Num", position=(61, 61), length=1, inclusive_range=('0', '1'), allowable_values=['0', '1', '8'], blanks=[])
        self.fields["C19KOVE"] = nacc.uds3.Field(name="C19KOVE", typename="Num", position=(63, 63), length=1, inclusive_range=('0', '1'), allowable_values=['0', '1', '8'], blanks=[])
        self.fields["C19KFAC"] = nacc.uds3.Field(name="C19KFAC", typename="Num", position=(65, 65), length=1, inclusive_range=('0', '1'), allowable_values=['0', '1', '8'], blanks=[])
        self.fields["C19KAPP"] = nacc.uds3.Field(name="C19KAPP", typename="Num", position=(67, 67), length=1, inclusive_range=('0', '1'), allowable_values=['0', '1', '8'], blanks=[])
        self.fields["C19KOTH"] = nacc.uds3.Field(name="C19KOTH", typename="Num", position=(69, 69), length=1, inclusive_range=('0', '1'), allowable_values=['0', '1', '8'], blanks=[])
        self.fields["C19KOTHX"] = nacc.uds3.Field(name="C19KOTHX", typename="Char", position=(71, 130), length=60, inclusive_range=None, allowable_values=[], blanks=['Blank if 7 C19KOTH not = 1 (Yes)'])
        self.fields["C19CORE"] = nacc.uds3.Field(name="C19CORE", typename="Num", position=(132, 132), length=1, inclusive_range=('1', '5'), allowable_values=['1', '2', '3', '4', '5', '8'], blanks=[])
        self.fields["C19COPRE"] = nacc.uds3.Field(name="C19COPRE", typename="Num", position=(134, 134), length=1, inclusive_range=('1', '5'), allowable_values=['1', '2', '3', '4', '5', '8'], blanks=[])
        self.fields["C19COSPX"] = nacc.uds3.Field(name="C19COSPX", typename="Char", position=(136, 1159), length=1024, inclusive_range=None, allowable_values=[], blanks=[])