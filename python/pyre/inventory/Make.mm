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
PACKAGE = inventory

BUILD_DIRS = \
    odb \
    pml \
    properties \
    validators \

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
    Configurable.py \
    Descriptor.py \
    Facility.py \
    Interface.py \
    Inventory.py \
    Notary.py \
    Property.py \
    Trait.py \
    __init__.py \


export:: export-package-python-modules
	BLD_ACTION="export" $(MM) recurse

# version
# $Id: Make.mm,v 1.1.1.1 2006-11-27 00:10:01 aivazis Exp $

# End of file
