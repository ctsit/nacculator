###############################################################################
# Copyright 2015-2019 University of Florida. All rights reserved.
# This file is part of UF CTS-IT's NACCulator project.
# Use of this source code is governed by the license found in the LICENSE file.
###############################################################################

"""Copyright 2015-2019 University of Florida

Usage: python3 tools/generator.py -h|--help
       python3 tools/generator.py <deds>
       python3 tools/generator.py <deds> <header>
       python3 tools/generator.py <deds> <header> <corrections>

Form Generator creates Python code from NACC Data Element Dictionaries stored
as CSV files.

  deds         Path to the directory containing the DED CSV files
  header       Filename of the header file within <deds>
               Defaults to "uds3dedheader.csv".
  corrections  Path to the directory containing manually corrected DED CSVs
               If unspecified, checking for corrected CSVs is skipped.

Note: the CSV versions of the DEDs are found on the NACC website with the form.
For example, UDS3 FVP Form A1 is at:
    https://www.alz.washington.edu/NONMEMBER/UDS/DOCS/VER3/uds3dedA1FVP.csv
"""

import csv
import os
import re
import sys
import typing


class DynamicObject:
    """
    Extension to the standard object to support adding members at runtime.

    ```
    foo = object()
    foo.bar = 42  # raises an AttributeError
    foo = DynamicObject()
    foo.bar = 42  # Works!
    ```
    """
    pass


class MethodField(str):
    """ Allows a method to be used in `str.format()` like a field """

    @property
    def method(self):
        string = self.lower()
        if string in ["del"]:
            string += "_"
        return string


def fields_to_strings(fields, this="self.") -> typing.Iterable[str]:
    """ Returns fields as a Python variable declaration """
    for field in fields:
        code = (
            '{qualifier}fields["{field.name}"] = nacc.uds3.Field('
            'name="{field.name}", '
            'typename="{field.type}", '
            'position={field.position}, '
            'length={field.length}, '
            'inclusive_range={field.inclusive_range}, '
            'allowable_values={field.allowable_codes}, '
            'blanks={field.blanks})'
        ).format(qualifier=this, field=field)
        yield code


def form_to_string(form: DynamicObject, class_prefix: str = "") -> str:
    """ Returns headers with "self.fields" Python tags """

    return f"""
class Form{form.id}(nacc.uds3.FieldBag):
    def __init__(self):
        self.fields = header_fields()
    """.strip()


def generate(ded: str, encoding: str = "utf-8"):
    """ Generates Python code representing each NACC Form as a class """

    try:
        with open(ded, encoding=encoding) as stream:
            reader = csv.DictReader(stream)
            form = DynamicObject()
            form.fields = []

            for record in reader:
                form.packet = record["Packet"]
                form.id = record["Form ID"]

                field = DynamicObject()
                field.name = MethodField(record["Data Element"])
                field.order = record["Data Order"]
                field.type = record["Data Type"]
                field.length = record["Data Length"]
                field.position = \
                    (int(record["Column 1"]), int(record["Column 2"]))
                if record["RANGE1"] not in ("", "."):
                    field.inclusive_range = \
                        (int(record["RANGE1"]), int(record["RANGE2"]))
                else:
                    field.inclusive_range = None

                field.allowable_codes = []
                for key, code in record.items():
                    if not code or code == ".":
                        continue
                    if not re.match(r"^VAL\d\d?$", str(key)):
                        continue
                    field.allowable_codes.append(code)

                form.fields.append(field)
                field.blanks = [record[f] for f in reader.fieldnames
                                if "BLANKS" in f and record[f]]

            form.fields.sort(key=lambda f: f.order)

    except UnicodeDecodeError as err:
        if encoding != "windows-1252":
            return generate(ded, "windows-1252")
        raise err

    return form


def indent(text, times=1, tab="    "):
    """ Returns text with times-tabs inserted at the beginning of each line """
    if not text:
        return ""

    tabs = tab * times
    return tabs + text.replace("\n", f"\n{tabs}")


def main():
    """ Program entry """

    deds_path = ""
    ded_header = "uds3dedheader.csv"
    corrected_path = ""

    if len(sys.argv) < 2:
        usage()
        sys.exit(2)

    if sys.argv[1] in ["-h", "--help"]:
        usage()
        sys.exit(0)

    if len(sys.argv) > 1:
        deds_path = sys.argv[1]

    if len(sys.argv) > 2:
        ded_header = sys.argv[2]

    if len(sys.argv) > 3:
        corrected_path = sys.argv[3]

    # Search deds_path for CSV files, excluding the ded_header.
    deds = [filename for filename in os.listdir(deds_path)
            if filename.endswith(".csv") and filename != ded_header]

    # Generate the Python module starting with the preamble, then the common
    # header fields, and finally the classes which represents the Forms.
    print("""# Generated using the NACCulator form generator tool.
import nacc.uds3


def header_fields():
    fields = {}""")

    header = generate(os.path.join(deds_path, ded_header))
    fields = sort_by_starting_position(header.fields)
    fields = fields_to_strings(fields, this="")
    for field in fields:
        print(indent(field))
    print(indent("return fields"))
    print("")

    for ded in deds:
        dedpath = os.path.join(deds_path, ded)
        if corrected_path:
            corrected = os.path.join(corrected_path, ded)
            if os.path.isfile(corrected):
                dedpath = corrected

        form = generate(dedpath)
        fields = sort_by_starting_position(form.fields)
        fields = fields_to_strings(fields)

        print("")
        print(form_to_string(form))
        for field in fields:
            print(indent(field, 2))
        print("")


def sort_by_starting_position(fields: typing.List[DynamicObject]) \
        -> typing.List[DynamicObject]:
    """ Sorts fields by their starting positions """
    return sorted(fields, key=lambda field: field.position[1])


def usage():
    """ Prints the usage text """
    print(__doc__, file=sys.stderr)


if __name__ == "__main__":
    main()
