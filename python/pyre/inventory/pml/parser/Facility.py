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

import urllib.parse
from .AbstractNode import AbstractNode


class Facility(AbstractNode):


    tag = "facility"


    def notify(self, parent):
        return parent.onFacility(self)


    def content(self, content):
        self.value += urllib.parse.unquote(content)
        self.locator = self.document.locator
        return


    def __init__(self, document, attributes):
        AbstractNode.__init__(self, document)
        self.name = attributes["name"]
        self.value = ''
        self.locator = None
        return
    

# version
__id__ = "$Id: Facility.py,v 1.1.1.1 2006-11-27 00:10:02 aivazis Exp $"

# End of file 
