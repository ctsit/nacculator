import os
import sys
import csv
import json
import datetime
import time
import nacc
import ConfigParser
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


def run_all_filters(folder_name, config):
    # Calling Filters
    try:
        print >> sys.stderr, "--------------Removing subjects already in current--------------------"
        input_path = os.path.join(folder_name, "redcap_input.csv")
        output_path = os.path.join(folder_name, "clean.csv")
        print >> sys.stderr, "Processing"
        with open (output_path,'w') as output_ptr, open (input_path,'r') as input_ptr:
            filter_clean_ptid(input_ptr, config, output_ptr)

        print >> sys.stderr, "--------------Replacing drug IDs--------------------"
        input_path = os.path.join(folder_name, "clean.csv")
        output_path = os.path.join(folder_name, "drugs.csv")
        with open (output_path,'w') as output_ptr, open (input_path,'r') as input_ptr:
            filter_replace_drug_id(input_ptr, config, output_ptr)

        print >> sys.stderr, "--------------Fixing Headers--------------------"
        input_path = os.path.join(folder_name, "drugs.csv")
        output_path = os.path.join(folder_name, "clean_headers.csv")
        with open (output_path,'w') as output_ptr, open (input_path,'r') as input_ptr:
            filter_fix_headers(input_ptr, config, output_ptr)

        print >> sys.stderr, "--------------Filling in Defaults--------------------"
        input_path = os.path.join(folder_name, "clean_headers.csv")
        output_path = os.path.join(folder_name, "default.csv")
        with open (output_path,'w') as output_ptr, open (input_path,'r') as input_ptr:
            filter_fill_default(input_ptr, config, output_ptr)

        print >> sys.stderr, "--------------Updating fields--------------------"
        input_path = os.path.join(folder_name, "default.csv")
        output_path = os.path.join(folder_name, "Update_field.csv")
        with open (output_path,'w') as output_ptr, open (input_path,'r') as input_ptr:
            filter_update_field(input_ptr, config, output_ptr)

        print >> sys.stderr, "--------------Removing Unnecessary Records--------------------"
        input_path = os.path.join(folder_name, "Update_field.csv")
        output_path = os.path.join(folder_name, "CleanedPtid_Update.csv")
        with open (output_path,'w') as output_ptr, open (input_path,'r') as input_ptr:
            filter_remove_ptid(input_ptr, config, output_ptr)

        print >> sys.stderr, "--------------Removing Records without VisitDate--------------------"
        input_path = os.path.join(folder_name, "CleanedPtid_Update.csv")
        output_path = os.path.join(folder_name, "final_Update.csv")
        with open (output_path,'w') as output_ptr, open (input_path,'r') as input_ptr:
            filter_eliminate_empty_date(input_ptr, config, output_ptr)

    except Exception as e:
        print "Error in Opening a file"
        print e


    return

def read_config(config_path):
    config = ConfigParser.ConfigParser()
    config.read(config_path)
    return config

# Getting Data From RedCap
def get_data_from_redcap(folder_name, config):
    # Enter the path for filters_config
    try:
        token = config.get('cappy','token')
        redcap_url= config.get('cappy','redcap_server')
    except Exception as e:
        print >> sys.stderr, "Please check the config file and validate all the proper fields exist"
        print e
        raise e

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

    current_directory = os.getcwd()
    identified_folder = os.path.join(current_directory, folder_name)

    if not os.path.exists(identified_folder):
        recent_run_folder(identified_folder)

# Reading from Config and Accessing the necessary Data
    config_path = sys.argv[1]
    config = read_config(config_path)

    get_data_from_redcap(folder_name, config)
    run_all_filters(folder_name, config_path)

    exit()
