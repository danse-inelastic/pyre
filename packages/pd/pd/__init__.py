#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                             Michael A.G. Aivazis
#                      California Institute of Technology
#                      (C) 1998-2005  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

"""proposed changes:
1) change _reference to ReferredEntity?
2)  

"""


def bigint(**kwds):
    from BigInt import BigInt
    return BigInt(**kwds)


def boolean(**kwds):
    from Boolean import Boolean
    return Boolean(**kwds)


def char(**kwds):
    from Char import Char
    return Char(**kwds)


def date(**kwds):
    from Date import Date
    return Date(**kwds)


def double(**kwds):
    from Double import Double
    return Double(**kwds)


def doubleArray(**kwds):
    from DoubleArray import DoubleArray
    return DoubleArray(**kwds)


def integer(**kwds):
    from Integer import Integer
    return Integer(**kwds)


def integerArray(**kwds):
    from IntegerArray import IntegerArray
    return IntegerArray(**kwds)


def interval(**kwds):
    from Interval import Interval
    return Interval(**kwds)


def real(**kwds):
    from Real import Real
    return Real(**kwds)


def ref(**kwds):
    from Reference import Reference
    return Reference(**kwds)


def versatileRef(**kwds):
    from VersatileReference import VersatileReference
    return VersatileReference(**kwds)


def refSet(**kwds):
    from ReferenceSet import ReferenceSet
    return ReferenceSet(**kwds)


def smallint(**kwds):
    from SmallInt import SmallInt
    return SmallInt(**kwds)


def time(**kwds):
    from Time import Time
    return Time(**kwds)


def timestamp(**kwds):
    from Timestamp import Timestamp
    return Timestamp(**kwds)


def str(**kwds):
    from VarChar import VarChar
    return VarChar(**kwds)


def strArray(**kwds):
    from VarCharArray import VarCharArray
    return VarCharArray(**kwds)

# End of file 
