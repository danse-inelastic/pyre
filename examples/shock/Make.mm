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

PROJECT = examples
PACKAGE = shock

#--------------------------------------------------------------------------
#

all: tidy

shock:
	shock.py #--pulse.generator=bath

# version
# $Id: Make.mm,v 1.1.1.1 2006-11-27 00:09:20 aivazis Exp $

# End of file
