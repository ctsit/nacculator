import os
import sys
import csv
import re
import fileinput
from nacc.uds3.filters import  write_headers


def filter_clean_ptid(input_ptr, filter_meta, output_ptr):
# TODO  To deal with M Flag in Current_db.csv

    reader = csv.DictReader(input_ptr)
    output = csv.DictWriter(output_ptr, None)
    write_headers(reader, output)

    for record in reader:
        ptid = record['ptid']
        # print >> sys.stderr, ptid
        with open(filter_meta, 'r') as ptid_file:

            curr_ptid = csv.DictReader(ptid_file)
            repeat_flag = 0

            for row in curr_ptid:
                packet_type = row['Packet type']
                if ptid == row['Patient ID']:
                    prog_followup_visit = re.compile("followup.*")
                    prog_initial_visit = re.compile("initial.*")
                    if packet_type == "I" and prog_initial_visit.match(record['redcap_event_name']):
                        repeat_flag = 1
                        print >> sys.stderr, 'Eliminated ptid : ' + ptid + " Event Name : " + record['redcap_event_name']

                    elif packet_type == "F" and prog_followup_visit.match(record['redcap_event_name']):
                        repeat_flag = 1
                        print >> sys.stderr, 'Eliminated ptid : ' + ptid + " Event Name : " + record['redcap_event_name']

                    elif packet_type == "M":
                        repeat_flag = 1
                        print >> sys.stderr, 'Eliminated ptid : ' + ptid
            if(repeat_flag == 0):
                output.writerow(record)
    return

# def filter_clean_ptid(input_ptr, filter_meta, output_ptr):
#
#     reader = csv.DictReader(input_ptr)
#     output = csv.DictWriter(output_ptr, None)
#     write_headers(reader, output)
#
#     with open(filter_meta, 'r') as ptid_file:
#         ptids = ptid_file.read().splitlines()
#         for record in reader:
#             ptid = record['ptid']
#             prog_initial_visit = re.compile("initial.*")
#             if ptid in ptids and prog_initial_visit.match(record['redcap_event_name'])!=None:
#                 print >> sys.stderr, 'Eliminated ptid : ' + ptid
#             else:
#                 output.writerow(record)
#     return

def filter_eliminate_redcapeventname(input_ptr, filter_meta, output_ptr):

    reader = csv.DictReader(input_ptr)
    output = csv.DictWriter(output_ptr, None)
    write_headers(reader, output)
    for record in reader:
        prog_initial_visit = re.compile("initial.*")
        # prog_followup_visit = re.compile("followup.*")
        if prog_initial_visit.match(record['redcap_event_name'])==None:
            print >> sys.stderr, 'Removing  : ' + record['redcap_event_name']
        else:
            output.writerow(record)
    return
