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

PROJECT = pd
PACKAGE = pd


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
	DoubleArray.py \
	DBManager.py \
	Integer.py \
	IntegerArray.py \
	Interval.py \
	Psycopg.py \
	Psycopg2.py \
	Real.py \
	Schemer.py \
	SmallInt.py \
	SQLite.py \
	Table.py \
	Time.py \
	Timestamp.py \
	VarChar.py \
	VarCharArray.py \
	__init__.py \
	dump.py \


export:: export-package-python-modules

# version
# $Id: Make.mm,v 1.2 2008-04-12 08:59:56 aivazis Exp $

# End of file
