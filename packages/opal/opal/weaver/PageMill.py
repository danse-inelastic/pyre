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


from pyre.weaver.mills.HTMLMill import HTMLMill


class PageMill(HTMLMill):


    def onBody(self, body):
        return self.bodyMill.render(body)


    def onHead(self, head):
        return self.headMill.render(head)


    def onPage(self, page):
        content = [ self.tagger.onElementBegin(page) ]
        for tag in page.contents:
            content += tag.identify(self)
        content.append(self.tagger.onElementEnd(page))
        return content


    def __init__(self):
        HTMLMill.__init__(self)
        self.stylesheets = []

        from TagMill import TagMill
        self.tagger = TagMill()

        from HeadMill import HeadMill
        self.headMill = HeadMill(self.tagger)

        from BodyMill import BodyMill
        self.bodyMill = BodyMill(self.tagger)

        return
        

    def _renderDocument(self, document):
        self._rep += document.identify(self)
        return


# version
__id__ = "$Id: PageMill.py,v 1.1.1.1 2006-11-27 00:09:49 aivazis Exp $"

# End of file 
