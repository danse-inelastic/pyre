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
from ParagraphFactory import ParagraphFactory
from LiteralFactory import LiteralFactory


class Form(ElementContainer, ParagraphFactory, LiteralFactory):


    def identify(self, inspector):
        return inspector.onForm(self)


    def box(self, **kwds):
        from ControlBox import ControlBox
        box = ControlBox(**kwds)
        self.contents.append(box)
        return box


    def control(self, **kwds):
        from FormControl import FormControl
        control = FormControl(**kwds)
        self.contents.append(control)
        return control


    def field(self, **kwds):
        from FormField import FormField
        field = FormField(**kwds)
        self.contents.append(field)
        return field


    def hidden(self, **kwds):
        from FormHiddenInput import FormHiddenInput
        field = FormHiddenInput(**kwds)
        self.contents.append(field)
        return field


    def password(self, **kwds):
        from Input import Input
        control = Input(type="password", **kwds)
        
        from FormField import FormField
        field = FormField(control)
        self.contents.append(field)

        return control


    def submitButton(self, value="submit", **kwds):
        return self.control(name="submit", type="submit", value=value, **kwds)


    def text(self, required=False, **kwds):
        from Input import Input
        control = Input(**kwds)
        
        from FormField import FormField
        field = FormField(control, required)
        self.contents.append(field)

        return control


    def textarea(self, required=False, **kwds):
        from TextArea import TextArea
        control = TextArea(**kwds)
        
        from FormField import FormField
        field = FormField(control, required)
        self.contents.append(field)

        return control


    # event handlers
    def onSubmit(self, action):
        self.attributes['onSubmit'] = action
        return


    def __init__(self, name, action, legend=None, **kwds):
        ElementContainer.__init__(self, 'form', name=name, action=action, method="post", **kwds)
        ParagraphFactory.__init__(self)
        LiteralFactory.__init__(self)
        
        self.legend = legend
        return

# version
__id__ = "$Id: Form.py,v 1.7 2007-10-03 21:02:41 aivazis Exp $"

# End of file 
