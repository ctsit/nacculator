#!/usr/bin/env python
# coding=ascii
###############################################################################
# Copyright 2015-2016 University of Florida. All rights reserved.
# This file is part of UF CTS-IT's NACCulator project.
# Use of this source code is governed by the license found in the LICENSE file.
###############################################################################

import csv
import os
import re
import sys


class DynamicObject(object):
    """ Extension to the standard object class

    Mainly used to allow dynamic addition of members.
    """
    pass


class MethodField(str):
    """ Allows for a method to be used in str.format() like a field """

    @property
    def method(self):
        l = self.lower()
        if l in ['del']:
            l += "_"
        return l


def form_to_string(form, class_prefix=''):
    return ("class " + class_prefix + "Form{id}(nacc.uds3.FieldBag):\n".format(id=form.id) +
            indent("def __init__(self):\n" + indent(
                    "self.fields = header_fields()")))


def fields_to_strings(fields, this="self."):
    for field in fields:
        yield ("{qualifier}fields['{field.name}'] = nacc.uds3.Field("
               "name='{field.name}', "
               "typename='{field.type}', "
               "position={field.position}, "
               "length={field.length}, "
               "inclusive_range={field.inclusive_range}, "
               "allowable_values={field.allowable_codes}, "
               "blanks={field.blanks})"
               ).format(qualifier=this, field=field)


def generate(ded):
    """ Generates Python code representing each NACC Form as classes """
    with open(ded) as stream:
        reader = csv.DictReader(stream)
        form = DynamicObject()
        form.fields = []

        for record in reader:
            form.packet = record['Packet']
            form.id = record['Form ID']

            field = DynamicObject()
            field.name = MethodField(record['Data Element'])
            field.order = record['Data Order']
            field.type = record['Data Type']
            field.length = record['Data Length']
            field.position = (int(record['Column 1']), int(record['Column 2']))
            if record['RANGE1'] not in ('', '.'):
                field.inclusive_range = (int(record['RANGE1']),
                                         int(record['RANGE2']))
            else:
                field.inclusive_range = None
            field.allowable_codes = filter(None,
                                           [code for key, code in
                                            record.iteritems()
                                            if re.match('^VAL\d\d?$', str(
                                                   key)) and code != '.'])

            form.fields.append(field)
            field.blanks = [record[f] for f in reader.fieldnames
                            if 'BLANKS' in f and record[f]]

        form.fields.sort(key=lambda f: f.order)

    return form


def generate_header(ded):
    form = generate(ded)
    form.id = "Header"
    return form


def indent(text, times=1, tab='    '):
    """ Returns indented text

    Inserts times number of tabs for each line and at the beginning
    """
    if not text:
        return ''

    tabs = tab * times
    return tabs + text.replace('\n', "\n%s" % tabs)


def retab(text, newtab='    ', oldtab='\t'):
    """ Replaces all occurrences of oldtab with newtab """
    return text.replace(oldtab, newtab)

def fields_for_records(form, fields):
    formId = form.id.lower()
    print >> sys.stderr, indent("\n\n"+formId+" = fvp_forms.Form"+form.id+"()", 1)
    for field in fields:
        print >> sys.stderr, indent(formId+'{0: <10}'.format("." + field.name) + " = record['fu_"+field.name.lower()+"']", 1)
    print >> sys.stderr, indent("packet.append("+formId+")", 1)

def main():
    data_dict_path = './ded_fvp'
    corrected_dict_path = './corrected'
    header_file = 'uds3dedheader.csv'

    if len(sys.argv) > 1:
        data_dict_path = sys.argv[1]

    if len(sys.argv) > 2:
        header_file = sys.argv[2]

    deds = [f for f in os.listdir(data_dict_path)
            if f.endswith('.csv') and f != header_file]

    print "import nacc.uds3"
    print ""
    print ""
    header = generate_header(os.path.join(data_dict_path, header_file))
    print "def header_fields():"
    print indent("fields = {}")
    for field in fields_to_strings(sorted(header.fields,
                                          key=lambda fld: fld.position[1]),
                                   this=""):
        print indent(field)
    print indent("return fields")
    print ""

    for ded in deds:
        # First check to see if we have a correct version of the DED
        dedpath = os.path.join(corrected_dict_path, ded)
        if not os.path.isfile(dedpath):
            # If not, then we use the regular path
            dedpath = os.path.join(data_dict_path, ded)

        print ""
        form = generate(dedpath)
        # Uncomment this method if you want to print the templates to read records. Keys have
        # to be filled manually as per your csv header names. To seperate this from the normal
        # output, this prints to standard error
        # fields_for_records(form, sorted(form.fields, key=lambda fld: fld.position[1]))
    
        print form_to_string(form, 'FVP_')
        for field in fields_to_strings(sorted(form.fields, key=lambda fld: fld.position[1])):
            print indent(field, 2)
        print ""


if __name__ == '__main__':
    main()
