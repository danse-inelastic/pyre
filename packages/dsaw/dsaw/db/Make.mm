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

PROJECT = dsaw
PACKAGE = db

BUILD_DIRS = \
	components \

OTHER_DIRS = \

RECURSE_DIRS = $(BUILD_DIRS) $(OTHER_DIRS)

#--------------------------------------------------------------------------
#

all: export
	BLD_ACTION="export" $(MM) recurse

tidy::
	BLD_ACTION="tidy" $(MM) recurse

clean::
	BLD_ACTION="clean" $(MM) recurse

distclean::
	BLD_ACTION="distclean" $(MM) recurse

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
	BackReference.py \
	Column.py \
	DBManager.py \
	GloballyReferrable.py \
	Pickler.py \
	QueryProxy.py \
	Reference.py \
	ReferenceSet.py \
	Schemer.py \
	Table.py \
	Table2SATable.py \
	TableRegistry.py \
	Time.py \
	Unpickler.py \
	VersatileReference.py \
	WithID.py \
	__init__.py \
	_reference.py \
	_referenceset.py \
	_referencetypes.py \
	_system_tables.py \


export:: export-package-python-modules
	BLD_ACTION="export" $(MM) recurse

# version
# $Id$

# End of file
