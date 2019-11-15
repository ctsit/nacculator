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
        'LBDeLAGe': _blanking_rule_lbd,
        'LBDeLMeD': _blanking_rule_lbd,
        'LBDeLMD1': _blanking_rule_lbd,
        'LBDeLMD2': _blanking_rule_lbd,
        'LBHALAGe': _blanking_rule_lbd,
        'LBHALMeD': _blanking_rule_lbd,
        'LBHALMD1': _blanking_rule_lbd,
        'LBHALMD2': _blanking_rule_lbd,
        'LBANXAGe': _blanking_rule_lbd,
        'LBANXMeD': _blanking_rule_lbd,
        'LBANXMD1': _blanking_rule_lbd,
        'LBANXMD2': _blanking_rule_lbd,
        'LBAPAAGe': _blanking_rule_lbd,
        'LBAPAMeD': _blanking_rule_lbd,
        'LBAPAMD1': _blanking_rule_lbd,
        'LBAPAMD2': _blanking_rule_lbd,
    }

    single_value = re.compile(
        r"Blank if( Question(s?))? *\w+ (?P<key>\w+) *(?P<eq>=|ne)"
        r" (?P<value>\d+)([^-]|$)")
    range_values = re.compile(
        r"Blank if( Question(s?))? *\w+ (?P<key>\w+) *(?P<eq>=|ne)"
        r" (?P<start>\d+)-(?P<stop>\d+)( |$)")

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


def _blanking_rule_lbd():
    """
    All of these fields have the same blanking rule.
    Blank if Question 1 LBDeLUS, Question 2 LBHALL, Question 3 LBANXIet,
    and Question 4 LBAPAtHy = 0 (No) """
    return lambda packet: packet['LBDeLUS'] == 0 and \
        packet['LBHALL'] == 0 and \
        packet['LBANXIet'] == 0 and packet['LBAPAtHy'] == 0


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
            'RENURSE', 'RENAVAIL', 'RECOGIM', 'REJOIN', 'REPHYILL', 'REREFUSE',
            'FTLDDISC', 'CHANGEMO', 'CHANGEDY', 'CHANGEYR', 'PROTOCOL',
            'ACONSENT', 'RECOGIM', 'REPHYILL', 'NURSEMO', 'NURSEDY', 'NURSEYR',
            'FTLDREAS', 'FTLDREAX')
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
