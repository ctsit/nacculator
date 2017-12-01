import os
import sys
import csv
import re
import fileinput

fill_default_values = { 'nogds' : 0,
                        'arthupex' : 0,
                        'arthloex' : 0,
                        'arthspin' : 0,
                        'arthunk' : 0,
                        'adcid' : 41,
                        'formver' : 3 }

fill_non_blank_values = { 'adcid' : '41' }

def filter_clean_ptid(input_ptr, filter_meta, output_ptr):
# TODO  To deal with M Flag in Current_db.csv

    reader = csv.DictReader(input_ptr)
    output = csv.DictWriter(output_ptr, None)
    write_headers(reader, output)

    for record in reader:
        ptid = record['ptid']
        visit_num = record['visitnum']
        with open(filter_meta, 'r') as ptid_file:
            curr_ptid = csv.DictReader(ptid_file)
            repeat_flag = 0

            for row in curr_ptid:
                packet_type = row['Packet type']
                curr_visit = row['Visit Num']

                if ptid == row['Patient ID']:
                    prog_followup_visit = re.compile("followup.*")
                    prog_initial_visit = re.compile("initial.*")
                    prog_mile_visit = re.compile("milestone.*")
                    if packet_type == "I" and prog_initial_visit.match(record['redcap_event_name']):
                        repeat_flag = 1
                        print >> sys.stderr, 'Eliminated ptid : ' + ptid + " Event Name : " + record['redcap_event_name']

                    elif packet_type == "F" and prog_followup_visit.match(record['redcap_event_name']):
                        if (visit_num and visit_num == curr_visit) or visit_num == '':
                            repeat_flag = 1
                            print >> sys.stderr, 'Eliminated ptid : ' + ptid + " Event Name : " + record['redcap_event_name']

                    elif packet_type == "M" and prog_mile_visit.match(record['redcap_event_name']):
                        # The visit num for Mile Stone is given in M1...M2...M3 for so to get integra; part of it we use Regex
                        if (visit_num and re.search('\d+',curr_visit).group() == visit_num) or visit_num == '':
                            repeat_flag = 1
                            print >> sys.stderr, 'Eliminated ptid : ' + ptid+ " Event Name : " + record['redcap_event_name']
            if(repeat_flag == 0):
                output.writerow(record)
    return output

def write_headers(reader, output):
    if output.fieldnames is None:
        # Initially empty file. Write column headers.
        output.fieldnames = reader.fieldnames
        output_header = dict((h,h) for h in reader.fieldnames)
        output.writerow(output_header)

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

def filter_fix_headers(input_file, header_mapping, output_file):
    with open(input_file, 'r') as input_csv, open(output_file, 'w') as output_csv:
        csv_reader = csv.reader(input_csv)
        csv_writer = csv.writer(output_csv)
        headers = csv_reader.next()
        fixed_headers = list(map(lambda header: header_mapping.get(header,header), headers))
        csv_writer.writerow(fixed_headers)
        csv_writer.writerows([row for row in csv_reader])

    return

def filter_remove_ptid(input_ptr, filter_meta, regex_exp, output_ptr):

    reader = csv.DictReader(input_ptr)
    output = csv.DictWriter(output_ptr, None)
    write_headers(reader, output)
    for record in reader:
        prog = re.compile(regex_exp)
        if prog.match(record['ptid'])!=None:
            output.writerow(record)
        else:
            print >> sys.stderr, 'Removed ptid : ' + record['ptid']

def filter_eliminate_empty_date(input_ptr, filter_meta, output_ptr):

    reader = csv.DictReader(input_ptr)
    output = csv.DictWriter(output_ptr, None)
    write_headers(reader, output)
    for record in reader:
        if record['visitmo']=='' or record['visitday']=='' or record['visityr']=='':
            print >> sys.stderr, ' Empty Visit Date ' + record['ptid']
        else:
            output.writerow(record)

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

def filter_fill_default(input_ptr, filter_meta, output_ptr):
    fill_value_of_fields(input_ptr, output_ptr, fill_default_values, defaultCheck=True)

def filter_update_field(input_ptr, filter_meta, output_ptr):
    fill_value_of_fields(input_ptr, output_ptr, fill_non_blank_values, blankCheck=True)
