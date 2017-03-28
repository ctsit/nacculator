###############################################################################
# Copyright 2015-2016 University of Florida. All rights reserved.
# This file is part of UF CTS-IT's NACCulator project.
# Use of this source code is governed by the license found in the LICENSE file.
###############################################################################

from setuptools import setup, find_packages

VERSION="0.2.4"

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

    package_dir = {'nacc': 'nacc'},
    packages = find_packages(),

    entry_points={
        "console_scripts": [
            "redcap2nacc = nacc.redcap2nacc:main"
        ]
    }
)
