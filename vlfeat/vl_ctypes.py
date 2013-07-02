from ctypes import (cdll, sizeof, Structure,
    c_float, c_double,
    c_int, c_int8, c_int16, c_int32, c_int64,
    c_uint, c_uint8, c_uint16, c_uint32, c_uint64)
from ctypes.util import find_library

import numpy as np

import os
from . import download
_loc = os.path.join(os.path.dirname(os.path.abspath(download.__file__)),
                    download.pick_platform()[1])
try:
    LIB = cdll[_loc]
except OSError:
    _loc = find_library('vl')
    try:
        LIB = cdll[_loc]
    except (OSError, TypeError):  # TypeError if _loc is None
        msg = ("Can't find vlfeat library. "
               "Run python -m vlfeat.download to fetch.")
        raise ImportError(msg)


################################################################################

# Enumeration class
# based on http://code.activestate.com/recipes/576415-ctype-enumeration-class/

class EnumMeta(type(c_uint)):
    def __new__(cls, name, bases, classdict):
        # figure out which members of the class are enum items
        _members = {}
        _rev_members = {}
        for k, v in classdict.iteritems():
            if not k.startswith('_'):
                try:
                    c_uint(v)
                except TypeError:
                    pass
                else:
                    if not k == k.upper():
                        raise ValueError("Enum values must be all-uppercase")

                    classdict[k] = _members[k] = v
                    _rev_members[v] = k

        # construct the class
        classdict['_members'] = _members
        classdict['_rev_members'] = _rev_members
        the_type = type(c_uint).__new__(cls, name, bases, classdict)

        # now that the class is finalized, switch members to be of the class
        for k, v in _members.iteritems():
            as_class = the_type(v)
            the_type._members[k] = as_class
            setattr(the_type, k, as_class)

        return the_type

    def __contains__(self, value):
        return value in self._members.itervalues()

    def __repr__(self):
        return "<Enumeration %s>" % self.__name__


class Enum(c_uint):
    __metaclass__ = EnumMeta

    def __init__(self, value):
        if isinstance(value, self.__class__):
            value = value.value
        else:
            try:
                value = self._members[value.upper()].value
            except (AttributeError, KeyError):
                if value not in self._rev_members:
                    raise ValueError("invalid %s value %r" %
                            (self.__class__.__name__, value))

        super(Enum, self).__init__(value)

    @property
    def name(self):
        try:
            return self._rev_members[self.value]
        except KeyError:
            raise ValueError("Bad %r value %r" % (self.__class__, self.value))

    @classmethod
    def from_param(cls, param):
        if hasattr(param, 'upper'):
            s = param.upper()
            try:
                return getattr(cls, s)
            except AttributeError:
                raise ValueError("Bad %s value %r" % (cls.__name__, param))
        return param

    def __repr__(self):
        return "<member %s=%d of %r>" % (self.name, self.value, self.__class__)


# XXX: here because otherwise __init__ doesn't seem to get called
def returns_enum(enum_subclass):
    def inner(value):
        return enum_subclass(value)
    return inner

################################################################################
### Custom structure class, with defaults and nicer enumeration support

# extremely loosely based on code from pyflann.flann_ctypes

_identity = lambda x: x
class CustomStructure(Structure):
    _defaults_ = {}
    __enums = {}

    def __init__(self, *args, **kwargs):
        self.__enums = dict((f, t) for f, t in self._fields_
                            if issubclass(t, Enum))
        for field, val in self._defaults_.iteritems():
            setattr(self, field, val)

        Structure.__init__(self, *args, **kwargs)

    def __setattr__(self, k, v):
        class_wrapper = self.__enums.get(k, _identity)
        super(CustomStructure, self).__setattr__(k, class_wrapper(v))

    def update(self, **vals):
        for k, v in vals.iteritems():
            setattr(self, k, v)

################################################################################

# TODO actually figure out if it's built LP64 or ILP64 or whatever
vl_size = c_uint64
vl_index = c_int64


class vl_type(Enum):
    FLOAT = 1
    DOUBLE = 2
    INT8 = 3
    UINT8 = 4
    INT16 = 5
    UINT16 = 6
    INT32 = 7
    UINT32 = 8
    INT64 = 9
    UINT64 = 10

c_to_vl_types = {
    c_float: vl_type.FLOAT,
    c_double: vl_type.DOUBLE,
    c_int8: vl_type.INT8,
    c_uint8: vl_type.UINT8,
    c_int16: vl_type.INT16,
    c_uint16: vl_type.UINT16,
    c_int32: vl_type.INT32,
    c_uint32: vl_type.UINT32,
    c_int64: vl_type.INT64,
    c_uint64: vl_type.UINT64,
}


np_to_c_types = {}
c_to_np_types = {}
_dtypes = {
    'i': (c_int, c_int8, c_int32, c_int64),
    'u': (c_uint, c_uint8, c_uint32, c_uint64),
    'f': (c_float, c_double),
}
for t, c_types in _dtypes.items():
    for c_type in c_types:
        dtype = np.dtype('<{}{}'.format(t, sizeof(c_type)))
        np_to_c_types[dtype] = c_type
        c_to_np_types[c_type] = dtype
del t, c_types, c_type, dtype

vl_epsilon_f = 2 ** -23  # smallest representable single
