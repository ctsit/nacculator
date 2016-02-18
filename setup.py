###############################################################################
# Copyright 2015-2016 University of Florida. All rights reserved.
# This file is part of UF CTS-IT's NACCulator project.
# Use of this source code is governed by the license found in the LICENSE file.
###############################################################################

from setuptools import setup

setup(
    name="NACCulator",
    version="0.1.0",
    packages=["nacc"],
    entry_points={
        "console_scripts": [
            "redcap2nacc = nacc.redcap2nacc:main"
        ]
    },
    author="Taeber Rapczak",
    author_email="taeber@ufl.edu",
    description="CSV to NACC's UDS3 format converter",
    license="BSD 2-Clause",

    url='https://github.com/ctsit/nacculator',
    download_url='https://github.com/ctsit/nacculator/releases/tag/0.1.0',
    keywords=['REDCap', 'NACC', 'UDS', 'Clinical data'],
)
