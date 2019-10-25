###############################################################################
# Copyright 2015-2016 University of Florida. All rights reserved.
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
        'MOMAGEO': _blanking_rule_momageo,
        'FTLDSUBT': _blanking_rule_ftldsubt,
        'LEARNED': _blanking_rule_learned,
        'ZIP': _blanking_rule_dummy,
        'DECCLMOT': _blanking_rule_dummy,
        'CRAFTDRE': _blanking_rule_dummy,
        # Neuropath skip rules
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


        'FTDCPC2F': 'Blank if form completed',
        'FTDhAIRD': 'Blank if question not answered',
        'FTDSPIT': 'Blank if question not answered',
        'FTDNOSE': 'Blank if question not answered',
        'FTDCOAGE': 'Blank if question not answered',
        'FTDCRY': 'Blank if question not answered',
        'FTDCUT': 'Blank if question not answered',
        'FTDYTRIP': 'Blank if question not answered',
        'FTDEATP': 'Blank if question not answered',
        'FTDTELLA': 'Blank if question not answered',
        'FTDOPIN': 'Blank if question not answered',
        'FTDLAUGh': 'Blank if question not answered',
        'FTDShIRT': 'Blank if question not answered',
        'FTDKEEPM': 'Blank if question not answered',
        'FTDPICKN': 'Blank if question not answered',
        'FTDOVER': 'Blank if question not answered',
        'FTDEATR': 'Blank if question not answered',
        'FTDhAIRL': 'Blank if question not answered',
        'FTDShIRW': 'Blank if question not answered',
        'FTDMOVE': 'Blank if question not answered',
        'FTDhUGS': 'Blank if question not answered',
        'FTDLOUD': 'Blank if question not answered',
        'FTDLOST': 'Blank if question not answered',
    
        'FTDWORKU': 'Blank if question not answered',
        'FTDMIST': 'Blank if question not answered',
        'FTDCRIT': 'Blank if question not answered',
        'FTDWORR': 'Blank if question not answered',
        'FTDBAD': 'Blank if question not answered',
        'FTDPOOR': 'Blank if question not answered',
        'FTDFFEAR': 'Blank if question not answered',


        'FTDFEEL': 'Blank if question not answered',
        'FTDDIFF': 'Blank if question not answered',
        'FTDSORR': 'Blank if question not answered',
        'FTDSIDE': 'Blank if question not answered',
        'FTDADVAN': 'Blank if question not answered',
        'FTDIMAG': 'Blank if question not answered',
        'FTDMISF': 'Blank if question not answered',
        'FTDWASTE': 'Blank if question not answered',
        'FTDPITY': 'Blank if question not answered',
        'FTDQTOUC': 'Blank if question not answered',
        'FTDSIDES': 'Blank if question not answered',
        'FTDSOFTh': 'Blank if question not answered',
        'FTDUPSET': 'Blank if question not answered',
        'FTDCRITI': 'Blank if question not answered',


        'FTDALTER': 'Blank if question not answered',
        'FTDEMOT': 'Blank if question not answered',
        'FTDACROS': 'Blank if question not answered',
        'FTDCONV': 'Blank if question not answered',
        'FTDINTUI': 'Blank if question not answered',
        'FTDJOKE': 'Blank if question not answered',
        'FTDIMAGP': 'Blank if question not answered',
        'FTDINAPP': 'Blank if question not answered',
        'FTDChBEh': 'Blank if question not answered',
        'FTDADBEh': 'Blank if question not answered',
        'FTDLYING': 'Blank if question not answered',
        'FTDGOODF': 'Blank if question not answered',
        'FTDREGUL': 'Blank if question not answered',



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
        'FTDMRIOS': _blanking_rule_ftld_or2,
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
        'FTDFDGOS': _blanking_rule_ftld_or3,
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
        'FTDAMYOS': _blanking_rule_ftld_or4,
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
        'FTDCBFOS': _blanking_rule_ftld_or5,

    
    }

    # single_value = re.compile(
    #     r"Blank if( Question(s?))? *\w+ (?P<key>\w+) *(?P<eq>=|ne) (?P<value>\d+)([^-]|$)")
    # range_values = re.compile(
    #     r"Blank if( Question(s?))? *\w+ (?P<key>\w+) *(?P<eq>=|ne) (?P<start>\d+)-(?P<stop>\d+)( |$)")

    single_value = re.compile(
        r"Blank if( # *\w+ (?P<key>\w+) *(?P<eq>=|ne) (?P<value>\d+)([^-]|$)")
    range_values = re.compile(
        r"Blank if( # *\w+ (?P<key>\w+) *(?P<eq>=|ne) (?P<start>\d+)-(?P<stop>\d+)( |$)")

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


def _blanking_rule_ftld_form_complete():
    # "Blank if form completed"
    return lambda packet: False

def _blanking_rule_ftld_q_noanswer():
    # "Blank if question not answered"
    return lambda packet: False

def _blanking_rule_ftld_or2():
    # Blank if either of 2 possibilities is true (= 0 (No) or = 9 (Unknown))
    return lambda packet: packet['FTDMRIFA'] in (0, 9)

def _blanking_rule_ftld_or3():
    # Blank if either of 2 possibilities is true
    return lambda packet: packet['FTDFDGFH'] in (0, 9)

def _blanking_rule_ftld_or4():
    # Blank if either of 2 possibilities is true
    return lambda packet: packet['FTDAMYVI'] in (0, 9)

def _blanking_rule_ftld_or5():
    # Blank if either of 2 possibilities is true
    return lambda packet: packet['FTDCBFVI'] in (0, 9)


def _blanking_rule_dummy():
    return lambda packet: False


def _blanking_rule_ftldsubt():
    #Blank if #14a PSP ne 1 and #14b CORT ne 1 and #14c FTLDMO ne 1 and 14d FTLDNOS ne 1
    return lambda packet: packet['PSP'] != 1 and packet['CORT'] != 1 and \
                          packet['FTLDMO'] != 1 and packet['FTLDNOS'] != 1


def _blanking_rule_learned():
    # The two rules contradict each other:
    #  - Blank if Question 2a REFERSC ne 1
    #  - Blank if Question 2a REFERSC ne 2
    # The intent appears to be "blank if REFERSC is 3, 4, 5, 6, 8, or 9", but
    # that makes 6 individual blanking rules and the maximum is 5 (BLANKS1-5).
    return lambda packet: packet['REFERSC'] in (3, 4, 5, 6, 8, 9)


def _blanking_rule_momageo():
    # Blank if Question 54MOMNEUR = 8 (N/A)
    # Blank if Question 54MOMNEUR = 9 (Unknown)
    return lambda packet: packet['MOMNEUR'] in (8, 9)

def set_zeros_to_blanks(packet):
    """ Sets specific fields to zero if they meet certain criteria """
    def set_to_blank_if_zero(*field_names):
        for field_name in field_names:
            field = packet[field_name]
            if field == 0:
                field.value = ''
    # M1 
    if packet['DECEASED'] == 1 or packet['DISCONT'] == 1:
        set_to_blank_if_zero('RENURSE','RENAVAIL','RECOGIM','REJOIN','REPHYILL',
        'REREFUSE','FTLDDISC','CHANGEMO','CHANGEDY','CHANGEYR','PROTOCOL','ACONSENT',
        'RECOGIM','REPHYILL','NURSEMO','NURSEDY','NURSEYR','FTLDREAS','FTLDREAX')
    elif packet['DECEASED'] == 1:
        #for just dead
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
