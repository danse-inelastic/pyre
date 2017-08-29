#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                             Michael A.G. Aivazis
#                      California Institute of Technology
#                      (C) 1998-2008  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


def connect(database, wrapper=None, **kwds):
    name2mod = {
        None: 'Psycopg',
        'psycopg': 'Psycopg',
        'psycopg2': 'Psycopg2',
        'sqlite': 'SQLite',
        }
    mod = name2mod.get(wrapper)
    if not mod:
        import journal
        journal.error("pyre.db").log("{0!r}: unknown db wrapper type".format(wrapper))
        return None

    package = 'pyre.db'
    module = __import__(package+'.'+mod, {}, {}, [''])
    factory = getattr(module, mod)
    return factory(database, **kwds)



def bigint(**kwds):
    from BigInt import BigInt
    return BigInt(**kwds)


def boolean(**kwds):
    from Boolean import Boolean
    return Boolean(**kwds)

def booleanArray(**kwds):
    from BooleanArray import BooleanArray
    return BooleanArray(**kwds)

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


def reference(**kwds):
    from Reference import Reference
    return Reference(**kwds)


def smallint(**kwds):
    from SmallInt import SmallInt
    return SmallInt(**kwds)


def tableRegistry():
    from VersatileReference import tableRegistry
    return tableRegistry()


def time(**kwds):
    from Time import Time
    return Time(**kwds)


def timestamp(**kwds):
    from Timestamp import Timestamp
    return Timestamp(**kwds)


def varchar(**kwds):
    from VarChar import VarChar
    return VarChar(**kwds)


def varcharArray(**kwds):
    from VarCharArray import VarCharArray
    return VarCharArray(**kwds)

# version
__id__ = "$Id: __init__.py,v 1.2 2008-04-04 08:37:14 aivazis Exp $"

# End of file 
