# -*- Makefile -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2007 All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PROJECT = fuego
PACKAGE = serialization/c

#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
#
# export

EXPORT_PYTHON_MODULES = \
    CPickler.py \
    __init__.py


export:: export-package-python-modules

# version
# $Id: Make.mm,v 1.1.1.1 2007-09-13 18:17:30 aivazis Exp $

# End of file
