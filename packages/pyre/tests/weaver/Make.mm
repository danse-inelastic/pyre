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
PACKAGE = tests/weaver

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
    languages.py \
    mills.py \
    __init__.py

export:: export-package-python-modules


#PROJ_TESTS = \

#PROJ_CLEAN =
#PROJ_LIBRARIES =

#--------------------------------------------------------------------------
#

#all: tidy

#test:
#	for test in $(PROJ_TESTS) ; do $${test}; done

# version
# $Id: Make.mm,v 1.1.1.1 2006-11-27 00:10:13 aivazis Exp $

# End of file
