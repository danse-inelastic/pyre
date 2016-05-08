# -*- Makefile -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2005  All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PROJECT = pyre
PACKAGE = parsing/locators


#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
    ChainLocator.py \
    FileLocator.py \
    ScriptLocator.py \
    SimpleFileLocator.py \
    SimpleLocator.py \
    Traceable.py \
    __init__.py


export:: export-package-python-modules

# version
# $Id: Make.mm,v 1.1.1.1 2006-11-27 00:10:05 aivazis Exp $

# End of file