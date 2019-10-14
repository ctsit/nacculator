import os
import sys
import csv
import re
import fileinput
import ConfigParser

from collections import defaultdict

fill_default_values = { 'nogds' : 0,
                        'adcid' : 41,
                        'formver' : 3 }

fill_non_blank_values = { 'adcid' : '41' }

#This dictionary contains the keys used in the config
def validate(func):
    def read_config(config_path):
        config = ConfigParser.ConfigParser()
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
        func(*updated_args,**kwargs)

    return validate_filter

def int_or_string(value, default=-1):
    try:
        returnable = int(value)
    except ValueError:
        returnable = value or default

    return returnable

@validate
def filter_clean_ptid(input_ptr, filter_config, output_ptr):
# TODO  To deal with M Flag in Current_db.csv

    filepath = filter_config['filepath']
    redcap_packet_list = csv.DictReader(input_ptr)
    output = csv.DictWriter(output_ptr, None)
    write_headers(redcap_packet_list, output)

    followup_visit = re.compile("followup.*")
    initial_visit = re.compile("initial.*")

    completed_subjs = defaultdict(list)
    with open(filepath, 'r') as nacc_packet_file:
        nacc_packet_list = csv.DictReader(nacc_packet_file)
        for nacc_packet in nacc_packet_list:
            if nacc_packet['Status'].lower() == "current":
                nacc_subj_id = nacc_packet['Patient ID']
                nacc_visit_num = int_or_string(nacc_packet['Visit Num'])
                completed_subjs[nacc_subj_id].append(nacc_visit_num)

    for redcap_packet in redcap_packet_list:
        #if they exist in completed subjs (same id and visit num) then remove them.
        rc_ptid = redcap_packet['ptid']
        rc_event = redcap_packet['redcap_event_name']
        if not (initial_visit.match(rc_event) or followup_visit.match(rc_event)):
            print >> sys.stderr, 'Eliminated ptid : ' + rc_ptid + " Event Name : " + redcap_packet['redcap_event_name'] + " NOT INIT OR FOLLOWUP"
            continue

        if redcap_packet['visitnum']:
            rc_visit_num = int_or_string(redcap_packet['visitnum'], -1)
        else:
            print >> sys.stderr, 'Eliminated ptid : ' + rc_ptid + " Event Name : " + redcap_packet['redcap_event_name'] + " MISSING VISIT NUM"
            continue
        if rc_ptid in completed_subjs:
            if rc_visit_num in completed_subjs[rc_ptid]:
                print >> sys.stderr, 'Eliminated ptid : ' + rc_ptid + " Event Name : " + redcap_packet['redcap_event_name'] + " IN CURRENT"
                continue
        output.writerow(redcap_packet)
    return output

def write_headers(reader, output):
    if output.fieldnames is None:
        # Initially empty file. Write column headers.
        output.fieldnames = reader.fieldnames
        output_header = dict((h,h) for h in reader.fieldnames)
        output.writerow(output_header)

@validate
def filter_replace_drug_id(input_ptr, filter_meta, output_ptr):
    reader = csv.DictReader(input_ptr)
    output = csv.DictWriter(output_ptr, None)
    write_headers(reader, output)
    for record in reader:
        count = 0
        prefixes = ['','fu_']
        for prefix in prefixes:
            for i in range(1, 31):
                col_name = prefix + 'drugid_' + str(i)
                if col_name in record.keys():
                    col_value = record[col_name]
                    if len(col_value) > 0 :
                        record[col_name] = 'd' + col_value[1:]
                        count += 1
        output.writerow(record)
        print >> sys.stderr, 'Processed ptid : ' + record['ptid'] + ' Updated ' + str(count) + ' fields.'
    return

@validate
def filter_fix_headers(input_file, header_mapping, output_file):
    csv_reader = csv.reader(input_file)
    csv_writer = csv.writer(output_file)
    headers = csv_reader.next()
    fixed_headers = list(map(lambda header: header_mapping.get(header,header), headers))
    csv_writer.writerow(fixed_headers)
    csv_writer.writerows([row for row in csv_reader])

    return

@validate
def filter_remove_ptid(input_ptr, filter_config, output_ptr):
    regex_exp = filter_config['ptid_format']
    good_ptids_string = filter_config['good_ptid'] 
    bad_ptids_string = filter_config['bad_ptid'] 
    good_ptids_list = ptid_string_to_list(good_ptids_string)
    bad_ptids_list = ptid_string_to_list(bad_ptids_string)
    reader = csv.DictReader(input_ptr)
    output = csv.DictWriter(output_ptr, None)
    write_headers(reader, output)
    for record in reader:
        prog = re.compile(regex_exp)
        if test_all_ptid(bad_ptids_list,record['ptid']):        #have not tested removing specific bad ptid
            print >> sys.stderr, 'Removed ptid : ' + record['ptid']
        elif test_all_ptid(good_ptids_list,record['ptid']):     
            output.writerow(record)
        elif prog.match(record['ptid'])!=None:
            output.writerow(record)
        else:
            print >> sys.stderr, 'Removed ptid : ' + record['ptid']

@validate
def filter_eliminate_empty_date(input_ptr, filter_meta, output_ptr):
    reader = csv.DictReader(input_ptr)
    output = csv.DictWriter(output_ptr, None)
    write_headers(reader, output)
    for record in reader:
        if _invalid_date(record):
            print >> sys.stderr, ' Empty Visit Date ' + record['ptid']
        else:
            output.writerow(record)

def _invalid_date(record):
    return (record['visitmo']=='' or record['visitday']=='' or record['visityr']=='')

def fill_value_of_fields(input_ptr, output_ptr, keysDict, blankCheck=False, defaultCheck=False):
    reader = csv.DictReader(input_ptr)
    output = csv.DictWriter(output_ptr, None)
    write_headers(reader, output)
    for record in reader:
        count = 0
        for col_name in keysDict.keys():
            if col_name in record.keys():
                if blankCheck and (len(record[col_name]) > 0) and (record[col_name] != keysDict[col_name]):
                        record[col_name] = keysDict[col_name]
                        count += 1
                elif defaultCheck and len(record[col_name]) == 0:
                        record[col_name] = keysDict[col_name]
                        count += 1
        output.writerow(record)
        print >> sys.stderr, 'Processed ptid : ' + record['ptid'] + ' Updated ' + str(count) + ' fields.'
    return

@validate
def filter_fix_visitdate(input_ptr, filter_meta, output_ptr):
    reader = csv.DictReader(input_ptr)
    output = csv.DictWriter(output_ptr, None)
    write_headers(reader,output)
    for record in reader:
        if record['visitnum']:
            record['visitnum'] = int_or_string(record['visitnum'])
        print >> sys.stderr, 'Processed ptid : ' + record['ptid']
        output.writerow(record)
    return

@validate
def filter_fill_default(input_ptr, filter_meta, output_ptr):
    fill_value_of_fields(input_ptr, output_ptr, fill_default_values, defaultCheck=True)

@validate
def filter_update_field(input_ptr, filter_meta, output_ptr):
    fill_value_of_fields(input_ptr, output_ptr, fill_non_blank_values, blankCheck=True)

def filter_extract_ptid(input_ptr, Ptid, visit_num, visit_type, output_ptr):
    reader = csv.DictReader(input_ptr)
    output = csv.DictWriter(output_ptr, None)
    write_headers(reader, output)

    if(visit_num and visit_type):
        filtered = filter(lambda row: filter_csv_all(Ptid, visit_num, visit_type, row), reader)

    elif(not visit_num and visit_type):
        filtered = filter(lambda row: filter_csv_vtype(Ptid, visit_type, row), reader)

    elif(not visit_type and visit_num):
        filtered = filter(lambda row: filter_csv_vnum(Ptid, visit_num, row), reader)

    elif(not visit_type and not visit_num):
        filtered = filter(lambda row: filter_csv_ptid(Ptid, row), reader)
    output.writerows(filtered)

def filter_csv_all(Ptid, visit_num, visit_type, record):
    if record['ptid'] == Ptid and record['visitnum'].lstrip("0") == visit_num and (re.search(visit_type, record['redcap_event_name'])):
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

def test_all_ptid(ptid_list, record):  
    for x in ptid_list:
        if record == x:
            return True

def ptid_string_to_list(ptid_string):
    li = list(ptid_string.split(","))
    return li  