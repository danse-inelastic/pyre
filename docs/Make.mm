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
PACKAGE = sphinx


RECURSE_DIRS = \


#--------------------------------------------------------------------------
#

all: docs
	BLD_ACTION="all" $(MM) recurse

PROJ_CLEAN = \
	_build/* \

clean::
	BLD_ACTION="clean" $(MM) recurse

distclean::
	BLD_ACTION="distclean" $(MM) recurse

tidy::
	BLD_ACTION="tidy" $(MM) recurse

docs: sphinx-build


include std-docs.def

RSYNC_A = rsync -a
sphinx-build: Makefile $(EXPORT_DOCDIR)
	make html
	$(RSYNC_A) _build/html/ $(EXPORT_DOCDIR)/

# version
# $Id: Make.mm,v 1.2 2008-04-13 03:55:58 aivazis Exp $

# End of file
