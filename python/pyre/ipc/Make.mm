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
PACKAGE = ipc


#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
    PortMonitor.py \
    Selector.py \
    Socket.py \
    TCPMonitor.py \
    TCPSocket.py \
    UDPMonitor.py \
    UDPSocket.py \
    __init__.py

export:: export-package-python-modules

# version
# $Id: Make.mm,v 1.1.1.1 2006-11-27 00:10:04 aivazis Exp $

# End of file
