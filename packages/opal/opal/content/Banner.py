#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                             Michael A.G. Aivazis
#                      California Institute of Technology
#                      (C) 1998-2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


class Banner(object):


    def identify(self, inspector):
        return inspector.onBanner(self)


    def __init__(self, href):
        self.href = href
        return


# version
__id__ = "$Id: Banner.py,v 1.1 2007-09-08 03:26:54 aivazis Exp $"

# End of file 
