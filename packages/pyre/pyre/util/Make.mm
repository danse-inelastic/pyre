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
PACKAGE = util


#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
    Resource.py \
    ResourceManager.py \
    Singleton.py \
    Toggle.py \
    bool.py \
    expand.py \
    locate.py \
    range.py \
    subprocesses.py \
    tmpdir.py \
    __init__.py


export:: export-package-python-modules


# version
# $Id: Make.mm,v 1.1.1.1 2006-11-27 00:10:08 aivazis Exp $

# End of file
