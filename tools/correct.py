#!/usr/bin/env python3

###############################################################################
# Copyright 2015-2016 University of Florida. All rights reserved.
# This file is part of UF CTS-IT's NACCulator project.
# Use of this source code is governed by the license found in the LICENSE file.
###############################################################################

import csv
import sys


class Fields(object):
    def __init__(self, fields):
        self.fields = list(fields)
        self.fieldnames = fields.fieldnames

    def __iter__(self):
        self._refresh()
        return iter(self.fields)

    def _find(self, name):
        index = 0
        for field in self.fields:
            if name == field['Data Element']:
                return index, field
            index += 1
        raise KeyError("Could not find data element with the name '%s'" % name)

    def _refresh(self):
        # Updates Data Order, Column 1, and Column 2 based on position
        first = self.fields[0]
        data_order = int(first['Data Order'])
        column_1 = int(first['Column 1'])
        column_2 = int(first['Column 2'])
        length = int(first['Data Length'])
        assert column_2 - column_1 + 1 == length, \
            "%s has bad lengths and columns" % first['Data Element']

        for field in self.fields[1:]:
            data_order += 1
            length = int(field['Data Length'])
            column_1 = column_2 + 2  # 2 since we have a space
            column_2 = column_1 + length - 1

            field['Data Order'] = str(data_order)
            field['Column 1'] = str(column_1)
            field['Column 2'] = str(column_2)

    def clear(self, name, attribs_values_map):
        for attrib, expected_value in attribs_values_map.items():
            self.update(name, attrib, current=expected_value, new="")

    def duplicate(self, name, new_name, details, insert=None):
        index, field = self._find(name)
        insert_at = index+1

        if insert is not None:
            offset, f = insert
            i, _ = self._find(f)
            insert_at = i+offset

        copy = dict(field)
        copy.update(details)
        copy['Data Element'] = new_name
        self.fields.insert(insert_at, copy)

    def find(self, name):
        _, field = self._find(name)
        return field

    def remove(self, name):
        index, _ = self._find(name)
        self.fields.pop(index)

    def rename(self, orig, new):
        orig_row = self.find(orig)
        orig_row['Data Element'] = new
        replace(self.fieldnames, orig, new)

    def update(self, name, attrib, current, new):
        row = self.find(name)
        assert row[attrib] == current, "%s's %s is %s, not %s" % (name, attrib,
                                                                  current, new)
        row[attrib] = new


def after(name):
    return 1, name


def before(name):
    return 0, name


def replace(list_, old, new):
    # Replaces an old value in a list with a new one
    for i, v in enumerate(list_):
        if v == old:
            list_[i] = new


def main():
    reader = csv.DictReader(sys.stdin)
    fields = Fields(reader)
    del reader

    if len(sys.argv) != 2:
        print("Please specify form using --form=...", file=sys.stderr)
        return

    if sys.argv[1] == '--form=a3':
        # IVP A3
        fields.update("SIB6AGO", 'BLANKS2',
                current='Blank if Question 6f4 SIB6NEUR = 8 (N/A)',
                new='Blank if Question 6f4 SIB6NEU = 8 (N/A)')
        fields.update("SIB6AGO", "BLANKS3",
                current='Blank if Question 6f4 SIB6NEUR = 9 (Unknown)',
                new='Blank if Question 6f4 SIB6NEU = 9 (Unknown)')
        fields.update("SIB13PDX", 'BLANKS2',
                current='Blank if Question 6m3 SIB13NEUR = 8 (N/A)',
                new='Blank if Question 6m3 SIB13NEU = 8 (N/A)')
        fields.update("SIB13PDX", "BLANKS3",
                current='Blank if Question 6m3 SIB13NEUR = 9 (Unknown)',
                new='Blank if Question 6m3 SIB13NEU = 9 (Unknown)')

        # On 2015-07-29, allowable codes for mother's and father's year of
        # birth changed to allow for earlier dates
        fields.update("MOMYOB", 'RANGE1', current='1875', new='1850')
        fields.update("DADYOB", 'RANGE1', current='1875', new='1850')

        # On 2015-04-03, in form A3, allowable codes for age of onset were
        # changed from 15-110, 999 to 0-110, 999.
        fields.update("MOMAGEO", 'RANGE1', current='15', new='0')
        fields.update("DADAGEO", 'RANGE1', current='15', new='0')
        for i in range(1, 20+1):
            fields.update("SIB"+str(i)+"AGO", 'RANGE1', current='15', new='0')
        for i in range(1, 15+1):
            fields.update("KID"+str(i)+"AGO", 'RANGE1', current='15', new='0')

        fields.update("MOMDAGE", 'RANGE1', current='15', new='0')
        fields.update("DADDAGE", 'RANGE1', current='15', new='0')
        for i in range(1, 20+1):
            fields.update("SIB"+str(i)+"AGD", 'RANGE1', current='15', new='0')
        for i in range(1, 15+1):
            fields.update("KID"+str(i)+"AGD", 'RANGE1', current='15', new='0')

    if sys.argv[1] == '--form=b4':
        # IVP B4
        fields.update("CDRLANG", 'Data Length', current='4', new='3')
    elif sys.argv[1] == '--form=b8':
        # IVP B8
        fields.rename("GAITAPRA", "SIVDFIND")
        fields.remove("CVDATAXL")
        fields.remove("CVDATAXR")
        fields.duplicate("DYSTONR", new_name="MYOCLLT", details={
            "Item #": "5k1",
            "UDS Question": "Myoclonus consistent with CBS — left side",
        })
        fields.duplicate("MYOCLLT", new_name="MYOCLRT", details={
            "Item #": "5k2",
            "UDS Question": "Myoclonus consistent with CBS — right side",
        })
    elif sys.argv[1] == '--form=d1':
        # IVP D1
        fields.rename("STROKCOG", "STROKDEC")
    elif sys.argv[1] == '--form=d2':
        # IVP D2
        fields.remove("CANCACT")
        fields.duplicate("OTHCOND", "ANTIENC", {
            "Item #": "22",

        }, insert=before("OTHCOND"))
        fields.duplicate("OTHCONDX", "ANTIENCX", {
            "Item #": "22a",
            "BLANKS1": "Blank if Question 22 ANTIENC ne 1 (Yes)"
        }, insert=after("ANTIENC"))

        fields.update("OTHCOND", "Item #", current="22", new="23")
        fields.clear("OTHCOND", {
            "MISS1": "8",
            "VAL3": "8",
            "VAL3D": "Not assessed"
        })

        fields.update("OTHCONDX", "Item #", current="22a", new="23a")
        fields.update("OTHCONDX", "BLANKS1",
                      current="Blank if Question 22 OTHCOND ne 1 (Yes)",
                      new="Blank if Question 23 OTHCOND ne 1 (Yes)")

    writer = csv.DictWriter(sys.stdout, fieldnames=fields.fieldnames)
    writer.writeheader()
    writer.writerows(fields)


if __name__ == '__main__':
    main()
