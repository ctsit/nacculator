NACCulator
==========

[![DOI](https://zenodo.org/badge/20501/ctsit/nacculator.svg)](https://zenodo.org/badge/latestdoi/20501/ctsit/nacculator)

NACCulator is a Python 3-based data converter that changes REDCap .csv exported
data to NACC’s fixed-width .txt format. It is configured for UDS3 forms,
including FTLD and LBD (versions 3.0 and 3.1). It will perform basic data
integrity checks during a run: verifying that each field is the correct type
and length, verifying that there are no illegal characters in the Char fields,
verifying that Num fields are within the acceptable range as defined in NACC's
Data Element Dictionary for each form, and checking that no blanking rules have
been violated. NACCulator outputs a .txt file that is immediately ready to
submit to NACC's database.

_Note:_ NACCulator _**requires Python 3.**_


HOW TO Convert from REDCap to NACC
----------------------------------

To install NACCulator, run:

    $ pip3 install git+https://github.com/ctsit/nacculator.git

Once the project data is exported from REDCap to the CSV file `data.csv`, run:

    $ redcap2nacc <data.csv >data.txt

This command will work only in the simplest case; UDS3 IVP data only.
NACCulator will automatically skip PTIDs with errors, so the output `data.txt`
file will be ready to submit to NACC.
In order to properly filter the data in the csv, NACCulator is expecting that
REDCap visits (denoted by `redcap_event_name`) contain certain keywords:
    "initial" for all initial visit packets (including telephone and optional modules such as lbd),
    "follow" for all followups (including version 3.1 telephone and optional modules),
    "milestone" for milestone packets,
    "neuropath" for neuropathology packets,
    "tele" for old (version 3.0) telephone followups,
    "covid" for covid-related survey packets

NACCulator collects data from the Z1X form first and uses that to determine the
presence of other forms in the packet. The Z1X form for that record must be
marked "Unverified" or "Complete" for NACCulator to recognize the record, and
each optional form must be marked as submitted within the Z1X for NACCulator to
find those forms.

_Note: For UDS visits (the -ivp and -fvp flags), NACCulator also expects the
A1 subject demographics form to be either Unverified or Complete._

_Note: output is written to `STDOUT`; errors are written to `STDERR`; input is
expected to be from `STDIN` (the command line) unless a file is specified using
the `-file` flag._


### Usage

    $ redcap2nacc -h
    usage: redcap2nacc [-h]
                       [-fvp | -ivp | -tip | -tfp | -tfp3 | -np | -np10 | -m | -cv | -csf | -f {cleanPtid,replaceDrugId,fixHeaders,fillDefault,updateField,removePtid,removeDateRecord,getPtid}]
                       [-lbd | lbdsv | -ftld] [-file FILE] [-meta FILTER_META] [-ptid PTID]
                       [-vnum VNUM] [-vtype VTYPE]

    Process redcap export data through nacculator.

    optional arguments:
      -h, --help            show this help message and exit
      -fvp                  Set this flag to process as FVP data
      -ivp                  Set this flag to process as IVP data
      -tfp                  Set this flag to process as Telephone Followup Packet v3.2 data
      -tip                  Set this flag to process as Telephone Initial Packet data
      -tfp3                 Set this flag to process as TFP v3.0 (pre-2020) data
      -np                   Set this flag to process as Neuropathology version 11 data
      -np10                 Set this flag to process as Neuropathology version 10 data
      -m                    Set this flag to process as Milestone data
      -cv                   Set this flag to process as COVID data
      -csf                  Set this flag to process as NACC BIDSS CSF data

      -f {cleanPtid,replaceDrugId,fixHeaders,fillDefault,updateField,removePtid,removeDateRecord,getPtid}, --filter {cleanPtid,replaceDrugId,fixHeaders,fillDefault,updateField,removePtid,removeDateRecord,getPtid}
                              Set this flag to run the data through the chosen filter
      -lbd                  Set this flag to process as Lewy Body Dementia data (FORMVER = 3)
      -lbdsv                Set this flag to process as Lewy Body Dementia short version data (FORMVER = 3.1)
      -ftld                 Set this flag to process as Frontotemporal Lobar Degeneration data

      -file FILE            Path of the csv file to be processed
      -meta FILTER_META     Input file for the filter metadata (in case -filter is used)
      -ptid PTID            Ptid for which you need the records
      -vnum VNUM            Visit number for which you need the records
      -vtype VTYPE          Visit type for which you need the records


**Example** - Process a Neuropathology form:

    $ redcap2nacc -np -file data.csv >data.txt

**Example** - Processing LBD Follow-up visit packets:

    redcap2nacc -lbd -fvp -file data.csv >data.txt

Both LBD / LBDSV and FTLD forms can have IVP or FVP arguments.

**Example** - Run data through the `cleanPtid` filter:

    $ redcap2nacc -f cleanPtid -meta nacculator_cfg.ini <data.csv >filtered_data.csv


HOW TO Filter Data Using NACCulator
-----------------------------------

If your data is not clean enough to be processed by NACCulator, there are some
built in functions to clean (read: transform) the data.

In order to properly use the filters, the first step is to check and validate
that `nacculator_cfg.ini` has the proper settings for the filter to run. In
order to create this file, find the `nacculator_cfg.ini.example` file and
remove the `.example` portion, and then fill in your center's information.
The config file contains sections with in-code filter function name. Each of
these sections contains elements necessary for the filter to run.
The filters described below will discuss what is required, if anything.

The filters can be run all at once with your REDCap API token using:

    $ nacculator_filters nacculator_cfg.ini

You can find more details on `nacculator_filters` under the section:
HOW TO Acquire current-db-subjects.csv for the filters


RUNNING ALL FILTERS ON A LOCAL FILE
------------------------------------------------------

REDCap has an export size limit that can be exceeded with a large project like
the ADRC. When the size of the project surpasses the REDCap limit, the
`nacculator_filters` command will no longer work. The data must be manually
exported from the project in chunks (whether by event or by ptid). However you
choose to export the data, keep in mind that all of the fields in a packet need
to be present in the input csv you use. So, for example, the A1 and A2 forms in
the IVP cannot be exported and run separately through NACCulator.

You can still run all the filters using your config file on a REDCap-exported
csv, even when not using `nacculator_filters`. The command to use this filter
locally is:

    $ python3 nacc/local_filters.py nacculator_cfg.ini redcap_input.csv

where `redcap_input.csv` is the location of the file you want to filter. The
filter will then run as normal, creating a `run_CURRENT-DATE` folder and
depositing each stage of the filter process in this folder. The final output
of the filter process is a csv file called `final_Update.csv` which can then
be run through NACCulator.


RUNNING INDIVIDUAL FILTERS
------------------------------------------------------

The filters can also be run one at a time on a `.csv` file with the `-f` and `-meta`
flags.

For example, to run the fixHeaders filter:

    $ redcap2nacc -f fixHeaders -meta nacculator_cfg.ini <data_input.csv >filtered_output.csv

If the filter requires the config, it must be passed with the `-meta` flag like
the example above shows.


* **cleanPtid**

  This filter requires a section in the config called `filter_clean_ptid`. This
  section will contain a single key `filepath` which will point to a csv 
  (usually called `current-db-subjects.csv`) file of ptids to be removed. All 
  the records whose ptid with same packet and visit num found in the passed 
  meta file will be discarded in the output file. This filter also removes 
  events that lack a visit number in REDCap.

  Example meta file:

      Patient ID,Packet type,Visit Num,Status
      110001,I,1,Current
      110001,M,M1,Current
      110003,I,001,Current
      110003,F,002,Current


* **replaceDrugId**

  This filter replaces the first character of non empty fields of columns
  `drugid_1` to `drugid_30` with character "**d**".


* **fixHeaders**

  This filter requires a section in the config called `filter_fix_headers` with
  as many keys as needed to replace the necessary columns. See example below.
  This filter fixes the column names of any column found in the filter mapping.
  This filter does not check for any data. It only replaces the column names
  if found.

  For example, the configuration would look like this:

      [filter_fix_headers]
      c1s_2a_npsylan: c1s_2_npsycloc
      c1s_2a_npsylanx: c1s_2a_npsylan
      b6s_2a1_npsylanx: c1s_2a1_npsylanx
      fu_otherneur: fu_othneur
      fu_otherneurx: fu_othneurxs
      fu_strokedec: fu_strokdec
      fukid9agd: fu_kid9agd
      fusib17pdx: fu_sib17pdx


* **fillDefault**

  This filter is used to set some predefined fields to their corresponding
  predefined values. Below are the current defaults :

      nogds    -> 0
      formver  -> 3

  *If field is blank, it will be updated to default value.*


* **updateField**

  This filter is used to update fields that already had a value in the REDCap
  export. Currently, only `adcid` is updated.


* **fixVisitNum**

  This filter is used to ensure that the `visitnum` field is always an integer.
  It is currently only accessible from the config file when running all
  filters.


* **removePtid**

  This filter requires a section in the config called `filter_remove_ptid` with
  a single key called `ptid_format`. The value for that key is a regex string
  to match ptids that are to be kept.
  11\d.* keeps all PTIDs that fit the format 11xxxx, such as 110001.

  This filter is used to remove ptids that may have a different set of ids for
  a different study, or help limit which ids show up in the final result.

      config:
      ptid_format: 11\d.*

* **removeDateRecord**

  This filter is used to remove records who may be missing visit dates. It
  searches for rows missing the visit day, month, or year. If any of those
  fields are missing, it removes the row.

* **getPtid**

    This filter is used to get information about a single PatientID and is not
    present in the config file. You need to use the `-ptid` flag to specify the
    patient ID.
    You can use the `-vnum` to get the records with particular visit number and
    Patient ID or use `-vtype` to get records with particular visit type and
    Patient ID.

        $ redcap2nacc -f getPtid -ptid $SOME_PATIENT_ID -vnum $SOME_VISIT_NUM -vtype $SOMEVISIT_TYPE <data.csv >data.txt


HOW TO Acquire current-db-subjects.csv for the filters
------------------------------------------------------

This file is a csv that determines which of your center's PTIDs are already
present in NACC's current database using the patient's PTID, the packet type
(ivp or fvp, etc), the visit number, and the status (working or current). In
order to get it, you need to use the contents of
`tools/preprocess/get_subject_list.js`. The script is meant to be run on the
"Finalize Data" page of the NACC UDS3 upload system.

Navigate to "Finalize Data" and right-click anywhere on the page. Select
"Inspect" or "Inspect element" to open the browser's Inspect panel. Click on
the "Console" tab and copy/paste the contents of `get_subject_list.js` into the
console. Then, press the "Enter" or "Return" key on your keyboard. This will
collect all of the PTIDs in your center's Working and Current databases into a
csv called `current-db-subjects.csv` in your Downloads folder. You may then
move it to whatever location you specified in your `nacculator_cfg.ini` file.

The csv is used by the filter_clean_ptid filter to identify and cull all
packets already in NACC's Current database from your input csv. It is used to
make NACCulator run faster for very large databases.


Example Workflow
----------------

Once you have edited the `nacculator_cfg.ini` file with your API token and
desired filters, you can get a filtered CSV file of the raw REDCap data with:

    $ nacculator_filters nacculator_cfg.ini

This will create a run folder labeled with the current date 
(`$run_CURRENT-DATE`) (for example, `run_01-01-2000`) that contains the csv and
each iteration of filter, ending with `final_update.csv`.

Note: The files created by `redcap2nacc` will not be in the run folder created
by `run_filters.py`. They will be in the base directory. The filepaths in the
following commands are modified so that the output is deposited in your
`$run_CURRENT-DATE` folder.

Next, you will need to run the actual `redcap2nacc` program to produce the
fixed width text file for NACC. One type of flag can be used at a time, so the
program must be run once for each type of packet.

    $ redcap2nacc -ivp < $run_CURRENT-DATE/final_Update.csv > $run_CURRENT-DATE/iv_nacc_complete.txt 2> $run_CURRENT-DATE/ivp_errors.txt
    $ redcap2nacc -fvp < $run_CURRENT-DATE/final_Update.csv > $run_CURRENT-DATE/fv_nacc_complete.txt 2> $run_CURRENT-DATE/fvp_errors.txt

This will place the text files (`iv_nacc_complete.txt`) in the run folder
created earlier, as well as a log of the run that contains any found errors
(`ivp_errors.txt`).


Development
-----------

### Quickstart

    $ git clone https://github.com/ctsit/nacculator.git nacculator
    $ cd nacculator
    $ python3 -mvenv venv
    $ source venv/bin/activate
    $ pip install -e .

### Files

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
    Used by developers to update the existing forms.py files as necessary.

* `nacculator_cfg.ini`:
    configuration file for the filters, built from `nacculator_cfg.ini.example`
    in the root `nacculator/` directory.

* `nacc/run_filters.py` and `tools/preprocess/run_filters.sh`:
    pulls data from REDCap based on the settings found in `nacculator_cfg.ini`
    (for .py) and `filters_config.cfg` (for .sh). Supports exporting data from multiple REDCap projects by adding a comma-delimited list of tokens without spaces e.g., `token=token1,token2` to `token` in the `nacculator_cfg.ini` config file.


### Testing

To run all the tests:

    $ python3 -m unittest


To run only the tests in a specific file:

    $ python3 tests/test_$SPECIFIC_FILE.py


### Generating Forms

**Warning: the generator is currently broken due to changes in the CSV format.**

You only need to generate forms when there are new DEDs from NACC. The
NACCulator install includes the current forms automatically.

Before running the generator, read the warnings in `./nacc/uds3/ivp/forms.py`
first.

    $ python3 tools/generator.py tools/uds3/ded/csv/ >nacc/uds3/ivp/forms.py
    $ edit nacc/uds3/ivp/forms.py

_Note: execute `generator.py` from the same folder as the `corrected`
folder, which should contain any "corrected" DEDs._

### Resources

* UDS3 forms: https://www.alz.washington.edu/NONMEMBER/UDS/DOCS/VER3/UDS3csvded.html
* NACC forms and documentation: https://www.alz.washington.edu/NONMEMBER/NACCFormsAndDoc.html
* UDS submission site: https://www.alz.washington.edu/MEMBER/sitesub.htm
