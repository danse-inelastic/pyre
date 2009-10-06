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
PACKAGE = tests/inventory

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
    array.py \
    bool.py \
    component.py \
    curator.py \
    infile.py \
    inventory.py \
    list.py \
    logicals.py \
    odb.py \
    outfile.py \
    trait.py \
    vectors.py \
    __init__.py

export:: export-package-python-modules


#PROJ_TESTS = \

#PROJ_LIBRARIES =

#--------------------------------------------------------------------------
#

#all: $(PROJ_TESTS)

#test:
	for test in $(PROJ_TESTS) ; do $${test}; done

# version
# $Id: Make.mm,v 1.1.1.1 2006-11-27 00:10:10 aivazis Exp $

# End of file
