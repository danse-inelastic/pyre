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


class Checkbox(Element):


    def identify(self, inspector):
        return inspector.onButton(self)


    def __init__(self, id, name, label, value='', embeddedText='', help='', error='', type='checkbox', **kwds):
        Element.__init__(self, tag='checkbox', id=id, name=name, type=type, value=value, **kwds)

        self.label = label
        self.help = help
        self.error = error

        return

# version
__id__ = "$Id: Input.py,v 1.1.1.1 2006-11-27 00:09:47 aivazis Exp $"

# End of file 
