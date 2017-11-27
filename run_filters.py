import os
import sys
import csv
import re
import fileinput
import requests
import yaml
import json
import csv
import datetime
import time
import nacc
from cappy import API
from nacc.uds3.filters import *

# Creating a folder which contains Intermediate files
def recent_run_folder(out_dir):
    #Check if directory exists. If not, create it.
    if not os.path.exists(out_dir):
        try:
            os.makedirs(out_dir)
        except Exception as e:
            raise e

def get_headers(input_ptr):
    reader = csv.DictReader(input_ptr)
    headers = reader.fieldnames
    print headers


def run_all_filters(folder_name):
    filter_meta = "./current-db-subjects.csv"

    # Calling Filters
    try:
        print >> sys.stderr, "--------------Removing subjects already in current--------------------"
        input_path = os.path.join(folder_name, "redcap_intput.csv")
        output_path = os.path.join(folder_name, "clean.csv")
        with open (output_path,'w') as output_ptr, open (input_path,'r') as input_ptr:
            filter_clean_ptid(input_ptr, filter_meta, output_ptr)

        print >> sys.stderr, "--------------Replacing drug IDs--------------------"
        input_path = os.path.join(folder_name, "clean.csv")
        output_path = os.path.join(folder_name, "drugs.csv")
        with open (output_path,'w') as output_ptr, open (input_path,'r') as input_ptr:
            filter_replace_drug_id(input_ptr, filter_meta, output_ptr)

        print >> sys.stderr, "--------------Fixing C1S in files--------------------"
        input_path = os.path.join(folder_name, "drugs.csv")
        output_path = os.path.join(folder_name, "c1s.csv")
        with open (output_path,'w') as output_ptr, open (input_path,'r') as input_ptr:
            filter_fix_c1s(input_ptr, filter_meta, output_ptr)

        print >> sys.stderr, "--------------Fixing FVP in files--------------------"
        input_path = os.path.join(folder_name, "c1s.csv")
        output_path = os.path.join(folder_name, "fixed_fvp.csv")
        with open (output_path,'w') as output_ptr, open (input_path,'r') as input_ptr:
            filter_fix_fvpheader(input_ptr, filter_meta, output_ptr)

        print >> sys.stderr, "--------------Filling in Defaults--------------------"
        input_path = os.path.join(folder_name, "fixed_fvp.csv")
        output_path = os.path.join(folder_name, "default.csv")
        with open (output_path,'w') as output_ptr, open (input_path,'r') as input_ptr:
            filter_fill_default(input_ptr, filter_meta, output_ptr)

        print >> sys.stderr, "--------------Updating fields--------------------"
        input_path = os.path.join(folder_name, "default.csv")
        output_path = os.path.join(folder_name, "Update_field.csv")
        with open (output_path,'w') as output_ptr, open (input_path,'r') as input_ptr:
            filter_update_field(input_ptr, filter_meta, output_ptr)

        print >> sys.stderr, "--------------Removing Unnecessary Records--------------------"
        input_path = os.path.join(folder_name, "Update_field.csv")
        output_path = os.path.join(folder_name, "CleanedPtid_Update.csv")
        with open (output_path,'w') as output_ptr, open (input_path,'r') as input_ptr:
            filter_remove_ptid(input_ptr, filter_meta, output_ptr)

        print >> sys.stderr, "--------------Removing Records without VisitDate--------------------"
        input_path = os.path.join(folder_name, "CleanedPtid_Update.csv")
        output_path = os.path.join(folder_name, "final_Update.csv")
        with open (output_path,'w') as output_ptr, open (input_path,'r') as input_ptr:
            filter_eliminate_empty_date(input_ptr, filter_meta, output_ptr)

    except Exception as e:
        print "Error in Opening a file"
        print e


    return

def connect_to_redcap(config_path):
    #Read in the config file. If the config file is missing or the wrong format, exit the program.
    print config_path
    try:
        with open(config_path, 'r') as config_file:
            config = yaml.load(config_file.read())
        print "Config Loaded"
    except:
        print("Error: Check config file")
        exit()
    return config



# Getting Data From RedCap
def get_data_from_redcap(folder_name):
    # Enter the path for filters_config
    config = connect_to_redcap("filters_config.yaml")
    token = config.get('token')
    redcap_url = config.get('redcap_server')
    redcap_access_api = API(token, redcap_url, 'master.yaml')
    res = redcap_access_api.export_records(adhoc_redcap_options={
                                              'format': 'csv'
                                          })
    try:
        rawdata = str(res.content).encode("utf-8")
        myreader = csv.reader(rawdata.splitlines())
        try:
            with open(os.path.join(folder_name, "redcap_intput.csv"),"w") as file:
                writer = csv.writer(file, delimiter=',')
                for row in myreader:
                    writer.writerow(row)
        except Exception as e:
            print("Error in Writing")
            print e

    except:
        print("Error in CSV file")

    return


if __name__ == '__main__':
    curentdate = datetime.datetime.now().strftime('%m-%d-%Y')
    folder_name = "run_"+curentdate
    print >> sys.stderr, "Recent folder "+folder_name
    print "Recent folder "+folder_name

    current_directory = os.getcwd()
    identified_folder = os.path.join(current_directory, folder_name)

    if not os.path.exists(identified_folder):
        recent_run_folder(identified_folder)

    get_data_from_redcap(folder_name)
    run_all_filters(folder_name)

    exit()
