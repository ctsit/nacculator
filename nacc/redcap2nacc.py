#!/usr/bin/env python

###############################################################################
# Copyright 2015-2016 University of Florida. All rights reserved.
# This file is part of UF CTS-IT's NACCulator project.
# Use of this source code is governed by the license found in the LICENSE file.
###############################################################################

import csv
import re
import sys
import argparse
import traceback

from nacc.uds3 import blanks
from nacc.uds3.ivp import builder as ivp_builder
from nacc.uds3.np import builder as np_builder
from nacc.uds3.fvp import builder as fvp_builder
from nacc.uds3 import filters

def check_blanks(packet):
    """
    Parses rules for when each field should be blank and then checks them
    """
    pattern = re.compile(r"Blank if Question \d+ (\w+) (ne|=) (\d+)")
    warnings = []

    for form in packet:
        # Find all fields that:
        #   1) have blanking rules; and
        #   2) aren't blank.
        for field in [f for f in form.fields.itervalues()
                      if f.blanks and not empty(f)]:

            for rule in field.blanks:
                r = blanks.convert_rule_to_python(field.name, rule)
                if r(packet):
                    warnings.append(
                        "'%s' is '%s' with length '%s', but should be blank: '%s'." %
                        (field.name, field.value, len(field.value), rule))

    return warnings


def check_single_select(packet):
    """ Checks the values of sets of interdependent questions

    There are some sets of questions which should function like an HTML radio
    button group in that only one of them should be selected. However, because
    of the manner in which they were implemented in REDCap, the values need to
    be double-checked to ensure at most one in a given set has the real answer.
    """
    warnings = list()

    # D1 4
    fields = ('AMNDEM', 'PCA', 'PPASYN', 'FTDSYN', 'LBDSYN', 'NAMNDEM')
    if not exclusive(packet, fields):
        warnings.append('For Form D1, Question 4, there is unexpectedly more '
                        'than one syndrome indicated as "Present".')

    # D1 5
    fields = ('MCIAMEM', 'MCIAPLUS', 'MCINON1', 'MCINON2', 'IMPNOMCI')
    if not exclusive(packet, fields):
        warnings.append('For Form D1, Question 5, there is unexpectedly more '
                        'than one syndrome indicated as "Present".')

    # D1 11-39
    fields = ('ALZDISIF', 'LBDIF', 'MSAIF', 'PSPIF', 'CORTIF', 'FTLDMOIF',
              'FTLDNOIF', 'FTLDSUBX', 'CVDIF', 'ESSTREIF', 'DOWNSIF', 'HUNTIF',
              'PRIONIF', 'BRNINJIF', 'HYCEPHIF', 'EPILEPIF', 'NEOPIF', 'HIVIF',
              'OTHCOGIF', 'DEPIF', 'BIPOLDIF', 'SCHIZOIF', 'ANXIETIF',
              'DELIRIF', 'PTSDDXIF', 'OTHPSYIF', 'ALCDEMIF', 'IMPSUBIF',
              'DYSILLIF', 'MEDSIF', 'COGOTHIF', 'COGOTH2F', 'COGOTH3F')
    if not exclusive(packet, fields):
        warnings.append('For Form D1, Questions 11-39, there is unexpectedly '
                        'more than one Primary cause selected.')

    return warnings


def empty(field):
    """ Helper function that returns True if a field's value is empty """
    return field.value.strip() == ""


def exclusive(packet, fields, value_to_check=1):
    """ Returns True iff, for a set of fields, only one of field is set. """
    values = [packet[f].value for f in fields]
    true_values = filter(lambda v: v == value_to_check, values)
    return len(true_values) <= 1


def set_blanks_to_zero(packet):
    """ Sets specific fields to zero if they meet certain criteria """
    def set_to_zero_if_blank(*field_names):
        for field_name in field_names:
            field = packet[field_name]
            if empty(field):
                field.value = 0

    # B8 2.
    if packet['PARKSIGN'] == 1:
        set_to_zero_if_blank(
            'RESTTRL', 'RESTTRR', 'SLOWINGL', 'SLOWINGR', 'RIGIDL', 'RIGIDR',
            'BRADY', 'PARKGAIT', 'POSTINST')

    # B8 3.
    if packet['CVDSIGNS'] == 1:
        set_to_zero_if_blank('CORTDEF', 'SIVDFIND', 'CVDMOTL', 'CVDMOTR',
                             'CORTVISL', 'CORTVISR', 'SOMATL', 'SOMATR')

    # B8 5.
    if packet['PSPCBS'] == 1:
        set_to_zero_if_blank(
            'PSPCBS', 'EYEPSP', 'DYSPSP', 'AXIALPSP', 'GAITPSP', 'APRAXSP',
            'APRAXL', 'APRAXR', 'CORTSENL', 'CORTSENR', 'ATAXL', 'ATAXR',
            'ALIENLML', 'ALIENLMR', 'DYSTONL', 'DYSTONR')

    # D1 4.
    if packet['DEMENTED'] == 1:
        set_to_zero_if_blank(
                'AMNDEM', 'PCA', 'PPASYN', 'FTDSYN', 'LBDSYN', 'NAMNDEM')

    # D1 5.
    if packet['DEMENTED'] == 0:
        set_to_zero_if_blank(
                'MCIAMEM', 'MCIAPLUS', 'MCINON1', 'MCINON2', 'IMPNOMCI')

    # D1 11-39.
    set_to_zero_if_blank(
        'ALZDIS', 'LBDIS', 'MSA', 'PSP', 'CORT', 'FTLDMO', 'FTLDNOS', 'CVD',
        'ESSTREM', 'DOWNS', 'HUNT', 'PRION', 'BRNINJ', 'HYCEPH', 'EPILEP',
        'NEOP', 'HIV', 'OTHCOG', 'DEP', 'BIPOLDX', 'SCHIZOP', 'ANXIET',
        'DELIR', 'PTSDDX', 'OTHPSY', 'ALCDEM', 'IMPSUB', 'DYSILL', 'MEDS',
        'COGOTH', 'COGOTH2', 'COGOTH3')

    # D2 11.
    if packet['ARTH'] == 1:
        set_to_zero_if_blank('ARTUPEX', 'ARTLOEX', 'ARTSPIN', 'ARTUNKN')

def main():
    """
    Reads a REDCap exported CSV, data file, then prints it out in NACC's format
    """
    parser = argparse.ArgumentParser(description='Process redcap form output to nacculator.')

    filters_names = { 'cleanPtid' : 'clean_ptid',
                'replaceDrugId' : 'replace_drug_id',
                'fixC1S' : 'fix_c1s',
                'fillDefault' : 'fill_default',
                'updateField' : 'update_field'}

    option_group = parser.add_mutually_exclusive_group()
    option_group.add_argument('-fvp', action='store_true', dest='fvp', help='Set this flag to process as fvp data')
    option_group.add_argument('-ivp', action='store_true', dest='ivp', help='Set this flag to process as ivp data')
    option_group.add_argument('-np', action='store_true', dest='np', help='Set this flag to process as np data')
    option_group.add_argument('-f', '--filter', action='store', dest='filter', choices=filters_names.keys(), help='Set this flag to process the filter')

    parser.add_argument('-file', action='store', dest='file', help='Path of the csv file to be processed.')
    parser.add_argument('-meta', action='store', dest='filter_meta', help='Input file for the filter metadata (in case -filter is used)')

    options = parser.parse_args()

    # Defaults to processing of ivp.
    # TODO this can be changed in future to process fvp by default.
    if not (options.ivp or options.fvp or options.np or options.filter):
        options.ivp = True

    fp = sys.stdin if options.file == None else open(options.file, 'r')

    # Place holder for future. May need to output to a specific file in future.
    output = sys.stdout

    if options.filter:
        filter_method = getattr(filters, 'filter_' + filters_names[options.filter])
        filter_method(fp, options.filter_meta, output)
    else:
        reader = csv.DictReader(fp)
        for record in reader:    
            print >> sys.stderr, "[START] ptid : " + str(record['ptid'])
            try:
                if options.ivp:
                    packet = ivp_builder.build_uds3_ivp_form(record)    
                elif options.np:
                    packet = np_builder.build_uds3_np_form(record)
                elif options.fvp:
                    packet = fvp_builder.build_uds3_fvp_form(record)
            except Exception, exp:
                if 'ptid' in record:
                    print >> sys.stderr, "[SKIP] Error for ptid : " + str(record['ptid'])
                traceback.print_exc()
                continue

            if not options.np:
                set_blanks_to_zero(packet)

            warnings = []
            warnings += check_blanks(packet)

            if not options.np:
                warnings += check_single_select(packet)

            if warnings:
                print >> sys.stderr, "\n".join(warnings)

            for form in packet:
                print form

if __name__ == '__main__':
    main()