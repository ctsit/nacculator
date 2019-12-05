#!/usr/bin/env python

###############################################################################
# Copyright 2015-2019 University of Florida. All rights reserved.
# This file is part of UF CTS-IT's NACCulator project.
# Use of this source code is governed by the license found in the LICENSE file.
###############################################################################

import argparse
import csv
import re
import sys
import traceback
import typing

from nacc.uds3 import blanks as blanks_uds3
from nacc.lbd import blanks as blanks_lbd
from nacc.ftld import blanks as blanks_ftld
from nacc.csf import blanks as blanks_csf
from nacc.uds3.ivp import builder as ivp_builder
from nacc.uds3.np import builder as np_builder
from nacc.uds3.fvp import builder as fvp_builder
from nacc.uds3.m import builder as m_builder
from nacc.lbd.ivp import builder as lbd_ivp_builder
from nacc.lbd.fvp import builder as lbd_fvp_builder
from nacc.ftld.ivp import builder as ftld_ivp_builder
from nacc.ftld.fvp import builder as ftld_fvp_builder
from nacc.csf import builder as csf_builder
from nacc.uds3 import filters
from nacc.uds3 import packet as uds3_packet
from nacc.uds3 import Field


def check_blanks(packet: uds3_packet.Packet, options: argparse.Namespace) \
        -> typing.List:
    """
    Parses rules for when each field should be blank and then checks them
    """
    warnings = []

    for form in packet:
        # Find all fields that:
        #   1) have blanking rules; and
        #   2) aren't blank.
        for field in [f for f in form.fields.values()
                      if f.blanks and not empty(f)]:

            for rule in field.blanks:
                if not options.lbd and not options.ftld and not options.csf:
                    r = blanks_uds3.convert_rule_to_python(field.name, rule)
                    if r(packet):
                        warnings.append(
                            "'%s' is '%s' with length '%s', but should be"
                            " blank: '%s'." %
                            (field.name, field.value, len(field.value), rule))

                if options.lbd:
                    t = blanks_lbd.convert_rule_to_python(field.name, rule)
                    if t(packet):
                        warnings.append(
                            "'%s' is '%s' with length '%s', but should be"
                            " blank: '%s'." %
                            (field.name, field.value, len(field.value), rule))

                if options.ftld:
                    s = blanks_ftld.convert_rule_to_python(field.name, rule)
                    if s(packet):
                        warnings.append(
                            "'%s' is '%s' with length '%s', but should be"
                            " blank: '%s'." %
                            (field.name, field.value, len(field.value), rule))

                if options.csf:
                    q = blanks_csf.convert_rule_to_python(field.name, rule)
                    if q(packet):
                        warnings.append(
                            "'%s' is '%s' with length '%s', but should be"
                            " blank: '%s'." %
                            (field.name, field.value, len(field.value), rule))
    return warnings


def check_characters(packet: uds3_packet.Packet) -> typing.List:
    """
    Checks typename="Char" fields for any of 4 special characters: & ' " %
    If these characters are found, throws an error and skips the ptid
    """
    warnings = []

    for form in packet:
        # Find all fields that have any of the forbidden characters, and
        #   figure out which characters are present in the string.
        # If they are found, append an error to our error file
        #   and skip the PTID
        for field in [f for f in form.fields.values()]:
            if field.typename == "Char":
                incompatible = check_for_bad_characters(field)

                if incompatible:
                    character = " ".join(incompatible)
                    warnings.append(
                        '\'%s\' is \'%s\', which has invalid character(s) %s .'
                        ' This field can have any text or numbers, but cannot'
                        ' include single quotes \', double quotes \",'
                        ' ampersands & or percentage signs %% ' %
                        (field.name, field.value, character))

    return warnings


def check_for_bad_characters(field: Field) -> typing.List:
    """
    Searches the flagged fields for the special characters
    and tallies up all instances of each character
    """
    incompatible = []

    text = field.value
    chars = ["'", '"', '&', '%']

    if any((c in chars) for c in text):
        quote = re.search("'", text)
        num_quote = text.count("'")
        dquote = re.search('"', text)
        num_dquote = text.count('"')
        amp = re.search('&', text)
        num_amp = text.count("&")
        percent = re.search('%', text)
        num_percent = text.count("%")

        incompatible = []
        if quote:
            quote = "'"
            incompatible.append(quote + " (%s)" % num_quote)
        if dquote:
            dquote = '"'
            incompatible.append(dquote + " (%s)" % num_dquote)
        if amp:
            amp = '&'
            incompatible.append(amp + " (%s)" % num_amp)
        if percent:
            percent = '%'
            incompatible.append(percent + " (%s)" % num_percent)

    return incompatible


def check_single_select(packet: uds3_packet.Packet):
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
    true_values = [v for v in values if v == value_to_check]
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


def convert(fp, options, out=sys.stdout, err=sys.stderr):
    """Converts data in REDCap's CSV format to NACC's fixed-width format."""
    reader = csv.DictReader(fp)
    for record in reader:
        print("[START] ptid : " + str(record['ptid']), file=err)
        try:
            if options.lbd and options.ivp:
                packet = lbd_ivp_builder.build_uds3_lbd_ivp_form(record)
            elif options.lbd and options.fvp:
                packet = lbd_fvp_builder.build_uds3_lbd_fvp_form(record)
            elif options.ftld and options.ivp:
                packet = ftld_ivp_builder.build_uds3_ftld_ivp_form(record)
            elif options.ftld and options.fvp:
                packet = ftld_fvp_builder.build_uds3_ftld_fvp_form(record)
            elif options.csf:
                packet = csf_builder.build_uds3_csf_form(record)
            elif options.ivp:
                packet = ivp_builder.build_uds3_ivp_form(record)
            elif options.np:
                packet = np_builder.build_uds3_np_form(record)
            elif options.fvp:
                packet = fvp_builder.build_uds3_fvp_form(record)
            elif options.m:
                packet = m_builder.build_uds3_m_form(record)

        except Exception:
            if 'ptid' in record:
                print("[SKIP] Error for ptid : " + str(record['ptid']),
                      file=err)
            traceback.print_exc()
            continue

        if not options.np and not options.m and not options.lbd and not options.ftld and not options.csf:
            set_blanks_to_zero(packet)

        if options.m:
            blanks_uds3.set_zeros_to_blanks(packet)

        warnings = []
        try:
            warnings += check_blanks(packet, options)
        except KeyError:
            print("[SKIP] Error for ptid : " + str(record['ptid']), file=err)
            traceback.print_exc()
            continue

        try:
            warnings += check_characters(packet)
            if warnings:
                print("[SKIP] Error for ptid : " + str(record['ptid']),
                      file=err)
                warn = "\n".join(map(str, warnings))
                warn = warn.replace("\\", "")
                print(warn, file=err)
                continue
        except KeyError:
            print("[SKIP] Error for ptid : " + str(record['ptid']), file=err)
            traceback.print_exc()
            continue

        if not options.np and not options.m and not options.lbd and not options.ftld and not options.csf:
            warnings += check_single_select(packet)

        for form in packet:

            try:
                print(form, file=out)
            except AssertionError:
                print("[SKIP] Error for ptid : " + str(record['ptid']),
                      file=err)
                traceback.print_exc()
                continue


filters_names = {
    'cleanPtid': 'clean_ptid',
    'replaceDrugId': 'replace_drug_id',
    'fixHeaders': 'fix_headers',
    'fillDefault': 'fill_default',
    'updateField': 'update_field',
    'removePtid': 'remove_ptid',
    'removeDateRecord': 'eliminate_empty_date',
    'getPtid': 'extract_ptid'}


def parse_args(args=None):
    parser = argparse.ArgumentParser(
        description='Process redcap form output to nacculator.')

    option_group = parser.add_mutually_exclusive_group()
    option_group.add_argument(
        '-fvp', action='store_true', dest='fvp',
        help='Set this flag to process as fvp data')
    option_group.add_argument(
        '-ivp', action='store_true', dest='ivp',
        help='Set this flag to process as ivp data')
    option_group.add_argument(
        '-np', action='store_true', dest='np',
        help='Set this flag to process as np data')
    option_group.add_argument(
        '-m', action='store_true', dest='m',
        help='Set this flag to process as m data')
    option_group.add_argument(
        '-f', '--filter', action='store', dest='filter',
        choices=list(filters_names.keys()),
        help='Set this flag to process the filter')

    parser.add_argument(
        '-lbd', action='store_true', dest='lbd',
        help='Set this flag to process as Lewy Body Dementia data')
    parser.add_argument(
        '-ftld', action='store_true', dest='ftld',
        help='Set this flag to process as Frontotemporal Lobar'
        ' Degeneration data')
    parser.add_argument(
        '-csf', action='store_true', dest='csf',
        help='Set this flag to process as Cerebrospinal Fluid data')
    parser.add_argument(
        '-file', action='store', dest='file',
        help='Path of the csv file to be processed.')
    parser.add_argument(
        '-meta', action='store', dest='filter_meta',
        help='Input file for the filter metadata (in case -filter is used)')
    parser.add_argument(
        '-ptid', action='store', dest='ptid',
        help='Ptid for which you need the records')
    parser.add_argument(
        '-vnum', action='store', dest='vnum',
        help='Ptid for which you need the records')
    parser.add_argument(
        '-vtype', action='store', dest='vtype',
        help='Ptid for which you need the records')

    options = parser.parse_args(args)
    # Defaults to processing of ivp.
    # TODO this can be changed in future to process fvp by default.
    if not (options.ivp or options.fvp or options.np or options.m or options.csf or options.filter):
        options.ivp = True

    return options


def main():
    """
    Reads a REDCap exported CSV, data file, then prints it out in NACC's format
    """
    options = parse_args()

    fp = sys.stdin if options.file is None else open(options.file, 'r')

    # Place holder for future. May need to output to a specific file in future.
    output = sys.stdout

    if options.filter:
        if options.filter == "getPtid":
            filters.filter_extract_ptid(
                fp, options.ptid, options.vnum, options.vtype, output)
        else:
            filter_method = 'filter_' + filters_names[options.filter]
            filter_func = getattr(filters, filter_method)
            filter_func(fp, options.filter_meta, output)
    else:
        convert(fp, options)


if __name__ == '__main__':
    main()
