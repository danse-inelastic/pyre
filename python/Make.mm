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

RECURSE_DIRS = \
    pyre \

OTHERS = \

#--------------------------------------------------------------------------
# 

all:
	BLD_ACTION="all" $(MM) recurse

tidy::
	BLD_ACTION="tidy" $(MM) recurse

clean::
	BLD_ACTION="clean" $(MM) recurse

distclean::
	BLD_ACTION="distclean" $(MM) recurse


# version
# $Id: Make.mm,v 1.1.1.1 2006-11-27 00:09:50 aivazis Exp $

# End of file
