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
BRANCH_REVISION = $$(svn info|grep -o "^Last Changed Rev: [0-9]*" | sed -e "s/Last Changed Rev: //")
PYTHIA_ZIP = pythia-${PYTHIA_VERSION}.zip
PYTHIA_ZIP3 = pythia-${PYTHIA_VERSION}-r${BRANCH_REVISION}.zip

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

zip: prefix
	(cd packages; \
	for dir in pyre journal; do { \
             (cd $${dir}; zip -r ../../${PYTHIA_ZIP} $${dir} -i \*.py); \
	} ; done )

zip2: prefix
	(cd packages/pyre; zip -r ../../${PYTHIA_ZIP} pyre -i \*.py; \
        cd ../journal; zip -r ../../${PYTHIA_ZIP} journal -i \*.py)

zip3: zip
	$(MV_F) ./${PYTHIA_ZIP} ./${PYTHIA_ZIP3}

PREFIX_DIR = ./packages/pyre/pyre/inventory/odb/
prefix:
	$(CP_F) ${PREFIX_DIR}/prefix-template.py ${PREFIX_DIR}/prefix.py


# version
# $Id: Make.mm,v 1.2 2008-04-13 03:55:58 aivazis Exp $

# End of file
