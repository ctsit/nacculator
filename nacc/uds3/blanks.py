###############################################################################
# Copyright 2015-2023 University of Florida. All rights reserved.
# This file is part of UF CTS-IT's NACCulator project.
# Use of this source code is governed by the license found in the LICENSE file.
###############################################################################

import csv
import os
import re
import sys


def convert_rule_to_python(name: str, rule: str, options) -> bool:
    """
    Converts the "rule" string into a python function using "blanks" from the
    associated forms.py file. The fieldname being checked here is "name".

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
        'FTLDSUBT': _blanking_rule_ftldsubt,
        'LEARNED': _blanking_rule_learned,
        'ZIP': _blanking_rule_dummy,
        'DECCLMOT': _blanking_rule_dummy,
        'CRAFTDRE': _blanking_rule_dummy,
        # Account for the Neuropath skip rules
        'NPINF': _blanking_rule_dummy,
        'NPHEMO': _blanking_rule_dummy,
        'NPOLD': _blanking_rule_dummy,
        'NPOLDD': _blanking_rule_dummy,
        'NPFTDTAU': _blanking_rule_dummy,
        'NPOFTD': _blanking_rule_dummy,
        'NPNEC': _blanking_rule_dummy,
        'NPPATH': _blanking_rule_dummy,
        'NPPATHO': _blanking_rule_dummy,
        'NPPATH2': _blanking_rule_dummy,
        'NPPATH3': _blanking_rule_dummy,
        'NPPATH6': _blanking_rule_dummy,
        'NPPATH7': _blanking_rule_dummy,
        'NPPATH4': _blanking_rule_dummy,
        'NPPATH5': _blanking_rule_dummy,
        'NPPATH8': _blanking_rule_dummy,
        'NPPATH9': _blanking_rule_dummy,
        'NPPATH10': _blanking_rule_dummy,
        'NPPATH11': _blanking_rule_dummy,
        # TFP 3.2 skip rules
        'TELMILE': _blanking_rule_telmile,
    }

    if options.tip:
        special_cases_tip = {
            'INVISITS': _blanking_rule_tip_inlivwth,
            'INCALLS': _blanking_rule_tip_inlivwth,
            'MOCALANX': _blanking_rule_tip_mocalanx,
            'NPSYLANX': _blanking_rule_tip_npsylanx,
            'CRAFTURS': _blanking_rule_tip_crafturs,
            'REY1INT': _blanking_rule_tip_rey1rec,
            'REY2REC': _blanking_rule_tip_rey1rec,
            'REY2INT': _blanking_rule_tip_rey1rec,
            'REY3REC': _blanking_rule_tip_rey1rec,
            'REY3INT': _blanking_rule_tip_rey1rec,
            'REY4REC': _blanking_rule_tip_rey1rec,
            'REY4INT': _blanking_rule_tip_rey1rec,
            'REY5REC': _blanking_rule_tip_rey1rec,
            'REY5INT': _blanking_rule_tip_rey1rec,
            'REY6REC': _blanking_rule_tip_rey1rec,
            'REY6INT': _blanking_rule_tip_rey1rec,
            'DIGFORSL': blanking_rule_tip_digforsl,
            'DIGBACLS': blanking_rule_tip_digbacls,
            'OTRLARR': blanking_rule_tip_otraila,
            'OTRLALI': blanking_rule_tip_otraila,
            'OTRLBRR': blanking_rule_tip_otrailb,
            'OTRLBLI': blanking_rule_tip_otrailb,
            'CRAFTDRE': blanking_rule_tip_craftdvr,
            'CRAFTDTI': blanking_rule_tip_craftdvr,
            'CRAFTCUE': blanking_rule_tip_craftdvr,
            'UDSVERFN': blanking_rule_tip_udsverfc,
            'UDSVERNF': blanking_rule_tip_udsverfc,
            'UDSVERLC': blanking_rule_tip_udsverfc,
            'UDSVERLR': blanking_rule_tip_udsverlc,
            'UDSVERLN': blanking_rule_tip_udsverlc,
            'UDSVERTN': blanking_rule_tip_udsverlc,
            'UDSVERTE': blanking_rule_tip_udsverlc,
            'UDSVERTI': blanking_rule_tip_udsverlc,
            'REYDINT': blanking_rule_tip_reydrec,
            'REYTCOR': blanking_rule_tip_reydrec,
            'REYFPOS': blanking_rule_tip_reydrec,
            'RESPOTHX': blanking_rule_tip_respothx,
        }
        special_cases.update(special_cases_tip)


    # The regex needs to have a lot of flexibility due to inconsistent naming
    # conventions in our source, NACC's Data Element Dictionary (as seen in
    # forms.py)
    single_value = re.compile(
        r"Blank if( Question(s?))? (#?)*\w+\.? (?P<key>\w+) *(?P<eq>=|ne)"
        r" (?P<value>\d+)([^-]|$)")
    range_values = re.compile(
        r"Blank if( Question(s?))? (#?)*\w+\.? (?P<key>\w+) *(?P<eq>=|ne)"
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


def _blanking_rule_dummy():
    return lambda packet: False


def _blanking_rule_ftldsubt():
    """
    Blank if #14a PSP ne 1 and #14b CORT ne 1 and #14c FTLDMO ne 1 and
    14d FTLDNOS ne 1
    """
    return lambda packet: packet['PSP'] != 1 and packet['CORT'] != 1 and \
                          packet['FTLDMO'] != 1 and packet['FTLDNOS'] != 1


def _blanking_rule_learned():
    """
    The two rules contradict each other:
     - Blank if Question 2a REFERSC ne 1
     - Blank if Question 2a REFERSC ne 2

    The intent appears to be "blank if REFERSC is 3, 4, 5, 6, 8, or 9", but
    that makes 6 individual blanking rules and the maximum is 5 (BLANKS1-5).
    """
    return lambda packet: packet['REFERSC'] in (3, 4, 5, 6, 8, 9)


def _blanking_rule_telmile():
    """
    'Blank if Question 3 TELINPER = 1 (Yes)'
    'Blank if Question 3 TELINPER = 9 (Unknown)'
    'Blank if this is the first telephone packet submitted for the subject.'
    """
    return lambda packet: packet['TELINPER'] in (1, 9)


def _blanking_rule_tip_inlivwth():
    """
    This blanking rule is incorrect in the TIP data element dictionary. It
    reads: 'Blank if #9. INLIVWTH ne 1 (Yes)' but it should be the opposite:
    'Blank if Question 10 INLIVWTH = 1 (Yes)'
    """
    return lambda packet: packet['INLIVWTH'] == 1


def _blanking_rule_tip_mocalanx():
    """
    'Blank if 1a MOCACOMP = 0 (No) or 1b MOCALAN = English (1) or Spanish (2)'
    """
    return lambda packet: packet['MOCACOMP'] == 0 or \
                          packet['MOCALAN'] in (1, 2)


def _blanking_rule_tip_npsylanx():
    """
    'Blank if 2a NPSYLAN = English (1) or Spanish (2)'
    """
    return lambda packet: packet['NPSYLAN'] in (1, 2)


def _blanking_rule_tip_crafturs():
    """
    'Blank if 3a CRAFTVRS = 95 - 98'
    """
    return lambda packet: packet['CRAFTVRS'] in (95, 96, 97, 98)


def _blanking_rule_tip_rey1rec():
    """
    'Blank if 4a REY1REC 88, 95-98'
    """
    return lambda packet: packet['REY1REC'] in (88, 95, 96, 97, 98)


def blanking_rule_tip_digforsl():
    """
    Blank if 5a DIGFORCT = 95 - 98
    """
    return lambda packet: packet['DIGFORCT'] in (95, 96, 97, 98)


def blanking_rule_tip_digbacls():
    """
    'Blank if 6a DIGBACCT = 95 - 98'
    """
    return lambda packet: packet['DIGBACCT'] in (95, 96, 97, 98)


def blanking_rule_tip_otraila():
    """
    'Blank if 7a OTRAILA = 888, 995 - 998'
    """
    return lambda packet: packet['OTRAILA'] in (888, 995, 996, 997, 998)


def blanking_rule_tip_otrailb():
    """
    'Blank if 7b OTRAILB = 888, 995 - 998'
    """
    return lambda packet: packet['OTRAILB'] in (888, 995, 996, 997, 998)


def blanking_rule_tip_craftdvr():
    """
    'Blank if 8a CRAFTDVR is 95 - 98'
    """
    return lambda packet: packet['CRAFTDVR'] in (95, 96, 97, 98)


def blanking_rule_tip_udsverfc():
    """
    'Blank if 10a UDSVERFC is 95 - 98'
    """
    return lambda packet: packet['UDSVERFC'] in (95, 96, 97, 98)


def blanking_rule_tip_udsverlc():
    """
    'Blank if 10d UDSVERLC is 95 - 98'
    """
    return lambda packet: packet['UDSVERLC'] in (95, 96, 97, 98)


def blanking_rule_tip_reydrec():
    """
    'Blank if 11a REYDREC is 88, 95-98'
    """
    return lambda packet: packet['REYDREC'] in (88, 95, 96, 97, 98)


def blanking_rule_tip_respothx():
    """
    'Blank if 14a RESPVAL = 1 or RESPOTH ne 1'
    """
    return lambda packet: packet['RESPVAL'] == 1 or \
                          packet['RESPOTH'] != 0


def set_zeros_to_blanks(packet):
    """ Sets specific fields to zero if they meet certain criteria """
    def set_to_blank_if_zero(*field_names):
        for field_name in field_names:
            field = packet[field_name]
            if field == 0:
                field.value = ''
    # M1
    try:
        if packet['DECEASED'] == 1 or packet['DISCONT'] == 1:
            set_to_blank_if_zero(
                'RENURSE', 'RENAVAIL', 'RECOGIM', 'REJOIN', 'REPHYILL',
                'REREFUSE', 'FTLDDISC', 'CHANGEMO', 'CHANGEDY', 'CHANGEYR',
                'PROTOCOL', 'ACONSENT', 'RECOGIM', 'REPHYILL', 'NURSEMO',
                'NURSEDY', 'NURSEYR', 'FTLDREAS', 'FTLDREAX')
        elif packet['DECEASED'] == 1:
            # for just dead
            set_to_blank_if_zero('DISCONT')
        elif packet['DISCONT'] == 1:
            # for just discont
            set_to_blank_if_zero('DECEASED')
    except KeyError:
        pass
    # TFP
    try:
        if packet['RESPVAL'] == 1:
            set_to_blank_if_zero(
                'RESPHEAR', 'RESPDIST', 'RESPINTR', 'RESPDISN', 'RESPFATG',
                'RESPEMOT', 'RESPASST', 'RESPOTH')
    except KeyError:
        pass


def main():
    """
    This "blanks" file concerns the UDS3 packet types- IVP, FVP, TIP, TFP,
    and the Milestone and Neuropath forms.

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
