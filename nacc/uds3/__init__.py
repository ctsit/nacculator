###############################################################################
# Copyright 2015-2023 University of Florida. All rights reserved.
# This file is part of UF CTS-IT's NACCulator project.
# Use of this source code is governed by the license found in the LICENSE file.
###############################################################################

# nacc.uds3
import decimal


class _UdsType(object):
    """
    This class is used for "Field" object setup. Fields can have either "Char"
    or "Num" types. This class asserts that the object 1) has a length longer
    than 0, 2) has a string as its value, and 3) assigns those length and value
    attributes to the object.
    """
    def __init__(self, length):
        assert length > 0
        self.length = length

    def __call__(self, *args, **kwargs):
        value = args[0] if len(args) > 0 else None
        self.val = str(value if value is not None else "")
        self.val = self.val.ljust(self.length, ' ')
        return self.val

    def __eq__(self, other):
        return self.__class__ == other.__class__ and \
               self.length == other.length and self.val == other.val


class Char(_UdsType):
    """
    Char fields can have any characters besides ' " & or % (and these forbidden
    characters are checked for later)
    """
    pass


class Num(_UdsType):
    """
    Num fields must be a number (either integer or decimal depending on the
    field)
    """
    def __call__(self, *args, **kwargs):
        value = args[0] if len(args) > 0 else None
        try:
            # check to see if value is a number
            if value is not None and value != "":
                decimal.Decimal(value)
            return super(Num, self).__call__(value)
        except ValueError:
            # just re-raise the error for now
            raise


UDS3_TYPES = {'Num': Num, 'Char': Char}


class Field(object):
    """
    Base class for a field. Contains all metadata pertaining to that field:
    fieldname, whether it's a number or character, length of the field and
    which columns in the output text that the field should occupy, the range of
    values allowed, whether there are any exact values allowed such as error
    codes outside of the normal range, blanking rules, and the data value.
    """
    def __init__(self, name, typename, position, length, inclusive_range=None,
                 allowable_values=None, blanks=None, value=None):
        assert allowable_values is None or \
               allowable_values is not isinstance(allowable_values, str)

        self.name = name
        self.typename = typename
        self.udstype = UDS3_TYPES[typename](length)
        self.position = position
        self.length = length
        self.inclusive_range = inclusive_range
        # get the canonical representation for allowable values, but filter out
        # empty strings first
        self.allowable_values = [self.udstype(v)
                                 for v in [
                                     _f for _f in allowable_values if _f]]
        self.blanks = blanks or []
        self.val = value

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return self.value == self.udstype(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    @property
    def value(self):
        return self.udstype(self.val)

    @value.setter
    def value(self, val):
        def out_of_range(v):
            d = decimal.Decimal(v)
            return d < int(self.inclusive_range[0]) or \
                d > int(self.inclusive_range[1])

        if self.allowable_values:
            if val is None:
                pass
            elif isinstance(val, str) and str(val).strip() == "":
                pass
            else:
                # val can be None, but if it isn't AND we are restricted to
                # certain values, then we must check that the canonical form of
                # val is in the allowable list
                canonical = self.udstype(val)
                if canonical not in self.allowable_values:
                    if not isinstance(self.udstype, Num) or \
                            out_of_range(canonical):
                        raise ValueError('"%s" is either not a number or out'
                                         ' of range for %s' % (val, self.name))

        else:
            if val is None:
                pass
            elif isinstance(val, str) and str(val).strip() == "":
                pass
            elif isinstance(self.udstype, Char):
                pass
            else:
                # val can be None, but if it isn't, and we are NOT restricted
                # to certain values (only an allowable range of values),
                # then we need to check that the value is within that range
                canonical = self.udstype(val)
                assert self.inclusive_range
                if out_of_range(canonical):
                    raise ValueError(
                        '"%s" is outside of the allowable range for %s'
                        ' : %s - %s' % (
                            val, self.name, self.inclusive_range[0],
                            self.inclusive_range[1]))
        self.val = val


class FieldBag(object):
    """ Base class for Forms; aka a bag of Fields """
    def __init__(self):
        self.fields = dict()

    def __getattr__(self, name):
        key = self.__find_key(name)
        if key:
            return self.fields[key]

        raise AttributeError(name)

    def __setattr__(self, name, value):
        if name in self.__dict__ or name == "fields":
            object.__setattr__(self, name, value)
            return

        key = self.__find_key(name)
        if key:
            self.fields[key].value = value
        else:
            raise AttributeError(name)

    def __str__(self):
        return str(self.write())

    def __find_key(self, key):

        if key in self.fields:
            return key

        key = key.upper()
        if key in self.fields:
            return key

        return None

    @property
    def form_name(self):
        return self.__class__.__name__.replace("Form", "")

    def write(self, buf=None):
        if buf is None:
            last = max(list(self.fields.values()), key=lambda f: f.position[1])
            buf = bytearray(' ' * last.position[1], 'ascii')

        orig_buf_size = len(buf)

        for field in list(self.fields.values()):
            value = field.value
            start, end = field.position
            formid = ''
            try:
                formid = ' in form %s' % (self.fields['FORMID'].value)
            except KeyError:
                pass
            start -= 1
            end -= 1
            assert len(value) == end - start + 1, \
                'Length of field %s%s with value "%s" is not valid. %s != %s' % (field.name, formid, value, len(value), end - start + 1)
            buf[start:start + len(value)] = value.encode('ascii')

        assert len(buf) == orig_buf_size, field.name + ": buffer changed size!"
        return buf.decode('ascii')
