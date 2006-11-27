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


from ElementContainer import ElementContainer
from pyre.parsing.locators.Traceable import Traceable


class Page(ElementContainer, Traceable):


    def identify(self, inspector):
        return inspector.onPage(self)


    def body(self, **kwds):
        from Body import Body
        self._body = Body(**kwds)
        self.contents.append(self._body)
        return self._body


    def head(self, **kwds):
        from Head import Head
        self._head = Head(**kwds)
        self.contents.append(self._head)
        return self._head


    def __init__(self):
        ElementContainer.__init__(self, 'html')
        Traceable.__init__(self)

        # page parts
        self._head = None
        self._body = None
        
        return

# version
__id__ = "$Id: Page.py,v 1.1.1.1 2006-11-27 00:09:47 aivazis Exp $"

# End of file
