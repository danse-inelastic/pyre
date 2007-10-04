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


from Element import Element


class ControlBoxLine(Element):


    def identify(self, inspector):
        return inspector.onControlBoxLine(self)


    def __init__(self, **attributes):
        Element.__init__(self, tag='', **attributes)
        return


# version
__id__ = "$Id: ControlBoxLine.py,v 1.1 2007-10-04 00:09:55 aivazis Exp $"

# End of file 
