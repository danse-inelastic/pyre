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


class TextArea(Element):


    def identify(self, inspector):
        return inspector.onTextArea(self)


    def __init__(self, id, name, label, help='', error='', default='', **kwds):
        Element.__init__(self, tag='textarea', id=id, name=name, **kwds)

        self.label = label
        self.help = help
        self.error = error
        self.default = default

        return

# version
__id__ = "$Id: TextArea.py,v 1.1 2007-09-03 19:53:25 aivazis Exp $"

# End of file 
