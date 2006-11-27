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


from PageSection import PageSection
from PortletFactory import PortletFactory


class PageLeftColumn(PageSection, PortletFactory):


    def __init__(self, **kwds):
        PageSection.__init__(self, **kwds)
        PortletFactory.__init__(self)
        return


# version
__id__ = "$Id: PageLeftColumn.py,v 1.1.1.1 2006-11-27 00:09:47 aivazis Exp $"

# End of file 
