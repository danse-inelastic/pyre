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
from LiteralFactory import LiteralFactory
from ParagraphFactory import ParagraphFactory
from PreformattedFactory import PreformattedFactory

class Document(ElementContainer, LiteralFactory, ParagraphFactory, PreformattedFactory):


    def form(self, **kwds):
        from Form import Form
        form = Form(**kwds)
        self.contents.append(form)
        return form


    def document(self, **kwds):
        from Document import Document
        document = Document(**kwds)
        self.contents.append(document)
        return document


    def identify(self, inspector):
        return inspector.onDocument(self)


    def __init__(self, title, description="", byline="", **kwds):
        ElementContainer.__init__(self, 'div', **kwds)
        LiteralFactory.__init__(self)
        ParagraphFactory.__init__(self)
        PreformattedFactory.__init__(self)

        self.title = title
        self.description = description
        self.byline = byline
        
        return


# version
__id__ = "$Id: Document.py,v 1.2 2007-11-28 09:37:34 aivazis Exp $"

# End of file 
