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
PACKAGE = tests/ipc

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
    connection.py \
    monitor.py \
    selector.py \
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
# $Id: Make.mm,v 1.1.1.1 2006-11-27 00:10:11 aivazis Exp $

# End of file
