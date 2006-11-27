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


class FormControl(Element):


    def identify(self, inspector):
        return inspector.onFormControl(self)


    def __init__(self, name, type, value, **kwds):
        Element.__init__(self, 'div', cls='formControls', **kwds)

        self.name = name
        self.type = type
        self.value = value

        return

# version
__id__ = "$Id: FormControl.py,v 1.1.1.1 2006-11-27 00:09:47 aivazis Exp $"

# End of file 
