NACCulator
==========

[![DOI](https://zenodo.org/badge/20501/ctsit/nacculator.svg)](https://zenodo.org/badge/latestdoi/20501/ctsit/nacculator)

Converts a CSV data file exported from REDCap into the NACC's UDS3 fixed-width
format.

_Note:_ NACCulator _**requires Python 3.**_


HOW TO Convert from REDCap to NACC
----------------------------------

Once the project data is exported from REDCap to the CSV file `data.csv`, run:

    $ pip3 install git+https://github.com/ctsit/nacculator.git
    $ redcap2nacc <data.csv >data.txt

This command will work only in the simplest case; UDS3 IVP data only.
If there are no errors, then submit the `data.txt` file to NACC.

_Note: output is written to `STDOUT`; errors are written to `STDERR`; input is
expected to be from `STDIN` unless a file is specified using the `-file` flag._


### Usage

    $ redcap2nacc -h
    usage: redcap2nacc [-h]
                       [-fvp | -ivp | -tfp | -np | -m | -csf | -f {cleanPtid,replaceDrugId,fixHeaders,fillDefault,updateField,removePtid,removeDateRecord,getPtid}]
                       [-lbd | -ftld] [-file FILE] [-meta FILTER_META] [-ptid PTID]
                       [-vnum VNUM] [-vtype VTYPE]

    Process redcap form output to nacculator.

    optional arguments:
      -h, --help            show this help message and exit
      -fvp                  Set this flag to process as fvp data
      -ivp                  Set this flag to process as ivp data
      -tfp                  Set this flag to process as telephone follow-up data
      -np                   Set this flag to process as np data
      -m                    Set this flag to process as m data
      -csf                  Set this flag to process as NACC BIDSS CSF data
      -f {cleanPtid,replaceDrugId,fixHeaders,fillDefault,updateField,removePtid,removeDateRecord,getPtid}, --filter {cleanPtid,replaceDrugId,fixHeaders,fillDefault,updateField,removePtid,removeDateRecord,getPtid}
                              Set this flag to process the filter
      -lbd                  Set this flag to process as Lewy Body Dementia data
      -ftld                 Set this flag to process as Frontotemporal Lobar                                     Degeneration data
      -file FILE            Path of the csv file to be processed.
      -meta FILTER_META     Input file for the filter metadata (in case -filter is
                              used)
      -ptid PTID            Ptid for which you need the records
      -vnum VNUM            Ptid for which you need the records
      -vtype VTYPE          Ptid for which you need the records


**Example** - Process a Neuropathology form:

    $ redcap2nacc -np -file data.csv >data.txt

**Example** - Processing LBD Follow-up visit packets:

    redcap2nacc -lbd -fvp -file data.csv >data.txt

Both LBD and FTLD forms can have IVP or FVP arguments.

**Example** - Run data through the `cleanPtid` filter:

    $ redcap2nacc -f cleanPtid -meta nacculator_cfg.ini <data.csv >data.txt


HOW TO Filter Data Using NACCulator
-----------------------------------

If your data is not clean enough to be processed by NACCulator, there are some
built in functions to clean (read transform) the data.

In order to properly use the filters, the first step is to check and validate
that `nacculator_cfg.ini` has the proper settings for the filter to run.
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
  num found in the passed meta file will be discarded in the output file.

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

  This filter is used to update non blank fields. Currently, only `adcid` is
  updated to 41.

* **removePtid**

  **Filter config required**
  This filter requires a section in the config called `filter_remove_ptid` with
  a single key called `ptid_format`. The value for that key is a regex string
  to match ptids that are to be kept.

  This filter is used to remove ptids that may have a different set of ids for a
  different study, or help limit which ids show up in the final result.

      config:
      ptid_format: 11\d.*

* **removeDateRecord**

  This filter is used to remove records who may be missing visit dates. It
  searches for rows missing the visit day, month, or year. If any of those
  fields are missing, it removes the row.

* **getPtid**

    This filter is used to get information about a single PatientID.
    You need to use the `-ptid` flag to specify the patient ID.
    You can use the `-vnum` to get the records with particular visit number and
    Patient ID or use `-vtype` to get records with particular visit type and
    Patient ID.

        $ redcap2nacc -f getPtid -ptid $SOME_PATIENT_ID -vnum $SOME_VISIT_NUM -vtype $SOMEVISIT_TYPE <data.csv >data.txt


Example Workflow
----------------

Once you have edited the `nacculator_cfg.ini` file with your API token and
desired filters, you can get a filtered CSV file of the REDCap data with:

    $ python3 run_filters.py nacculator_cfg.ini

This will create a run folder (`$run_folder`) with the current date that
contains the csv and each iteration of filter, ending with `final_update.csv`.

Next, you will need to split apart the IVP and FVP visits:

    $ bash split_ivp_fvp.sh $run_folder/final_update.csv

The resulting files will not be in the run folder created by `run_filters.py`.
They will be in the base directory. You can move them if you would like to, but
you will need to modify the filepaths in the following commands.

Next, you will need to run the actual `redcap2nacc` program to produced the
fixed width text file for NACC. As you have split the IVP and FVP visits, you
will run the program twice, using each flag once.

    $ redcap2nacc -ivp <initial_visits.csv >$run_folder/iv_nacc_complete.txt 2>$run_folder/ivp_errors.txt
    $ redcap2nacc -fvp <followup_visits.csv >$run_folder/fv_nacc_complete.txt 2>$run_folder/fvp_errors.txt

This will place the text files in the run folder created earlier, as well as a
log of the run which will have any errors encountered.


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

* `tools/preprocess/run_filters.py` and `tools/preprocess/run_filters.sh`:
    pulls data from REDCap based on the settings found in `nacculator_cfg.ini`
    (for .py) and `filters_config.cfg` (for .sh).


### Generating New Forms

**Warning: read the warnings in the `./nacc/uds3/ivp/forms.py` first!**

_Note: executing `generator.py` from within tools is an important step as the
script assumes any corrected DEDs are stored under a folder in the current
working directory called `corrected`._

    $ python3 tools/generator.py tools/uds3/ded/csv/ >nacc/uds3/ivp/forms.py
    $ edit nacc/uds3/ivp/forms.py


### Testing

To run all the tests:

    $ make tests


To run only the tests in a file:

    $ python3 tests/WHICHEVER_test.py


### Resources

* UDS3 FVP forms: https://www.alz.washington.edu/NONMEMBER/UDS/DOCS/VER3/
