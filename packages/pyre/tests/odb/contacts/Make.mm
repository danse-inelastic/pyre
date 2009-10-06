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
PACKAGE = tests/odb/contacts

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
    10000.odb \
    10001.odb \
    Person.py \
    raw.py \
    __init__.py

export:: export-package-python-modules


#all: tidy


# version
# $Id: Make.mm,v 1.1.1.1 2006-11-27 00:10:13 aivazis Exp $

# End of file
