NACCulator
==========

[![DOI](https://zenodo.org/badge/20501/ctsit/nacculator.svg)](https://zenodo.org/badge/latestdoi/20501/ctsit/nacculator)

Converts a CSV data file exported from REDCap into the NACC's UDS3 fixed-width
format.


Files
-----

This is not exhaustive, but here is an explanation of some important files.

* `nacc/`:
    top-level Python package for all things NACC.

* `nacc/redcap2nacc.py`:
    converts a CSV data file exported from REDCap into NACC's UDS3 fixed-width
    format.

* `nacc/uds3/blanks.py`:
    specialized library for "Blanking Rules".

* `nacc/uds3/ivp/forms.py`:
    UDS3 IVP forms represented as Python classes.

* `tools/generator.py`:
    generates Python objects based on NACC Data Element Dictionaries in CSV.


HOW TO Convert from REDCap to NACC
---------------------------------

Once the project data is exported from REDCap to the CSV file `data.csv`, run:

    $ pip install nacculator
    $ redcap2nacc < data.csv > data.txt

Or, if you're using the source code:

    $ PYTHONPATH=. ./nacc/redcap2nacc.py < data.csv > data.txt

The program accepts two arguments -file and -(ivp|fvp|np). Both the arguments are optional. See the python help as:

      $ PYTHONPATH=. ./nacc/redcap2nacc.py -h
      usage: redcap2nacc.py [-h]
                        [-fvp | -ivp | -np | -f {cleanPtid,updateField,replaceDrugId,fillDefault,fixC1S}]
                        [-file FILE] [-meta FILTER_META]

      Process redcap form output to nacculator.

      optional arguments:
      -h, --help            show this help message and exit
      -fvp                  Set this flag to process as fvp data
      -ivp                  Set this flag to process as ivp data
      -np                   Set this flag to process as np data
      -f or --filter        Accepts one of {cleanPtid,updateField,replaceDrugId,fillDefault,fixC1S}
                            Set this flag to process the filter
      -file FILE            Path of the csv file to be processed.
      -meta FILTER_META     Input file for the filter metadata (in case cleanPtid is used)

Example Usage

    PYTHONPATH=. ./nacc/redcap2nacc.py  -np -file data.csv > data.txt

To use a filter,

    PYTHONPATH=. ./nacc/redcap2nacc.py  -f cleanPtid -meta someFileName.csv < data.csv > data.txt

Only cleanPtid filter requires a meta file to be passed to it. Other filters do not need a meta tag.    

_Note: output is written to `STDOUT`; errors are written to `STDERR`; input can
be `STDIN` or the first argument passed to `redcap2nacc`._

If there are no errors, then submit the `data.txt` file to NACC.

HOW TO Use nacculator to filter data
------------------------

If your data is not clean enough to be processed by nacculator, there are some
built in functions to clean (read transform) the data.

* **cleanPtid**

  This filter requires the meta option to be set using the -meta flag. The meta
  file can be a csv file of ptids to be removed. All the records whose ptid is
  found in the passed meta file will be discarded in the output file.

  Example meta file:

      $ cat sampleRemovePtidFile.csv
      ptids
      110001
      110003

* **replaceDrugId**

  This filter replaces the first character of non empty fields of columns
  drugid_1 to drugid_30 with character "**d**"

  This filter does not require any meta data file as of now.

* **fixC1S**

  This filter fixes the column names of some of the fields in C1S form. This
  filter does not check for any data. It always replaces the column names if found.

  Currently, below replacements are used:

      c1s_2a_npsylan    ->  c1s_2_npsycloc
      c1s_2a_npsylanx   ->  c1s_2a_npsylan
      b6s_2a1_npsylanx  ->  c1s_2a1_npsylanx


* **fillDefault**

  This filter is used to set some predefined fields to their corresponding
  predefined values. Below are the current defaults :

      nogds    -> 0
      arthupex -> 0
      arthloex -> 0
      arthspin -> 0
      arthunk  -> 0NACCulator

* **getPtid**

    This filter is used to get information about a single PatientID. 
    You need to use <kbd>-ptid</kbd> to give the patient ID.
    You can use the optional tags like <kbd>-vnum</kbd> to get the records with particular visit number and PatientID or use
    <kbd>-vtype</kbd> to get records with particular visit type and Patient ID.
    
    <code>
    PYTHONPATH=. ./nacc/redcap2nacc.py  -f getPtid -ptid some_patient_ID -vnum some_visit_num -vtype somevisit_type                          < data.csv > data.txt
    </code>


[![DOI](https://zenodo.org/badge/20501/ctsit/nacculator.svg)](https://zenodo.org/badge/latestdoi/20501/ctsit/nacculator)

Converts a CSV data file exported from REDCap into the NACC's UDS3 fixed-width
format.


Files
-----

This is not exhaustive, but here is an explanation of some important files.

* `nacc/`:
    top-level Python package for all things NACC.

* `nacc/redcap2nacc.py`:
    converts a CSV data file exported from REDCap into NACC's UDS3 fixed-width
    format.

* `nacc/uds3/blanks.py`:
    specialized library for "Blanking Rules".

* `nacc/uds3/ivp/forms.py`:
    UDS3 IVP forms represented as Python classes.

* `tools/generator.py`:
    generates Python objects based on NACC Data Element Dictionaries in CSV.

* `/run_filters.py and run_filters.sh`:
    pulls data from REDCap based on the settings found in nacculator_cfg.ini (for .py)
    and filters_config.cfg (for .sh).

HOW TO Convert from REDCap to NACC
---------------------------------

Once the project data is exported from REDCap to the CSV file `data.csv`, run:

    $ pip install nacculator
    $ redcap2nacc < data.csv > data.txt

Or, if you're using the source code:

    $ PYTHONPATH=. ./nacc/redcap2nacc.py < data.csv > data.txt

The program accepts two arguments -file and -(ivp|fvp|np). Both the arguments are optional. See the python help as:

      $ PYTHONPATH=. ./nacc/redcap2nacc.py -h
      usage: redcap2nacc.py [-h]
                        [-fvp | -ivp | -np | -f {cleanPtid,updateField,replaceDrugId,fillDefault,fixC1S}]
                        [-file FILE] [-meta FILTER_CONFIG]

      Process redcap form output to nacculator.

      optional arguments:
      -h, --help            show this help message and exit
      -fvp                  Set this flag to process as fvp data
      -ivp                  Set this flag to process as ivp data
      -np                   Set this flag to process as np data
      -f or --filter        Accepts one of {cleanPtid,updateField,replaceDrugId,fillDefault,fixC1S}
                            Set this flag to process the filter
      -file FILE            Path of the csv file to be processed.
      -meta FILTER_META     Filter config file (nacculator_cfg.ini) when running filters

Example Usage

    PYTHONPATH=. ./nacc/redcap2nacc.py  -np -file data.csv > data.txt

To use a filter,

    PYTHONPATH=. ./nacc/redcap2nacc.py  -f cleanPtid -meta nacculator_cfg.ini < data.csv > data.txt

_Note: output is written to `STDOUT`; errors are written to `STDERR`; input can
be `STDIN` or the first argument passed to `redcap2nacc`._

If there are no errors, then submit the `data.txt` file to NACC.

HOW TO Use nacculator to filter data
------------------------

If your data is not clean enough to be processed by nacculator, there are some
built in functions to clean (read transform) the data.

In order to properly use the filters, the first step is to check and validate
that the nacculator_cfg.ini file has the proper settings for the filter to run.
The config file contains sections with in-code filter function name. Each of
these sections contains elements necessary for the filter to run.
The filters described below will discuss what is required, if anything.
If the filter requires the config, it must be passed with the -meta flag like
the example above shows.

* **cleanPtid**

  **Filter config required**
  This filter requires a section in the config called 'filter_clean_ptid'. This
  section will contain a single key 'filepath' which will point to a csv file
  of ptids to be removed. All the records whose ptid with same packet and visit
  num found in the passed meta file will be discarded in the output file.

  Example meta file:

      Patient ID,Packet type,Visit Num,Status
      110001,I,1,Current
      110001,M,M1,Current
      110003,I,001,Current
      110003,F,002,Current

* **replaceDrugId**

  This filter replaces the first character of non empty fields of columns
  drugid_1 to drugid_30 with character "**d**"

  This filter does not require any meta data file as of now.

* **fixHeaders**

  **Filter config required**
  This filter requires a section in the config called 'filter_fix_headers' with
  as many keys as needed to replace the necessary columns. See example below.
  This filter fixes the column names of any column found in the filter mapping.
  This filter does not check for any data. It always replaces the column names
  if found.

  Currently, below replacements are used:

      config:
      c1s_2a_npsylan: c1s_2_npsycloc
      c1s_2a_npsylanx: c1s_2a_npsylan
      b6s_2a1_npsylanx: c1s_2a1_npsylanx
      fu_otherneur: fu_othneur
      fu_otherneurx: fu_othneurxs
      fu_strokedec: fu_strokdec


* **fillDefault**

  This filter is used to set some predefined fields to their corresponding
  predefined values. Below are the current defaults :

      nogds    -> 0
      arthupex -> 0
      arthloex -> 0
      arthspin -> 0
      arthunk  -> 0

  *If field is blank, always it will be updated to default value.*

* **updateField**

  This filter is used to update non blank fields. Currently, only adcid is updated
  to 41.

* **removePtid**

  **Filter config required**
  This filter requires a section in the config called 'filter_remove_ptid' with
  a single key called 'ptid_format'. The value for that key is a regex string
  to match ptids that are to be kept.

  This filter is used to remove ptids that may have a different set of ids for a
  different study, or help limit which ids show up in the final result.

      config:
      ptid_format: 11\d.*

* **removeDateRecord**

  This filter is used to remove records who may be missing visit dates. It
  searches for rows missing the visit day, month, or year. If any of those
  fields are missing, it removes the row.



HOW TO Generate New Forms
------------------------

_Note: executing `generator.py` from within tools is an important step as the
script assumes any corrected DEDs are stored under a folder in the current
working directory called `corrected`._

**Warning: read the warnings in the current `./nacc/uds3/ivp/forms.py` first.**

    $ cd tools
    $ PYTHONPATH=.. ./generator.py uds3/ded/csv/ > ../nacc/uds3/ivp/forms.py
    $ edit ../nacc/uds3/ivp/forms

* Resources for uds3 fvp forms are available [here](https://www.alz.washington.edu/NONMEMBER/UDS/DOCS/VER3/).


  *If field is blank, always it will be updated to default value.*

* **updateField**

  This filter is used to update non blank fields. Currently, only adcid is updated
  to 41.



HOW TO Generate New Forms
------------------------

_Note: executing `generator.py` from within tools is an important step as the
script assumes any corrected DEDs are stored under a folder in the current
working directory called `corrected`._

**Warning: read the warnings in the current `./nacc/uds3/ivp/forms.py` first.**

    $ cd tools
    $ PYTHONPATH=.. ./generator.py uds3/ded/csv/ > ../nacc/uds3/ivp/forms.py
    $ edit ../nacc/uds3/ivp/forms

* Resources for uds3 fvp forms are available [here](https://www.alz.washington.edu/NONMEMBER/UDS/DOCS/VER3/).


FAQ
------------------------

- This is developed and tested on Python 2.7
- If there are key not found errors, then your dictionary may have the value with a different name. Make sure you the name of the keys is consistent while writing and reading.
