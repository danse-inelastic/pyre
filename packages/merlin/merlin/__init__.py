#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                             Michael A.G. Aivazis
#                      California Institute of Technology
#                      (C) 1998-2005  All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


def merlin():
    from components.Merlin import Merlin
    return Merlin()


# misc
def copyright():
    return "merlin: Copyright (c) 1998-2005 Michael A.G. Aivazis"

# version
__version__ = "0.8"
__id__ = "$Id: __init__.py,v 1.1.1.1 2006-11-27 00:09:42 aivazis Exp $"

# End of file 
