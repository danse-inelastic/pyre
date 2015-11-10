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

PROJECT = pyre
PACKAGE = applications

PROJ_TIDY += *.log
PROJ_CLEAN =

#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
#

EXPORT_BINS = \
    app.py \
    component.py \
    idd.py \
    inventory.py \
    ipad.py \
    journald.py \
    module.py \
    script.py \
    service.py \
    stationery.py \
    table.py \


export:: export-binaries release-binaries


# version
# $Id: Make.mm,v 1.1.1.1 2006-11-27 00:09:50 aivazis Exp $

# End of file
