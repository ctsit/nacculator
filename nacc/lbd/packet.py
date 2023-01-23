###############################################################################
# Copyright 2015-2023 University of Florida. All rights reserved.
# This file is part of UF CTS-IT's NACCulator project.
# Use of this source code is governed by the license found in the LICENSE file.
###############################################################################


class Packet(list):
    """
    This Packet refers to a collection of LBD or LBD Short Version forms.

    A Packet is a collection of Forms, each with a unique FormID. The forms
    present depend on the packet type (determined by flag argument when
    running the program)- UDS, LBD, FTLD, Milestone, Neuropath, COVID, and so
    on.

    This class makes it convenient to access any field and its metadata. Each
    field is uniquely named according to NACC's Data Element Dictionary,
    regardless of which form they are in.
    """

    def __init__(self):
        self._cache = dict()

    def __getitem__(self, key):
        """
        Searches through each form in the packet for the field, `key`

        Example:
            packet['RESTTRL'] is equivalent to:
            packet.__getitem__('RESTTRL')
        """
        if key in self._cache:
            return self._cache[key]

        raise KeyError(key)
