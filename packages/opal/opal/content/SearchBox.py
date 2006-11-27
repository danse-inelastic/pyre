#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                             Michael A.G. Aivazis
#                      California Institute of Technology
#                      (C) 1998-2005  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


class SearchBox(object):


    def identify(self, inspector):
        return inspector.onSearchBox(self)


    def __init__(self):
        return


# version
__id__ = "$Id: SearchBox.py,v 1.1.1.1 2006-11-27 00:09:48 aivazis Exp $"

# End of file 
