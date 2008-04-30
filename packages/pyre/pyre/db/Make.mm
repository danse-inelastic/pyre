# -*- Makefile -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2005  All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PROJECT = pyre
PACKAGE = db


#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
    BigInt.py \
    Boolean.py \
    Char.py \
    Column.py \
    Date.py \
    Double.py \
    DBManager.py \
    Integer.py \
    Interval.py \
    Psycopg.py \
    Psycopg2.py \
    Real.py \
    Schemer.py \
    SmallInt.py \
    Table.py \
    Time.py \
    Timestamp.py \
    VarChar.py \
    __init__.py


export:: export-package-python-modules

# version
# $Id: Make.mm,v 1.2 2008-04-12 08:59:56 aivazis Exp $

# End of file
