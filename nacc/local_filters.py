import os
import sys
import csv
import datetime
import configparser
from nacc.uds3.filters import *


# Creating a folder which contains Intermediate files
def recent_run_folder(out_dir):
    # Check if directory exists. If not, create it.
    if not os.path.exists(out_dir):
        try:
            os.makedirs(out_dir)
        except Exception as e:
            raise e


def get_headers(input_ptr):
    reader = csv.DictReader(input_ptr)
    headers = reader.fieldnames
    print(headers)


def run_all_filters(folder_name, config, input_name):
    # Calling Filters
    try:
        print("--------------Removing subjects already in current--------------------", file=sys.stderr)
        if input_name:
            input_path = input_name
        else:
            input_path = os.path.join(folder_name, "redcap_input.csv")
        output_path = os.path.join(folder_name, "clean.csv")
        print("Processing", file=sys.stderr)
        with open(output_path, 'w') as output_ptr, open(input_path, 'r') as input_ptr:
            filter_clean_ptid(input_ptr, config, output_ptr)

        print("--------------Replacing drug IDs--------------------", file=sys.stderr)
        input_path = os.path.join(folder_name, "clean.csv")
        output_path = os.path.join(folder_name, "drugs.csv")
        with open(output_path, 'w') as output_ptr, open(input_path, 'r') as input_ptr:
            filter_replace_drug_id(input_ptr, config, output_ptr)

        print("--------------Fixing Headers--------------------", file=sys.stderr)
        input_path = os.path.join(folder_name, "drugs.csv")
        output_path = os.path.join(folder_name, "clean_headers.csv")
        with open(output_path, 'w') as output_ptr, open(input_path, 'r') as input_ptr:
            filter_fix_headers(input_ptr, config, output_ptr)

        print("--------------Filling in Defaults--------------------", file=sys.stderr)
        input_path = os.path.join(folder_name, "clean_headers.csv")
        output_path = os.path.join(folder_name, "default.csv")
        with open(output_path, 'w') as output_ptr, open(input_path, 'r') as input_ptr:
            filter_fill_default(input_ptr, config, output_ptr)

        print("--------------Updating fields--------------------", file=sys.stderr)
        input_path = os.path.join(folder_name, "default.csv")
        output_path = os.path.join(folder_name, "update_fields.csv")
        with open(output_path, 'w') as output_ptr, open(input_path, 'r') as input_ptr:
            filter_update_field(input_ptr, config, output_ptr)

        print("--------------Fixing Visit Dates--------------------", file=sys.stderr)
        input_path = os.path.join(folder_name, "update_fields.csv")
        output_path = os.path.join(folder_name, "proper_visitdate.csv")
        with open(output_path, 'w') as output_ptr, open(input_path, 'r') as input_ptr:
            filter_fix_visitdate(input_ptr, config, output_ptr)

        print("--------------Removing Unnecessary Records--------------------", file=sys.stderr)
        input_path = os.path.join(folder_name, "proper_visitdate.csv")
        output_path = os.path.join(folder_name, "CleanedPtid_Update.csv")
        with open(output_path, 'w') as output_ptr, open(input_path, 'r') as input_ptr:
            filter_remove_ptid(input_ptr, config, output_ptr)

        print("--------------Removing Records without VisitDate--------------------", file=sys.stderr)
        input_path = os.path.join(folder_name, "CleanedPtid_Update.csv")
        output_path = os.path.join(folder_name, "final_Update.csv")
        with open(output_path, 'w') as output_ptr, open(input_path, 'r') as input_ptr:
            filter_eliminate_empty_date(input_ptr, config, output_ptr)

    except Exception as e:
        print("Error in Opening a file")
        print(e)

    return


def read_config(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    return config


def main():
    currentdate = datetime.datetime.now().strftime('%m-%d-%Y')
    folder_name = "run_" + currentdate
    input_name = ""
    print("Recent folder " + folder_name, file=sys.stderr)

    current_directory = os.getcwd()
    identified_folder = os.path.join(current_directory, folder_name)

    if not os.path.exists(identified_folder):
        recent_run_folder(identified_folder)

    # Reading from Config and Accessing the necessary Data
    config_path = sys.argv[1]
    try:
        if sys.argv[2]:
            input_name = sys.argv[2]
    except IndexError:
        pass
    # config = read_config(config_path)

    run_all_filters(folder_name, config_path, input_name)

    exit()


if __name__ == '__main__':
    main()
