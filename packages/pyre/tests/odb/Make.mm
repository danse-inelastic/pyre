# -*- Makefile -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2005 All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PROJECT = pyre
PACKAGE = tests/odb

RECURSE_DIRS = \
    contacts \

all: export

tidy::
	BLD_ACTION="tidy" $(MM) recurse


#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
    __init__.py

export:: export-package-python-modules
	BLD_ACTION="export" $(MM) recurse


#PROJ_TESTS = \


#PROJ_CLEAN =
#PROJ_LIBRARIES =

#--------------------------------------------------------------------------
#

#all:
#	BLD_ACTION="all" $(MM) recurse

#clean::
#	BLD_ACTION="clean" $(MM) recurse

#distclean::
#	BLD_ACTION="clean" $(MM) recurse

#tidy::
#	BLD_ACTION="tidy" $(MM) recurse


# version
# $Id: Make.mm,v 1.1.1.1 2006-11-27 00:10:13 aivazis Exp $

# End of file
