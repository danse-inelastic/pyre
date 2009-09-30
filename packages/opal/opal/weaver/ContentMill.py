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


class ContentMill(object):


    def onLiteral(self, literal):
        return [ "\n".join(literal.text) ]


    def onParagraph(self, p):
        text = [ self.tagger.onElementBegin(p) ]
        text += p.text
        text.append(self.tagger.onElementEnd(p))
        return text
    
    def onPreformatted(self, p):
        text = [ self.tagger.onElementBegin(p) ]
        text += p.text
        text.append(self.tagger.onElementEnd(p))
        return text


    def onScript(self, script):
        if "src" in script.attributes:
            return [self.tagger.onElement(script)]
            
        return ["%s\n%s\n%s" % (
            self.tagger.onElementBegin(script),
            "\n".join(script.script),
            self.tagger.onElementEnd(script))]


# version
__id__ = "$Id: ContentMill.py,v 1.1.1.1 2006-11-27 00:09:49 aivazis Exp $"

# End of file 
