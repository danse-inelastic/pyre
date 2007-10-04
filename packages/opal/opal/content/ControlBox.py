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


class ControlBox(ElementContainer):


    def identify(self, inspector):
        return inspector.onControlBox(self)


    def newline(self, **kwds):
        from ControlBoxLine import ControlBoxLine
        control = ControlBoxLine(**kwds)
        self.contents.append(control)
        return control


    def field(self, **kwds):
        from FormField import FormField
        field = FormField(**kwds)
        self.contents.append(field)
        return field


    def text(self, required=False, **kwds):
        from Input import Input
        control = Input(**kwds)

        from FormField import FormField
        field = FormField(control, required)
        self.contents.append(field)

        return control

        
    def __init__(self, required=False, label="", help="", error="", **attributes):
        ElementContainer.__init__(self, tag='table', cls='formfield', **attributes)

        self.required = required
        self.label = label
        self.help = help
        self.error = error

        return


# version
__id__ = "$Id: ControlBox.py,v 1.3 2007-10-04 00:24:17 aivazis Exp $"

# End of file 
