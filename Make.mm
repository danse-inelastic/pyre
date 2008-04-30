# -*- Makefile -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2008  All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PROJECT = pyre
PACKAGE = pyre

PYTHIA_VERSION = 0.8
PYTHIA_ZIP = pythia-${PYTHIA_VERSION}.zip

RECURSE_DIRS = \
    packages \
    tests \
    applications \
    examples \



#--------------------------------------------------------------------------
#

all:
	BLD_ACTION="all" $(MM) recurse

PROJ_CLEAN = 
clean::
	BLD_ACTION="clean" $(MM) recurse

distclean::
	BLD_ACTION="distclean" $(MM) recurse

tidy::
	BLD_ACTION="tidy" $(MM) recurse

zip:
	(cd packages; \
	for dir in pyre journal; do { \
             (cd $${dir}; zip -r ../../${PYTHIA_ZIP} $${dir} -i \*.py); \
	} ; done )

zip2: 
	(cd packages/pyre; zip -r ../../${PYTHIA_ZIP} pyre -i \*.py; \
        cd ../journal; zip -r ../../${PYTHIA_ZIP} journal -i \*.py)



# version
# $Id: Make.mm,v 1.2 2008-04-13 03:55:58 aivazis Exp $

# End of file
