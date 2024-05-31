from redcap import Project
from configparser import ConfigParser

import logging
import pandas as pd
import sys


def main():
    config_path = sys.argv[1]

    try:
        config = ConfigParser()
        config.read(config_path)
        project_url = config.get('pycap', 'redcap_server')
        api_tokens = config.get('pycap', 'tokens').split(',')
    except Exception as e:
        logging.error(
            f" error: {e}."
            f" An error occurred when trying to read from the config file."
            f" Either the provided config file ({config_path}) does not exist,"
            f" an invalid value has been provided for 'redcap_server', or 'tokens' in the '[pycap]' section."
        )
        sys.exit()

    df_all_project_data = pd.DataFrame()
    for token in api_tokens:
        project = Project(project_url, token)
        data = project.export_records()
        df = pd.DataFrame(data)
        # ignore index to prevent overwriting data between projects
        df_all_project_data = pd.concat([df_all_project_data, df], ignore_index=True)

    # Ignore index to remove the record number column
    df_all_project_data.to_csv("redcap_input.csv", index=False)


if __name__ == "__main__":
    main()
