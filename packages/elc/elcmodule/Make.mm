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
#

PROJECT = elc
PACKAGE = elcmodule
MODULE = elc

include std-pythonmodule.def
include local.def

PROJ_CXX_SRCLIB = -ljournal

PROJ_SRCS = \
    bindings.cc \
    exceptions.cc \
    memory.cc \
    misc.cc \
    verify.cc \
    via_mpi.cc


# version
# $Id: Make.mm,v 1.1.1.1 2006-11-27 00:09:34 aivazis Exp $

# End of file
