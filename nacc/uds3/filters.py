import sys
import csv
import re

import configparser

from collections import defaultdict


def validate(func):
    def read_config(config_path):
        config = configparser.ConfigParser()
        config.read(config_path)
        return config

    def get_reqs_dict(config_path):
        config = read_config(config_path)
        reqs = None
        if config.has_section(func.__name__):
            reqs = dict(config.items(func.__name__))
        return reqs

    def validate_filter(*args, **kwargs):
        config_path = args[1]
        data_dict = None
        if config_path:
            data_dict = get_reqs_dict(args[1])
        updated_args = list(args)
        updated_args[1] = data_dict
        func(*updated_args, **kwargs)

    return validate_filter


def int_or_string(value, default=-1):
    try:
        returnable = int(value)
    except ValueError:
        returnable = value or default

    return returnable


@validate
def filter_clean_ptid(input_ptr, filter_config, output_ptr):
    if filter_config:
        filepath = filter_config['filepath']
        with open(filepath, 'r') as nacc_packet_file:
            out = filter_clean_ptid_do(input_ptr, nacc_packet_file, output_ptr)
            return out
    else:
        skip_filter(input_ptr, output_ptr)
        return


def filter_clean_ptid_do(input_ptr, nacc_packet_file, output_ptr):
    redcap_packet_list = csv.DictReader(input_ptr)
    output = csv.DictWriter(output_ptr, None)
    write_headers(redcap_packet_list, output)

    # TODO: Deal with M Flag in Current_db.csv.

    completed_subjs = defaultdict(list)
    nacc_packet_list = csv.DictReader(nacc_packet_file)
    for nacc_packet in nacc_packet_list:
        if nacc_packet['Status'].lower() == "current" \
          or nacc_packet['Status'].lower() == "certified":
            nacc_subj_id = nacc_packet['Patient ID']
            nacc_visit_num = int_or_string(nacc_packet['Visit Num'])
            completed_subjs[nacc_subj_id].append(nacc_visit_num)

    for redcap_packet in redcap_packet_list:
        # if they exist in completed subjs (same id and visit num)
        # then remove them.
        rc_ptid = redcap_packet['ptid']
        rc_event = redcap_packet['redcap_event_name']

        if rc_ptid in completed_subjs:
            for nacc_ptid in completed_subjs:
                if nacc_ptid == rc_ptid:
                    if redcap_packet['visitnum']:
                        rc_visit_num = int_or_string(redcap_packet['visitnum'], -1)
                    elif nacc_packet['Packet type'] == 'M':
                        if ('milestone_5' or 'arm_1e') in rc_event:
                            rc_visit_num = 'M5'
                        elif ('milestone_4' or 'arm_1d') in rc_event:
                            rc_visit_num = 'M4'
                        elif ('milestone_3' or 'arm_1c') in rc_event:
                            rc_visit_num = 'M3'
                        elif ('milestone_2' or 'arm_1b') in rc_event:
                            rc_visit_num = 'M2'
                        elif ('milestone_1' or 'arm_1a') in rc_event:
                            rc_visit_num = 'M1'
                        else:
                            rc_visit_num = ''
                            print('Eliminated ptid : ' + rc_ptid +
                                  " Event Name : " + rc_event +
                                  " MISSING VISIT NUM", file=sys.stderr)
                            break
                    else:
                        rc_visit_num = ''
                        print('Eliminated ptid : ' + rc_ptid +
                              " Event Name : " + rc_event +
                              " MISSING VISIT NUM", file=sys.stderr)
                        continue
                    if rc_ptid in completed_subjs:
                        if rc_visit_num in completed_subjs[rc_ptid]:
                            print('Eliminated ptid : ' + rc_ptid +
                                  " Event Name : " + rc_event + " IN CURRENT",
                                  file=sys.stderr)
                            break
                else:
                    continue
                output.writerow(redcap_packet)
        else:
            output.writerow(redcap_packet)
    return output


def write_headers(reader, output):
    if output.fieldnames is None:
        # Initially empty file. Write column headers.
        output.fieldnames = reader.fieldnames
        output_header = dict((h, h) for h in reader.fieldnames)
        output.writerow(output_header)


@validate
def filter_replace_drug_id(input_ptr, filter_meta, output_ptr):
    if filter_meta:
        filter_replace_drug_id_do(input_ptr, output_ptr)
    else:
        skip_filter(input_ptr, output_ptr)
        return


def filter_replace_drug_id_do(input_ptr, output_ptr):
    reader = csv.DictReader(input_ptr)
    output = csv.DictWriter(output_ptr, None)
    write_headers(reader, output)
    for record in reader:
        count = 0
        prefixes = ['', 'fu_']
        for prefix in prefixes:
            for i in range(1, 31):
                col_name = prefix + 'drugid_' + str(i)
                if col_name in list(record.keys()):
                    col_value = record[col_name]
                    if len(col_value) > 0:
                        record[col_name] = 'd' + col_value[1:]
                        count += 1
        output.writerow(record)
        print('Processed ptid : ' + record['ptid'] + ' Updated ' + str(count) +
              ' fields.', file=sys.stderr)
    return


@validate
def filter_fix_headers(input_file, header_mapping, output_file):
    if header_mapping:
        return filter_fix_headers_do(input_file, header_mapping, output_file)
    else:
        skip_filter(input_file, output_file)
        return


def filter_fix_headers_do(input_ptr, header_dictionary, output_ptr):
    csv_reader = csv.reader(input_ptr)
    csv_writer = csv.writer(output_ptr)
    headers = next(csv_reader)
    fixed_headers = list(map(lambda header:
                             header_dictionary.get(header, header), headers))
    csv_writer.writerow(fixed_headers)
    csv_writer.writerows([row for row in csv_reader])
    return


@validate
def filter_remove_ptid(input_ptr, filter_config, output_ptr):
    if filter_config:
        return filter_remove_ptid_do(input_ptr, filter_config, output_ptr)
    else:
        skip_filter(input_ptr, output_ptr)
        return


def filter_remove_ptid_do(input_ptr, filter_diction, output_ptr):
    regex_exp = filter_diction['ptid_format']
    good_ptids_list = load_special_case_ptid('good_ptid', filter_diction)
    bad_ptids_list = load_special_case_ptid('bad_ptid', filter_diction)
    reader = csv.DictReader(input_ptr)
    output = csv.DictWriter(output_ptr, None)
    write_headers(reader, output)
    for record in reader:
        prog = re.compile(regex_exp)
        if record['ptid'] in bad_ptids_list:
            print('Removed ptid : ' + record['ptid'], file=sys.stderr)
        elif record['ptid'] in good_ptids_list:
            output.writerow(record)
        elif prog.match(record['ptid']) != None:
            output.writerow(record)
        else:
            print('Removed ptid : ' + record['ptid'], file=sys.stderr)


@validate
def filter_eliminate_empty_date(input_ptr, filter_meta, output_ptr):
    if filter_meta:
        filter_eliminate_empty_date_do(input_ptr, output_ptr)
    else:
        skip_filter(input_ptr, output_ptr)
        return


def filter_eliminate_empty_date_do(input_ptr, output_ptr):
    reader = csv.DictReader(input_ptr)
    output = csv.DictWriter(output_ptr, None)
    write_headers(reader, output)
    for record in reader:
        if _invalid_date(record):
            print(' Empty Visit Date ' + record['ptid'], file=sys.stderr)
        else:
            output.writerow(record)


def _invalid_date(record):
    return (record['visitmo'] == '' or record['visitday'] == '' or
            record['visityr'] == '')


def fill_value_of_fields(input_ptr, output_ptr, keysDict, blankCheck=False,
                         defaultCheck=False):
    reader = csv.DictReader(input_ptr)
    output = csv.DictWriter(output_ptr, None)
    write_headers(reader, output)
    for record in reader:
        count = 0
        for col_name in list(keysDict.keys()):
            if col_name in list(record.keys()):
                if blankCheck and (len(record[col_name]) > 0) and \
                  (record[col_name] != keysDict[col_name]):
                    record[col_name] = keysDict[col_name]
                    count += 1
                elif defaultCheck and len(record[col_name]) == 0:
                    record[col_name] = keysDict[col_name]
                    count += 1
        output.writerow(record)
        print('Processed ptid : ' + record['ptid'] + ' Updated ' + str(count) +
              ' fields.', file=sys.stderr)
    return


@validate
def filter_fix_visitdate(input_ptr, filter_meta, output_ptr):
    if filter_meta:
        filter_fix_visitdate_do(input_ptr, output_ptr)
    else:
        skip_filter(input_ptr, output_ptr)
        return


def filter_fix_visitdate_do(input_ptr, output_ptr):
    reader = csv.DictReader(input_ptr)
    output = csv.DictWriter(output_ptr, None)
    write_headers(reader, output)
    for record in reader:
        if record['visitnum']:
            record['visitnum'] = int_or_string(record['visitnum'])
        print('Processed ptid : ' + record['ptid'], file=sys.stderr)
        output.writerow(record)
    return


@validate
def filter_fill_default(input_ptr, filter_meta, output_ptr):
    if filter_meta:
        fill_value_of_fields(input_ptr, output_ptr, fill_default_values(filter_meta), defaultCheck=True)
    else:
        skip_filter(input_ptr, output_ptr)
        return


def fill_default_values(config):
    # This dictionary contains the keys used in the config
    try:
        adcid = config['adcid']
    except KeyError:
        adcid = ''
    fill_default_values = {'nogds': 0,
                           'adcid': adcid,
                           'formver': 3}
    return fill_default_values


@validate
def filter_update_field(input_ptr, filter_meta, output_ptr):
    if filter_meta:
        fill_value_of_fields(input_ptr, output_ptr, fill_non_blank_values(filter_meta), blankCheck=True)
    else:
        skip_filter(input_ptr, output_ptr)


def fill_non_blank_values(config):
    try:
        adcid = config['adcid']
    except KeyError:
        adcid = ''
    fill_non_blank_values = {'adcid': adcid}
    return fill_non_blank_values


def skip_filter(input_ptr, output_ptr):
    reader = csv.DictReader(input_ptr)
    output = csv.DictWriter(output_ptr, None)
    write_headers(reader, output)
    for record in reader:
        output.writerow(record)
    print('Filter skipped.', file=sys.stderr)
    return


def filter_extract_ptid(input_ptr, Ptid, visit_num, visit_type, output_ptr):
    reader = csv.DictReader(input_ptr)
    output = csv.DictWriter(output_ptr, None)
    write_headers(reader, output)

    if(visit_num and visit_type):
        filtered = [row for row in reader if
                    filter_csv_all(Ptid, visit_num, visit_type, row)]

    elif(not visit_num and visit_type):
        filtered = [row for row in reader if
                    filter_csv_vtype(Ptid, visit_type, row)]

    elif(not visit_type and visit_num):
        filtered = [row for row in reader if
                    filter_csv_vnum(Ptid, visit_num, row)]

    elif(not visit_type and not visit_num):
        filtered = [row for row in reader if
                    filter_csv_ptid(Ptid, row)]
    output.writerows(filtered)


def filter_csv_all(Ptid, visit_num, visit_type, record):
    if record['ptid'] == Ptid and record['visitnum'].lstrip("0") == visit_num \
      and (re.search(visit_type, record['redcap_event_name'])):
        return record


def filter_csv_vtype(Ptid, visit_type, record):
    if record['ptid'] == Ptid and re.search(visit_type, record['redcap_event_name']):
        return record


def filter_csv_vnum(Ptid, visit_num, record):
    if record['ptid'] == Ptid and record['visitnum'].lstrip("0") == visit_num:
        return record


def filter_csv_ptid(Ptid, record):
    if record['ptid'] == Ptid:
        return record


def load_special_case_ptid(case_name, filter_config):
    try:
        ptids_string = filter_config[case_name]
        li = list(ptids_string.split(","))
        return li
    except KeyError:
        return []
