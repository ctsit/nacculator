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


HOWTO Convert from REDCap to NACC
---------------------------------

Once the project data is exported from REDCap to the CSV file `data.csv`, run:

    $ pip install nacculator
    $ redcap2nacc < data.csv > data.nacc

Or, if you're using the source code:

    $ PYTHONPATH=. ./nacc/redcap2nacc.py < data.csv > data.nacc
   
Or, if you need the output of only neuropathology form:
 
    $ PYTHONPATH=. ./nacc/redcap2nacc.py -nponly < data.csv > data.nacc
    
The program accepts two arguments -file and -nponly. Both are optional and can be used as below:

    $ PYTHONPATH=. ./nacc/redcap2nacc.py  -nponly -file data.csv > data.nacc

_Note: output is written to `STDOUT`; errors are written to `STDERR`; input can
be `STDIN` or the first argument passed to `redcap2nacc`._

If there are no errors, then submit the `data.nacc` file to NACC.


HOWTO Generate New Forms
------------------------

_Note: executing `generator.py` from within tools is an important step as the
script assumes any corrected DEDs are stored under a folder in the current
working directory called `corrected`._

**Warning: read the warnings in the current `./nacc/uds3/ivp/forms.py` first.**

    $ cd tools
    $ PYTHONPATH=.. ./generator.py uds3/ded/csv/ > ../nacc/uds3/ivp/forms.py
    $ edit ../nacc/uds3/ivp/forms

