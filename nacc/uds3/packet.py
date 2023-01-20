###############################################################################
# Copyright 2015-2023 University of Florida. All rights reserved.
# This file is part of UF CTS-IT's NACCulator project.
# Use of this source code is governed by the license found in the LICENSE file.
###############################################################################


class Packet(list):
    """
    A Packet is a collection of Forms, each with a unique FormID. The forms
    present depend on the packet type (determined by flag argument when
    running the program)- UDS, LBD, FTLD, Milestone, Neuropath, COVID, and so
    on.

    This class makes it convenient to access any field and its metadata. Each
    field is uniquely named according to NACC's Data Element Dictionary,
    regardless of which form they are in (with the exception of A4D, which is a
    repeating form).
    """

    def __init__(self):
        self._cache = dict()

    def __getitem__(self, key):
        """
        Searches through each form in the packet for the fieldname, or `key`

        Note: you cannot access fields in A4D in this manner since there is no
        guarantee there will only be one; a KeyError will be raised.

        Example:
            packet['RESTTRL'] is equivalent to:
            packet.__getitem__('RESTTRL')
        """
        if key in self._cache:
            return self._cache[key]

        for form in self:
            if key in form.fields:
                if "A4D" in str(form.__class__):
                    raise KeyError("Form A4D is unsupported")
                self._cache[key] = form.fields[key]
                return self._cache[key]

        raise KeyError(key)
