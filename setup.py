###############################################################################
# Copyright 2015-2020 University of Florida. All rights reserved.
# This file is part of UF CTS-IT's NACCulator project.
# Use of this source code is governed by the license found in the LICENSE file.
###############################################################################

from setuptools import setup, find_packages

VERSION = "1.14.0"

setup(
    name="nacculator",
    version=VERSION,
    author="Taeber Rapczak",
    author_email="taeber@ufl.edu",
    maintainer="UF CTS-IT",
    maintainer_email="ctsit@ctsi.ufl.edu",
    url="https://github.com/ctsit/nacculator",
    license="BSD 2-Clause",
    description="CSV to NACC's UDS3 format converter",
    keywords=["REDCap", "NACC", "UDS", "Clinical data"],
    download_url="https://github.com/ctsit/nacculator/releases/tag/" + VERSION,

    package_dir={'nacc': 'nacc'},
    packages=find_packages(),

    entry_points={
        "console_scripts": [
            "redcap2nacc = nacc.redcap2nacc:main",
            "nacculator_filters = nacc.run_filters:main"
        ]
    },

    install_requires=[
        "PyCap>=2.1.0",
        "pandas>=2.2.0",
        "report_handler @ git+https://git@github.com:/ctsit/report_handler.git@1.3.0"
    ],

    python_requires=">=3.6.0",
)
