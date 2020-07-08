NACCulator
==========

[![DOI](https://zenodo.org/badge/20501/ctsit/nacculator.svg)](https://zenodo.org/badge/latestdoi/20501/ctsit/nacculator)

Converts a CSV data file exported from REDCap into the NACC's UDS3 fixed-width
format.

_Note:_ NACCulator _**requires Python 3.**_


HOW TO Convert from REDCap to NACC
----------------------------------

To install NACCulator, run:

    $ pip3 install git+https://github.com/ctsit/nacculator.git

Once the project data is exported from REDCap to the CSV file `data.csv`, run:

    $ redcap2nacc <data.csv >data.txt

This command will work only in the simplest case; UDS3 IVP data only.
Nacculator will automatically skip PTIDs with errors, so the output `data.txt`
file will be ready to submit to NACC.
In order to properly filter the data in the csv, nacculator is expecting that
REDCap visits (denoted by `redcap_event_name`) contain certain keywords:
    "initial_visit" for initial visit packets,
    "followup_visit" for all followups,
    "milestone" for milestone packets,
    "neuropath" for neuropathology packets,
    "telephone" for telephone followup packets

_Note: output is written to `STDOUT`; errors are written to `STDERR`; input is
expected to be from `STDIN` (the command line) unless a file is specified using
the `-file` flag._


### Usage

    $ redcap2nacc -h
    usage: redcap2nacc [-h]
                       [-fvp | -ivp | -tfp | -np | -m | -csf | -f {cleanPtid,replaceDrugId,fixHeaders,fillDefault,updateField,removePtid,removeDateRecord,getPtid}]
                       [-lbd | -ftld] [-file FILE] [-meta FILTER_META] [-ptid PTID]
                       [-vnum VNUM] [-vtype VTYPE]

    Process redcap form output to nacculator.

    optional arguments:
      -h, --help            show this help message and exit
      -fvp                  Set this flag to process as FVP data
      -ivp                  Set this flag to process as IVP data
      -tfp                  Set this flag to process as Telephone Followup Packet data
      -np                   Set this flag to process as Neuropathology data
      -m                    Set this flag to process as Milestone data
      -csf                  Set this flag to process as NACC BIDSS CSF data

      -f {cleanPtid,replaceDrugId,fixHeaders,fillDefault,updateField,removePtid,removeDateRecord,getPtid}, --filter {cleanPtid,replaceDrugId,fixHeaders,fillDefault,updateField,removePtid,removeDateRecord,getPtid}
                              Set this flag to process the filter
      -lbd                  Set this flag to process as Lewy Body Dementia data (FORMVER = 3)
      -lbdsv                Set this flag to process as Lewy Body Dementia short version data (FORMVER = 3.1)
      -ftld                 Set this flag to process as Frontotemporal Lobar Degeneration data

      -file FILE            Path of the csv file to be processed.
      -meta FILTER_META     Input file for the filter metadata (in case -filter is used)
      -ptid PTID            Ptid for which you need the records
      -vnum VNUM            Ptid for which you need the records
      -vtype VTYPE          Ptid for which you need the records


**Example** - Process a Neuropathology form:

    $ redcap2nacc -np -file data.csv >data.txt

**Example** - Processing LBD Follow-up visit packets:

    redcap2nacc -lbd -fvp -file data.csv >data.txt

Both LBD / LBDSV and FTLD forms can have IVP or FVP arguments.

**Example** - Run data through the `cleanPtid` filter:

    $ redcap2nacc -f cleanPtid -meta nacculator_cfg.ini <data.csv >data.txt


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
If the filter requires the config, it must be passed with the `-meta` flag like
the example above shows.

* **cleanPtid**

  **Filter config required**
  This filter requires a section in the config called `filter_clean_ptid`. This
  section will contain a single key `filepath` which will point to a csv file
  of ptids to be removed. All the records whose ptid with same packet and visit
  num found in the passed meta file will be discarded in the output file. This
  filter also removes events that lack a visit number in REDCap.

  Example meta file:

      Patient ID,Packet type,Visit Num,Status
      110001,I,1,Current
      110001,M,M1,Current
      110003,I,001,Current
      110003,F,002,Current

* **replaceDrugId**

  This filter replaces the first character of non empty fields of columns
  `drugid_1` to `drugid_30` with character "**d**".

  This filter does not require any meta data file as of now.

* **fixHeaders**

  **Filter config required**
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


* **fillDefault**

  This filter is used to set some predefined fields to their corresponding
  predefined values. Below are the current defaults :

      nogds    -> 0
      formver  -> 3

  *If field is blank, it will be updated to default value.*

* **updateField**

  This filter is used to update fields that already had a value in the REDCap
  export. Currently, only `adcid` is updated.

* **removePtid**

  **Filter config required**
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


Example Workflow
----------------

Once you have edited the `nacculator_cfg.ini` file with your API token and
desired filters, you can get a filtered CSV file of the raw REDCap data with:

    $ nacculator_filters nacculator_cfg.ini

This will create a run folder labeled with the current date 
(`$run_CURRENT-DATE`) (for example, `run_01-01-2000`) that contains the csv and
each iteration of filter, ending with `final_update.csv`.

The resulting files will not be in the run folder created by `run_filters.py`.
They will be in the base directory. The filepaths in the following commands are
modified so that the output is deposited in your `$run_CURRENT-DATE` folder.

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
    (for .py) and `filters_config.cfg` (for .sh).


### Testing

To run all the tests:

    $ python3 -m unittest


To run only the tests in a file:

    $ python3 tests/WHICHEVER_test.py


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
