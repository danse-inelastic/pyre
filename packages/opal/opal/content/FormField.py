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


class FormField(Element):


    def identify(self, inspector):
        return inspector.onFormField(self)


    def __init__(self, control=None, required=False):
        Element.__init__(self, tag='div', cls="formfield")
        self.control = control
        self.required = required
        return

# version
__id__ = "$Id: FormField.py,v 1.2 2007-09-05 20:09:47 aivazis Exp $"

# End of file 
