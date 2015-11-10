# -*- Makefile -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2005  All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PROJECT = pyre
PACKAGE = pyre

RECURSE_DIRS = \
    journal \
    pyre \
    blade \
    fuego \
    merlin \
    opal \
    dsaw \
    pd \

ifdef MPI_DIR
RECURSE_DIRS += \
    mpi \
    elc \
    pulse \
    rigid
endif

ifdef ACIS_DIR
RECURSE_DIRS += acis
endif


OTHERS = \

#--------------------------------------------------------------------------
#

all:
	BLD_ACTION="all" $(MM) recurse

clean::
	BLD_ACTION="clean" $(MM) recurse

tidy::
	BLD_ACTION="tidy" $(MM) recurse


# version
# $Id: Make.mm,v 1.2 2007-09-13 17:11:36 aivazis Exp $

# End of file
