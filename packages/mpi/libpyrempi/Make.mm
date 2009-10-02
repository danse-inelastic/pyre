# -*- Makefile -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2005  All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

include local.def

PROJECT = mpi
PACKAGE = libpyrempi

PROJ_SAR = $(BLD_LIBDIR)/$(PACKAGE).$(EXT_SAR)
PROJ_DLL = $(BLD_LIBDIR)/$(PACKAGE).$(EXT_SO)
PROJ_TMPDIR = $(BLD_TMPDIR)/$(PROJECT)/$(PACKAGE)
PROJ_CLEAN += $(PROJ_DLL) $(PROJ_SAR)

PROJ_SRCS = \
    Group.cc \
    Communicator.cc \


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

all: $(PROJ_SAR) export

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
export:: export-headers export-libraries export-binaries

EXPORT_HEADERS = \
    Group.h \
    Communicator.h \


EXPORT_LIBS = $(PROJ_SAR)
EXPORT_BINS = $(PROJ_DLL)

# version
# $Id: Make.mm,v 1.2 2008-04-12 05:16:28 aivazis Exp $

# End of file
