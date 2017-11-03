import os
import sys
import csv
import re
import fileinput
from nacc.uds3.filters import  write_headers

def filter_clean_ptid(input_ptr, filter_meta, output_ptr):
# TODO  To run anything on followup visit Packet in future

    # reader = csv.DictReader(input_ptr)
    # output = csv.DictWriter(output_ptr, None)
    # curr_ptid = csv.DictReader(filter_meta)
    # write_headers(reader, output)
    #
    # # with open(filter_meta, 'r') as ptid_file:
    # for record in reader:
    #
    #     ptid = record['ptid']
    #
    #     for to_rem_ptid in curr_ptid:
    #         packet_type = to_rem_ptid['Packet type']
    #         if ptid == to_rem_ptid["Patient ID"]:
    #             prog_followup_visit = re.compile("followup.*")
    #             prog_initial_visit = re.compile("initial.*")
    #             if packet_type == "I" and prog_initial_visit.match(record['redcap_event_name']):
    #                 print >> sys.stderr, 'Eliminated ptid : ' + ptid + " Event Name : " + record['redcap_event_name']
    #
    #             elif packet_type == "F" and prog_followup_visit.match(record['redcap_event_name']):
    #                 print >> sys.stderr, 'Eliminated ptid : ' + ptid + " Event Name : " + record['redcap_event_name']
    #
    #             elif packet_type == "M":
    #                 print >> sys.stderr, 'Eliminated ptid : ' + ptid
    #
    #             else:
    #                 output.writerow(record)
    #         else:
    #             output.writerow(record)
    return

def filter_eliminate_redcapeventname(input_ptr, filter_meta, output_ptr):

    reader = csv.DictReader(input_ptr)
    output = csv.DictWriter(output_ptr, None)
    write_headers(reader, output)
    for record in reader:
        prog_initial_visit = re.compile("followup.*")
        # prog_followup_visit = re.compile("followup.*")
        if prog_initial_visit.match(record['redcap_event_name'])==None:
            print >> sys.stderr, 'Removing  : ' + record['redcap_event_name']
        else:
            output.writerow(record)
    return
