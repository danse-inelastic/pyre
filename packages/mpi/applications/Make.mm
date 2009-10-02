# -*- Makefile -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Michael A.G. Aivazis
#                        (C) 1998-2005 All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PROJECT = pyre
PACKAGE = applications

PROJ_TIDY +=
PROJ_CLEAN =

#--------------------------------------------------------------------------
#

all: export

release: clean
	cvs release .

update: clean
	cvs update .

#--------------------------------------------------------------------------
#

EXPORT_BINS = \
    mpi_world.py \

export:: export-binaries release-binaries


# version
# $Id: Make.mm,v 1.1.1.1 2006-11-27 00:09:43 aivazis Exp $

# End of file
