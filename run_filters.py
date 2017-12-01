import os
import sys
import csv
import yaml
import json
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


def run_all_filters(folder_name, filter_config):
    filter_meta = filter_config.get('current_sub')
    header_mapping = filter_config.get('header_mapping', {})
    regex_exp = filter_config.get('ptid_format')
    print "ptid Format "+regex_exp

    # Calling Filters
    try:
        print >> sys.stderr, "--------------Removing subjects already in current--------------------"
        input_path = os.path.join(folder_name, "redcap_input.csv")
        output_path = os.path.join(folder_name, "clean.csv")
        print >> sys.stderr, "Processing"
        with open (output_path,'w') as output_ptr, open (input_path,'r') as input_ptr:
            filter_clean_ptid(input_ptr, filter_meta, output_ptr)

        print >> sys.stderr, "--------------Replacing drug IDs--------------------"
        input_path = os.path.join(folder_name, "clean.csv")
        output_path = os.path.join(folder_name, "drugs.csv")
        with open (output_path,'w') as output_ptr, open (input_path,'r') as input_ptr:
            filter_replace_drug_id(input_ptr, filter_meta, output_ptr)

        print >> sys.stderr, "--------------Fixing Headers--------------------"
        input_path = os.path.join(folder_name, "drugs.csv")
        output_path = os.path.join(folder_name, "clean_headers.csv")
        filter_fix_headers(input_path, header_mapping, output_path)

        print >> sys.stderr, "--------------Filling in Defaults--------------------"
        input_path = os.path.join(folder_name, "clean_headers.csv")
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
            filter_remove_ptid(input_ptr, filter_meta, regex_exp, output_ptr)

        print >> sys.stderr, "--------------Removing Records without VisitDate--------------------"
        input_path = os.path.join(folder_name, "CleanedPtid_Update.csv")
        output_path = os.path.join(folder_name, "final_Update.csv")
        with open (output_path,'w') as output_ptr, open (input_path,'r') as input_ptr:
            filter_eliminate_empty_date(input_ptr, filter_meta, output_ptr)

    except Exception as e:
        print "Error in Opening a file"
        print e


    return

def read_from_config(config_path):
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
def get_data_from_redcap(folder_name, token, redcap_url):
    # Enter the path for filters_config

    redcap_access_api = API(token, redcap_url, 'master.yaml')
    res = redcap_access_api.export_records(adhoc_redcap_options={
                                              'format': 'csv'
                                          })
    try:
        rawdata = str(res.content).encode("utf-8")
        myreader = csv.reader(rawdata.splitlines())
        try:
            with open(os.path.join(folder_name, "redcap_input.csv"),"w") as file:
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
    currentdate = datetime.datetime.now().strftime('%m-%d-%Y')
    folder_name = "run_" + currentdate
    print >> sys.stderr, "Recent folder " + folder_name
    print "Recent folder " + folder_name

    current_directory = os.getcwd()
    identified_folder = os.path.join(current_directory, folder_name)

    if not os.path.exists(identified_folder):
        recent_run_folder(identified_folder)

# Reading from Config and Accessing the necessary Data
    config = read_from_config("filters_config.yaml")
    token = config.get('token')
    redcap_url = config.get('redcap_server')
    filter_config = config.get('filter_config')

    get_data_from_redcap(folder_name, token, redcap_url)
    run_all_filters(folder_name, filter_config)

    exit()
