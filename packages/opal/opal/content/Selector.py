#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                             Michael A.G. Aivazis
#                      California Institute of Technology
#                      (C) 1998-2004  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from Element import Element


class Selector(Element):


    def identify(self, inspector):
        return inspector.onSelector(self)


    def __init__(self, name, entries, label, selected=None, help='', error='',  **kwds):
        Element.__init__(self, tag='select', name=name, **kwds)

        self.label = label
        self.help = help
        self.error = error
        self.entries = entries
        self.selection = selected

        return
        

# version
__id__ = "$Id: Selector.py,v 1.1.1.1 2006-11-27 00:09:48 aivazis Exp $"

# End of file 
