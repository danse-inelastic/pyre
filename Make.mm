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

RECURSE_DIRS = \
    packages \
    tests \
    applications \
    examples \


#To use the pure python versions of selected pythia packages,
#you must add the produced .zip file to your PYTHONPATH.
PYTHIA_VERSION = 0.8
PYTHIA_ZIP = pythia-${PYTHIA_VERSION}.zip
ZIP_PACKAGES = pyre journal opal


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
	for dir in ${ZIP_PACKAGES}; do { \
             (cd $${dir}; zip -r ../../${PYTHIA_ZIP} $${dir} -i \*.py); \
	} ; done )

zip0: 
	(cd packages/pyre; zip -r ../../${PYTHIA_ZIP} pyre -i \*.py; \
        cd ../journal; zip -r ../../${PYTHIA_ZIP} journal -i \*.py)


# version
# $Id: Make.mm,v 1.1.1.1 2006-11-27 00:09:14 aivazis Exp $

# End of file
