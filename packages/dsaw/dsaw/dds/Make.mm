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
PACKAGE = dds

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
	$(RM) $(RMFLAGS) odb/prefix.py odb/prefix-template.pyc

clean::
	BLD_ACTION="clean" $(MM) recurse

distclean::
	BLD_ACTION="distclean" $(MM) recurse

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
	AbstractDataPathMapper.py \
	AbstractFileRegistry.py \
	DistributedDataStore.py \
	FileMirror.py \
	Node.py \
	SimpleDataPathMapper.py \
	SimpleFileRegistry.py \
	__init__.py \
	_debug.py \


export:: export-package-python-modules
	BLD_ACTION="export" $(MM) recurse

# version
# $Id$

# End of file
