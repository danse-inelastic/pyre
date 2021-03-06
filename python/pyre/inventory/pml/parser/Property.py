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

import sys
from .AbstractNode import AbstractNode

if sys.version_info < (3,0):
    import urllib
    url_unquote = urllib.unquote
else:
    import urllib.parse
    url_unquote = urllib.parse.unquote

class Property(AbstractNode):


    tag = "property"


    def notify(self, parent):
        return parent.onProperty(self)


    def content(self, content):
        self.value += url_unquote(content)
        self.locator = self.document.locator
        return


    def __init__(self, document, attributes):
        AbstractNode.__init__(self, document)
        self.name = attributes["name"]
        self.value = ''
        self.locator = None
        return
    

# version
__id__ = "$Id: Property.py,v 1.1.1.1 2006-11-27 00:10:02 aivazis Exp $"

# End of file 
