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
PACKAGE = tests

RECURSE_DIRS = \
    applications \
    components \
    db \
    geometry \
    idd \
    inventory \
    ipa \
    ipc \
    libpyre \
    odb \
    services \
    simulations \
    util \
    weaver \

#--------------------------------------------------------------------------
#

all: export


tidy::
	BLD_ACTION="tidy" $(MM) recurse


#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
    run.py \
    __init__.py

export:: export-package-python-modules
	BLD_ACTION="export" $(MM) recurse


#all:
#	BLD_ACTION="all" $(MM) recurse

#clean::
#	BLD_ACTION="clean" $(MM) recurse

#distclean::
#	BLD_ACTION="clean" $(MM) recurse

#tidy::
#	BLD_ACTION="tidy" $(MM) recurse

# version
# $Id: Make.mm,v 1.1.1.1 2006-11-27 00:10:10 aivazis Exp $

# End of file
