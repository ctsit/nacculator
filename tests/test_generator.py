import csv
import io
import unittest

from tools import generator


class TestGenerator(unittest.TestCase):

    def test_new_format(self):
        a1_ivp_sample = """
"DORDER","ITEM","VAR","PACKET","FLDLENG","COLUMN1","COLUMN2","DTYPE","RANGE","VALUES","VAL1D","VAL2D","VAL3D","VAL4D","VAL5D","VAL6D","VAL7D","VAL8D","VAL9D","VAL10D","MISSVALS","NEWQUEST","BLANKS"
"1","1","REASON","I",1,45,45,1,"1||4","1||2||4||9","To participate in a research study","To have a clinical evaluation","Both (to participate in a research study and to have a clinical evaluation)","Unknown",,,,,,,"9","Primary reason for coming to ADC:",
        """.strip()

        expected = """
fields["REASON"] = nacc.uds3.Field(name="REASON", typename="Num", position=(45, 45), length=1, inclusive_range=(1, 4), allowable_values=['1', '2', '4', '9'], blanks=[])
        """.strip()

        reader = io.StringIO(a1_ivp_sample)
        reader = csv.DictReader(reader)
        forms = generator.generate_form("", reader)
        fields = generator.fields_to_strings(forms.fields, "")
        actual = next(fields)

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
