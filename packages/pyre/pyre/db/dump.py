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


def dumps(db, table):
    '''dump a db table to a string.
    The output starts with a line of column names, and then
    all records.
    '''
    colnames = table._columnRegistry.keys()
    records = dumpToStrListIterator(db, table)
    records = list(records)
    
    lines = [colnames] + records
    
    _ = lambda line: '\t'.join(line)
    lines = map(_, lines)
    
    return '\n'.join(lines)


def dumpToStrListIterator(db, table):
    records = db.fetchall(table)

    cols = table._columnRegistry.values()
    converters = map(getConverter, cols)

    for record in records:
        l = []
        for col, converter in zip(cols, converters):
            val = col.__get__(record)
            s = converter(val)
            l.append(s)
            continue
        yield l
        continue
    return


def getConverter(col):
    type = col.__class__.__name__
    candidate = 'convert_' + type
    try:
        converter = eval(candidate)
    except:
        converter = convert_default
    return converter


def convert_default(value): return str(value)
def convert_VarChar(value): return repr(value)
def convert_VarCharArray(value):
    return str(map(convert_VarChar, value))


# version
__id__ = "$Id$"

# End of file 
