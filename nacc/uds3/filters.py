import os
import sys
import csv
import fileinput

fix_c1s_headers = { 'c1s_2a_npsylan' : 'c1s_2_npsycloc',
                    'c1s_2a_npsylanx' : 'c1s_2a_npsylan',
                    'b6s_2a1_npsylanx' : 'c1s_2a1_npsylanx'}

fill_default_values = { 'nogds' : 0,
                        'arthupex' : 0,
                        'arthloex' : 0,
                        'arthspin' : 0,
                        'arthunk' : 0,
                        'adcid' : 41,
                        'formver' : 3 }

fill_non_blank_values = { 'adcid' : '41' }

def write_headers(reader, output):
    if output.fieldnames is None:
        # Initially empty file. Write column headers.
        output.fieldnames = reader.fieldnames
        output_header = dict((h,h) for h in reader.fieldnames)
        output.writerow(output_header)

def filter_clean_ptid(input_ptr, filter_meta, output_ptr):

    reader = csv.DictReader(input_ptr)
    output = csv.DictWriter(output_ptr, None)
    write_headers(reader, output)

    with open(filter_meta, 'r') as ptid_file:
        ptids = ptid_file.read().splitlines()
        for record in reader:
            ptid = record['ptid']
            if ptid not in ptids:
                output.writerow(record)
            else:
                print >> sys.stderr, 'Eliminated ptid : ' + ptid
    return

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

def filter_fix_c1s(input_ptr, filter_meta, output_ptr):

    lines = input_ptr.read().splitlines()
    header = True
    for line in lines:
        if header:
            header = False
            for key in fix_c1s_headers.keys():
                line=line.replace(key, fix_c1s_headers[key],1)
        print line
    return

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
