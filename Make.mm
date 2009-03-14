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

PYRE_EXTENSIONS = \*.odb \*.pml \*.md5 \*.sha \*.crypt
zip2: prefix
	(cd packages/pyre; \
        zip -r ../../${PYTHIA_ZIP} pyre -i \*.py ${PYRE_EXTENSIONS}; \
        cd ../journal; \
        zip -r ../../${PYTHIA_ZIP} journal -i \*.py ${PYRE_EXTENSIONS})

zip3: zip2
	$(MV_F) ./${PYTHIA_ZIP} ./${PYTHIA_ZIP3}

zip4: addtests zip3 deltests


### slave calls ###
PREFIX_DIR = ./packages/pyre/pyre/inventory/odb/
prefix:
	$(CP_F) ${PREFIX_DIR}/prefix-template.py ${PREFIX_DIR}/prefix.py

CPFLAGS = -rf
addtests:
	$(CP) ${CPFLAGS} packages/pyre/tests packages/pyre/pyre/tests
	$(CP) ${CPFLAGS} packages/journal/tests packages/journal/journal/tests

deltests:
	$(RM) $(RMFLAGS) packages/pyre/pyre/tests
	$(RM) $(RMFLAGS) packages/journal/journal/tests


# version
# $Id: Make.mm,v 1.2 2008-04-13 03:55:58 aivazis Exp $

# End of file
