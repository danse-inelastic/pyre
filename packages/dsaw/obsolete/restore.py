#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                 Jiao  Lin
#                      California Institute of Technology
#                      (C) 2005-2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


def loads(s, db, table, idonly=False, update=False):
    '''load a db table from a string.
    The format of that string is in dsaw.db.dump
    '''
    lines = s.splitlines()
    colnames = lines[0].split('\t')
    recordlines = lines[1:]

    if update:
        f = db.updateRecord
    else:
        f = db.insertRow

    if idonly and update: raise RuntimeError

    failed = []

    if idonly:
        idcol_index = colnames.index('id')
        idcol = table._columnRegistry['id']

        for line in recordlines:
            values = line.split('\t')
            try:
                id = values[idcol_index]
            except:
                raise RuntimeError, 'values: %s, idcol_index: %s' % (values, idcol_index)

            converter = getConverter(idcol)
            id = converter(id)

            row = table()
            row.id = id
            f(row)
            continue
    else:
        cols = [table._columnRegistry[colname] for colname in colnames]
        converters = map(getConverter, cols)
        
        for line in recordlines:
            values = line.split('\t')
            row = table()
            for col, converter, value in zip(cols, converters, values):
                value = converter(value)
                col.__set__(row, value)
                continue
            try:
                f(row)
            except Exception:
                import traceback
                failed.append( (row, traceback.format_exc()) )
            continue

    db.commit()
    return failed


def getConverter(col):
    type = col.__class__.__name__
    candidate = 'convert_' + type
    try:
        converter = eval(candidate)
    except:
        converter = convert_default
    return converter


def convert_default(value): return value
def convert_VarChar(value): return eval(value)
def convert_VarCharArray(value): return map(eval, eval(value))
from _reference import reference
separator = reference.separator
del reference
def convert_Reference(value):
    if value.find(separator) != -1: return value.split(separator)[1]
    if value == 'None': return None
    return value
def convert_VersatileReference(value):
    if value == 'None' : return None
    return value


# version
__id__ = "$Id$"

# End of file 
