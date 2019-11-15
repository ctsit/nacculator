###############################################################################
# Copyright 2015-2019 University of Florida. All rights reserved.
# This file is part of UF CTS-IT's NACCulator project.
# Use of this source code is governed by the license found in the LICENSE file.
###############################################################################

import csv
import os
import re
import sys


def convert_rule_to_python(name, rule):
    """
    Converts the text `rule` into a python function.

    The returned function accepts one argument of type `Packet`.

    Example:
        packet["FOO"] = "I should be blank!"
        packet["BAR"] = 0
        r = convert_rule_to_python("FOO", "Blank if Question 1 BAR = 0 (No)")
        if packet["FOOBAR"] != "" and r(packet):
            raise RuleError("FOO should be blank, but is not!")

    :param name: Canonical name of the field
    :param rule: Blanking rule text
    """

    special_cases = {
        'FTDCPC2F': _blanking_rule_dummy,  # "Blank if form completed"

        'FTDhAIRD': _blanking_rule_ftld_q_noanswer,
        'FTDSPIT': _blanking_rule_ftld_q_noanswer,
        'FTDNOSE': _blanking_rule_ftld_q_noanswer,
        'FTDCOAGE': _blanking_rule_ftld_q_noanswer,
        'FTDCRY': _blanking_rule_ftld_q_noanswer,
        'FTDCUT': _blanking_rule_ftld_q_noanswer,
        'FTDYTRIP': _blanking_rule_ftld_q_noanswer,
        'FTDEATP': _blanking_rule_ftld_q_noanswer,
        'FTDTELLA': _blanking_rule_ftld_q_noanswer,
        'FTDOPIN': _blanking_rule_ftld_q_noanswer,
        'FTDLAUGh': _blanking_rule_ftld_q_noanswer,
        'FTDShIRT': _blanking_rule_ftld_q_noanswer,
        'FTDKEEPM': _blanking_rule_ftld_q_noanswer,
        'FTDPICKN': _blanking_rule_ftld_q_noanswer,
        'FTDOVER': _blanking_rule_ftld_q_noanswer,
        'FTDEATR': _blanking_rule_ftld_q_noanswer,
        'FTDhAIRL': _blanking_rule_ftld_q_noanswer,
        'FTDShIRW': _blanking_rule_ftld_q_noanswer,
        'FTDMOVE': _blanking_rule_ftld_q_noanswer,
        'FTDhUGS': _blanking_rule_ftld_q_noanswer,
        'FTDLOUD': _blanking_rule_ftld_q_noanswer,
        'FTDLOST': _blanking_rule_ftld_q_noanswer,

        'FTDWORKU': _blanking_rule_dummy,
        'FTDMIST': _blanking_rule_dummy,
        'FTDCRIT': _blanking_rule_dummy,
        'FTDWORR': _blanking_rule_dummy,
        'FTDBAD': _blanking_rule_dummy,
        'FTDPOOR': _blanking_rule_dummy,
        'FTDFFEAR': _blanking_rule_dummy,
        'FTDFEEL': _blanking_rule_dummy,
        'FTDDIFF': _blanking_rule_dummy,
        'FTDSORR': _blanking_rule_dummy,
        'FTDSIDE': _blanking_rule_dummy,
        'FTDADVAN': _blanking_rule_dummy,
        'FTDIMAG': _blanking_rule_dummy,
        'FTDMISF': _blanking_rule_dummy,
        'FTDWASTE': _blanking_rule_dummy,
        'FTDPITY': _blanking_rule_dummy,
        'FTDQTOUC': _blanking_rule_dummy,
        'FTDSIDES': _blanking_rule_dummy,
        'FTDSOFTh': _blanking_rule_dummy,
        'FTDUPSET': _blanking_rule_dummy,
        'FTDCRITI': _blanking_rule_dummy,
        'FTDALTER': _blanking_rule_dummy,
        'FTDEMOT': _blanking_rule_dummy,
        'FTDACROS': _blanking_rule_dummy,
        'FTDCONV': _blanking_rule_dummy,
        'FTDINTUI': _blanking_rule_dummy,
        'FTDJOKE': _blanking_rule_dummy,
        'FTDIMAGP': _blanking_rule_dummy,
        'FTDINAPP': _blanking_rule_dummy,
        'FTDChBEh': _blanking_rule_dummy,
        'FTDADBEh': _blanking_rule_dummy,
        'FTDLYING': _blanking_rule_dummy,
        'FTDGOODF': _blanking_rule_dummy,
        'FTDREGUL': _blanking_rule_dummy,

        'FTDMRIRF': _blanking_rule_ftld_or2,
        'FTDMRILF': _blanking_rule_ftld_or2,
        'FTDMRIRT': _blanking_rule_ftld_or2,
        'FTDMRILT': _blanking_rule_ftld_or2,
        'FTDMRIRM': _blanking_rule_ftld_or2,
        'FTDMRILM': _blanking_rule_ftld_or2,
        'FTDMRIRP': _blanking_rule_ftld_or2,
        'FTDMRILP': _blanking_rule_ftld_or2,
        'FTDMRIRB': _blanking_rule_ftld_or2,
        'FTDMRILB': _blanking_rule_ftld_or2,
        'FTDMRIOB': _blanking_rule_ftld_or2,
        'FTDMRIOS': _blanking_rule_ftld_or2a,
        'FTDFDGRF': _blanking_rule_ftld_or3,
        'FTDFDGLF': _blanking_rule_ftld_or3,
        'FTDFDGRT': _blanking_rule_ftld_or3,
        'FTDFDGLT': _blanking_rule_ftld_or3,
        'FTDFDGRM': _blanking_rule_ftld_or3,
        'FTDFDGLM': _blanking_rule_ftld_or3,
        'FTDFDGRP': _blanking_rule_ftld_or3,
        'FTDFDGLP': _blanking_rule_ftld_or3,
        'FTDFDGRB': _blanking_rule_ftld_or3,
        'FTDFDGLB': _blanking_rule_ftld_or3,
        'FTDFDGOA': _blanking_rule_ftld_or3,
        'FTDFDGOS': _blanking_rule_ftld_or3a,
        'FTDAMYRF': _blanking_rule_ftld_or4,
        'FTDAMYLF': _blanking_rule_ftld_or4,
        'FTDAMYRT': _blanking_rule_ftld_or4,
        'FTDAMYLT': _blanking_rule_ftld_or4,
        'FTDAMYRM': _blanking_rule_ftld_or4,
        'FTDAMYLM': _blanking_rule_ftld_or4,
        'FTDAMYRP': _blanking_rule_ftld_or4,
        'FTDAMYLP': _blanking_rule_ftld_or4,
        'FTDAMYRB': _blanking_rule_ftld_or4,
        'FTDAMYLB': _blanking_rule_ftld_or4,
        'FTDAMYOA': _blanking_rule_ftld_or4,
        'FTDAMYOS': _blanking_rule_ftld_or4a,
        'FTDCBFRF': _blanking_rule_ftld_or5,
        'FTDCBFLF': _blanking_rule_ftld_or5,
        'FTDCBFRT': _blanking_rule_ftld_or5,
        'FTDCBFLT': _blanking_rule_ftld_or5,
        'FTDCBFRM': _blanking_rule_ftld_or5,
        'FTDCBFLM': _blanking_rule_ftld_or5,
        'FTDCBFRP': _blanking_rule_ftld_or5,
        'FTDCBFLP': _blanking_rule_ftld_or5,
        'FTDCBFRB': _blanking_rule_ftld_or5,
        'FTDCBFLB': _blanking_rule_ftld_or5,
        'FTDCBFOA': _blanking_rule_ftld_or5,
        'FTDCBFOS': _blanking_rule_ftld_or5a,

    }

    single_value = re.compile(
        r"Blank if( Question(s?))? *\w+ (?P<key>\w+)"
        r" *(?P<eq>=|ne) (?P<value>\d+)([^-]|$)")
    range_values = re.compile(
        r"Blank if( Question(s?))? *\w+ (?P<key>\w+)"
        r" *(?P<eq>=|ne) (?P<start>\d+)-(?P<stop>\d+)( |$)")
    blank_value = re.compile(
        r"Blank if( Question(s?))? *\w+ (?P<key>\w+) *(?P<eq>=|ne) blank")

    # First, check to see if the rule is a "Special Case"
    if name in special_cases:
        return special_cases[name]()

    # Then, check to see if the rule is of the within-range type
    m = range_values.match(rule)
    if m:
        return _blanking_rule_check_within_range(
            m.group('key'), m.group('eq'), m.group('start'), m.group('stop'))

    # Next, check to see if the rule is of the single-value type
    m = single_value.match(rule)
    if m:
        return _blanking_rule_check_single_value(
            m.group('key'), m.group('eq'), m.group('value'))

    # Next, check to see if the rule is of the "blank if _ = blank" type
    m = blank_value.match(rule)
    if m:
        return _blanking_rule_check_blank_value(
            m.group('key'), m.group('eq'))

    # Finally, raise an error since we do not know how to handle the rule
    raise Exception("Could not parse Blanking rule: "+name)


def extract_blanks(csvfile):
    with open(csvfile) as fp:
        reader = csv.DictReader(fp)
        blanks_fieldnames = [f for f in reader.fieldnames if 'BLANKS' in f]
        for row in reader:
            rules = '\t'.join([row[f] for f in blanks_fieldnames]).strip()
            if rules:
                yield "%s:\t%s" % (row['Data Element'], rules)


def _blanking_rule_check_single_value(key, eq, value):
    def should_be_blank(packet):
        """ Returns True if the value should be blank according to the rule """
        if '=' == eq:
            return packet[key] == value
        elif 'ne' == eq:
            return packet[key] != value
        else:
            raise ValueError("'eq' must be '=' or 'ne', not '%s'." % eq)

    return should_be_blank


def _blanking_rule_check_within_range(key, eq, start, stop):
    def should_be_blank(packet):
        """ Returns True if the value should be blank according to the rule """
        first = int(start)
        last = int(stop)+1
        if '=' == eq:
            return packet[key] in range(first, last)
        elif 'ne' == eq:
            return packet[key] not in list(range(first, last))
        else:
            raise ValueError("'eq' must be '=' or 'ne', not '%s'." % eq)

    return should_be_blank


def _blanking_rule_check_blank_value(key, eq, value=None):
    def should_be_blank(packet):
        """ Returns True if the value should be blank according to the rule """
        if '=' == eq:
            return packet[key] == value
        elif 'ne' == eq:
            return packet[key] != value
        else:
            raise ValueError("'eq' must be '=' or 'ne', not '%s'." % eq)

    return should_be_blank


def _blanking_rule_ftld_q_noanswer():
    """"Blank if question not answered" questions
    with additional blanking rules"""
    return lambda packet: packet['FTDCPC2F'] in (95, 96, 97, 98)


def _blanking_rule_ftld_or2():
    """ Blank if either of 2 possibilities is true (= 0 (No) or = 9 (Unknown))
    Along with other regular conditions """
    return lambda packet: packet['FTDMRIFA'] in (0, 9) \
        or packet['FTDIDIAG'] == 0 or packet['FTDSMRIO'] == 0


def _blanking_rule_ftld_or2a():
    """
    Blank if either of 2 possibilities is true (= 0 (No) or = 9 (Unknown))
    This rule has an additional condition compared to
    the others in this form """
    return lambda packet: packet['FTDMRIFA'] in (0, 9) \
        or packet['FTDIDIAG'] == 0 or packet['FTDSMRIO'] == 0 \
        or packet['FTDMRIOB'] != 1


def _blanking_rule_ftld_or3():
    """ See _blanking_rule_ftld_or2 for rules """
    return lambda packet: packet['FTDFDGFh'] in (0, 9) \
        or packet['FTDIDIAG'] == 0 or packet['FTDFDGPE'] == 0


def _blanking_rule_ftld_or3a():
    """ See _blanking_rule_ftld_or2a for rules """
    return lambda packet: packet['FTDFDGFh'] in (0, 9) \
        or packet['FTDIDIAG'] == 0 or packet['FTDFDGPE'] == 0 \
        or packet['FTDFDGOA'] != 1


def _blanking_rule_ftld_or4():
    """ See _blanking_rule_ftld_or2 for rules """
    return lambda packet: packet['FTDAMYVI'] in (0, 9) \
        or packet['FTDIDIAG'] == 0 or packet['FTDAMYP'] == 0


def _blanking_rule_ftld_or4a():
    """ See _blanking_rule_ftld_or2a for rules """
    return lambda packet: packet['FTDAMYVI'] in (0, 9) \
        or packet['FTDIDIAG'] == 0 or packet['FTDAMYP'] == 0 \
        or packet['FTDAMYOA'] != 1


def _blanking_rule_ftld_or5():
    """ See _blanking_rule_ftld_or2 for rules """
    return lambda packet: packet['FTDCBFVI'] in (0, 9) \
        or packet['FTDIDIAG'] == 0 or packet['FTDCBFSP'] == 0


def _blanking_rule_ftld_or5a():
    """ See _blanking_rule_ftld_or2a for rules """
    return lambda packet: packet['FTDCBFVI'] in (0, 9) \
        or packet['FTDIDIAG'] == 0 or packet['FTDCBFSP'] == 0 \
        or packet['FTDCBFOA'] != 1


def _blanking_rule_dummy():
    return lambda packet: False


def set_zeros_to_blanks(packet):
    """ Sets specific fields to zero if they meet certain criteria """
    def set_to_blank_if_zero(*field_names):
        for field_name in field_names:
            field = packet[field_name]
            if field == 0:
                field.value = ''
    # M1
    if packet['DECEASED'] == 1 or packet['DISCONT'] == 1:
        set_to_blank_if_zero(
            'RENURSE', 'RENAVAIL', 'RECOGIM', 'REJOIN',
            'REPHYILL', 'REREFUSE', 'FTLDDISC', 'CHANGEMO', 'CHANGEDY',
            'CHANGEYR', 'PROTOCOL', 'ACONSENT', 'RECOGIM', 'REPHYILL',
            'NURSEMO', 'NURSEDY', 'NURSEYR', 'FTLDREAS', 'FTLDREAX')
    elif packet['DECEASED'] == 1:
        # for just dead
        set_to_blank_if_zero('DISCONT')
    elif packet['DISCONT'] == 1:
        # for just discont
        set_to_blank_if_zero('DECEASED')


def main():
    """
    Extracts all blanking rules from all DED files in a specified directory.

    Usage:
        python blanks.py ./ded_ivp

    Note: this module is more useful as an imported module; see
    `convert_rule_to_python`.
    """
    data_dict_path = './ded_ivp'
    if len(sys.argv) > 1:
        data_dict_path = sys.argv[1]

    deds = [f for f in os.listdir(data_dict_path) if f.endswith('.csv')]
    for ded in deds:
        for rule in extract_blanks(os.path.join(data_dict_path, ded)):
            print(rule)


if __name__ == '__main__':
    main()
