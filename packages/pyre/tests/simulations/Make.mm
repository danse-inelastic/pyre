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

# FIXME: For some reason it doesn't want to export simulation.py

PROJECT = pyre
PACKAGE = tests/simulations

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
    simulation.py \
    __init__.py

export:: export-package-python-modules


#PROJ_TESTS = \

#PROJ_TIDY += *.log solver-?????
#PROJ_LIBRARIES =

#--------------------------------------------------------------------------
#

#all: $(PROJ_TESTS)

#test:
#	for test in $(PROJ_TESTS) ; do $${test}; done

# version
# $Id: Make.mm,v 1.1.1.1 2006-11-27 00:10:13 aivazis Exp $

# End of file
