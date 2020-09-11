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

from future.utils import with_metaclass

from .AbstractDocument import AbstractDocument
from .DTDBuilder import DTDBuilder

class Document(with_metaclass(DTDBuilder, AbstractDocument)):


    tags = []


    # the metaclass has prepared a look up table of nested tags
    def node(self, tag, attributes):
        return self._mydtd[tag](self, attributes)


    def __init__(self, source):
        AbstractDocument.__init__(self, source)
        return


# version
__id__ = "$Id: Document.py,v 1.1.1.1 2006-11-27 00:10:10 aivazis Exp $"

# End of file 
