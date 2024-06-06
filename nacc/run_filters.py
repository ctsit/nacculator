import os
import sys
import csv
import datetime
import configparser
from redcap import Project
from nacc.uds3.filters import *
import logging
import pandas as pd


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


def run_all_filters(folder_name, config):
    # Calling Filters
    try:
        print("--------------Removing subjects already in current--------------------", file=sys.stderr)
        logging.info('Removing subjects already in current')
        input_path = os.path.join(folder_name, "redcap_input.csv")
        output_path = os.path.join(folder_name, "clean.csv")
        print("Processing", file=sys.stderr)
        with open(output_path, 'w') as output_ptr, open(input_path, 'r') as input_ptr:
            filter_clean_ptid(input_ptr, config, output_ptr)

        print("--------------Replacing drug IDs--------------------", file=sys.stderr)
        logging.info('Replacing drug IDs')
        input_path = os.path.join(folder_name, "clean.csv")
        output_path = os.path.join(folder_name, "drugs.csv")
        with open(output_path, 'w') as output_ptr, open(input_path, 'r') as input_ptr:
            filter_replace_drug_id(input_ptr, config, output_ptr)

        print("--------------Fixing Headers--------------------", file=sys.stderr)
        logging.info('Fixing Headers')
        input_path = os.path.join(folder_name, "drugs.csv")
        output_path = os.path.join(folder_name, "clean_headers.csv")
        with open(output_path, 'w') as output_ptr, open(input_path, 'r') as input_ptr:
            filter_fix_headers(input_ptr, config, output_ptr)

        print("--------------Filling in Defaults--------------------", file=sys.stderr)
        logging.info('Filling in Defaults')
        input_path = os.path.join(folder_name, "clean_headers.csv")
        output_path = os.path.join(folder_name, "default.csv")
        with open(output_path, 'w') as output_ptr, open(input_path, 'r') as input_ptr:
            filter_fill_default(input_ptr, config, output_ptr)

        print("--------------Updating fields--------------------", file=sys.stderr)
        logging.info('Updating fields')
        input_path = os.path.join(folder_name, "default.csv")
        output_path = os.path.join(folder_name, "update_fields.csv")
        with open(output_path, 'w') as output_ptr, open(input_path, 'r') as input_ptr:
            filter_update_field(input_ptr, config, output_ptr)

        print("--------------Fixing Visit Dates--------------------", file=sys.stderr)
        logging.info('Fixing Visit Dates')
        input_path = os.path.join(folder_name, "update_fields.csv")
        output_path = os.path.join(folder_name, "proper_visitnum.csv")
        with open(output_path, 'w') as output_ptr, open(input_path, 'r') as input_ptr:
            filter_fix_visitnum(input_ptr, config, output_ptr)

        print("--------------Removing Unnecessary Records--------------------", file=sys.stderr)
        logging.info('Removing unnecessary records')
        input_path = os.path.join(folder_name, "proper_visitnum.csv")
        output_path = os.path.join(folder_name, "CleanedPtid_Update.csv")
        with open(output_path, 'w') as output_ptr, open(input_path, 'r') as input_ptr:
            filter_remove_ptid(input_ptr, config, output_ptr)

        print("--------------Removing Records without VisitDate--------------------", file=sys.stderr)
        logging.info('Removing Records without VisitDate')
        input_path = os.path.join(folder_name, "CleanedPtid_Update.csv")
        output_path = os.path.join(folder_name, "final_Update.csv")
        with open(output_path, 'w') as output_ptr, open(input_path, 'r') as input_ptr:
            filter_eliminate_empty_date(input_ptr, config, output_ptr)

    except Exception as e:
        print("Error in Opening a file")
        logging.error('Error in Opening a file',
                      extra={
                          "report_handler": {
                              "data": {"ptid": None,
                                       "error": f'Error in Opening a file: {e}'},
                              "sheet": 'ERROR'
                          }
                      }
                      )
        print(e)

    return


def read_config(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    return config


def get_data_from_redcap_pycap(folder_name, config):
    """
    Uses PyCap to collect a REDCap project data export using your API token
    """
    # Enter the path for filters_config
    try:
        tokens = config.get('pycap', 'token').split(',')
        redcap_url = config.get('pycap', 'redcap_server')
    except Exception as e:
        print("Please check the config file and validate all the proper fields exist", file=sys.stderr)
        logging.error('Please check the config file and validate all the proper fields exist',
                      extra={
                          "report_handler": {
                              "data": {
                                  "ptid": None,
                                  "error": f'Please check the config file and validate all the proper fields exist : {e}'
                              },
                              "sheet": 'ERROR'
                          }
                      }
                      )
        print(e)
        raise e

    try:
        df_all_project_data = pd.DataFrame()
        for token in tokens:
            df_project_data = _get_project_data(redcap_url, token)
            df_all_project_data = pd.concat([df_all_project_data, df_project_data], ignore_index=True)

        # Ignore index to remove the record number column
        df_all_project_data.to_csv(os.path.join(folder_name, "redcap_input.csv"), index=False)
    except Exception as e:
        print("Error in exporting project data")
        logging.error('Error in processing project data',
                      extra={
                          "report_handler": {
                              "data": {"ptid": None, "error": f'Error in exporting project data: {e}'},
                              "sheet": 'ERROR'
                          }
                      }
                      )
        print(e)

    return


def _get_project_data(url: str, token: str) -> pd.DataFrame:
    df_project_data = pd.DataFrame()
    redcap_project = Project(url, token)

    # Get list of all fieldnames in project to create a csv header
    assert hasattr(redcap_project, 'field_names')
    header_a = getattr(redcap_project, 'field_names')

    header_b = []
    list_of_fields = redcap_project.export_field_names()
    for field in list_of_fields:
        header_b.append(field['export_field_name'])

    header_full = list(set(header_a + header_b))
    header_full.insert(1, 'redcap_event_name')

    # Get list of all records present in project to iterate over
    list_of_records = []

    # If there are multiple records with the same ptid only keep the first occurence
    # export all records only grabbing the ptid field
    all_records = redcap_project.export_records(fields=['ptid'])
    # iterate through all records
    for record in all_records:
        # if the ptid is not already in the list then append it
        if record['ptid'] not in list_of_records:
            list_of_records.append(record['ptid'])

    chunked_records = []
    # Break the list into chunks of 50
    n = 50
    for i in range(0, len(list_of_records), n):
        chunked_records.append(list_of_records[i:i + n])

    for current_record_chunk in chunked_records:
        chunked_data = redcap_project.export_records(records=current_record_chunk)
        df_project_data = pd.concat([df_project_data, pd.DataFrame(chunked_data)], ignore_index=True)

    return df_project_data


def main():
    currentdate = datetime.datetime.now().strftime('%m-%d-%Y')
    folder_name = "run_" + currentdate
    print("Recent folder " + folder_name, file=sys.stderr)

    current_directory = os.getcwd()
    identified_folder = os.path.join(current_directory, folder_name)

    if not os.path.exists(identified_folder):
        recent_run_folder(identified_folder)

# Reading from Config and Accessing the necessary Data
    config_path = sys.argv[1]
    config = read_config(config_path)

    get_data_from_redcap_pycap(folder_name, config)
    run_all_filters(folder_name, config_path)

    exit()


if __name__ == '__main__':
    main()
