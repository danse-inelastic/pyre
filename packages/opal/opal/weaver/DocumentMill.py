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


from ContentMill import ContentMill


class DocumentMill(ContentMill):


    def onForm(self, form):
        if form.legend:
            legendStart = '<fieldset><legend>%s</legend>' % form.legend
            legendEnd = '</fieldset>'
        else:
            legendStart = ''
            legendEnd = ''
            
        text = [
            self.tagger.onElementBegin(form),
            legendStart,
            ]

        for item in form.contents:
            text += item.identify(self)

        text += [
            legendEnd,
            self.tagger.onElementEnd(form),
            ]

        return text


    def onControlBox(self, box):
        text = ['<div>']

        text += [ '<div>' ]
        if box.required:
            text.append('<span class="formfieldRequired">&nbsp;</span>')
        if box.label:
            text.append('<label for="%s">%s</label>' % (box.attributes["id"], box.label))
        text += [ '</div>' ]

        if box.error:
            text.append('<div class="error">%s</div>' % box.error)

        if box.help:
            text.append('<div class="formfieldHelp">%s</div>' % box.help)

        text += [
            self.tagger.onElementBegin(box), 
            '<tr>'
            ]

        for item in box.contents:
            text += [ '<td class="controlBoxEntry">' ]
            text += item.identify(self)
            text += [ '</td>' ]

        text += [
            '</tr>',
            self.tagger.onElementEnd(box),
            '</div>',
            ]

        return text
    

    def onControlBoxLine(self, line):
        text = ["</tr><tr>"]
        return text


    def onFormControl(self, control):
        text = [
            self.tagger.onElementBegin(control),
            '<input class="context" name="%s" type="%s" value="%s"/>' % (
                control.name, control.type, control.value),
            self.tagger.onElementEnd(control),
            ]
        
        return text


    def onFormField(self, field):
        control = field.control
        if not control:
            return []

        text = [ self.tagger.onElementBegin(field) ]
        
        text += [ '<div>' ]
        if field.required:
            text.append('<span class="formfieldRequired">&nbsp;</span>')
        if control.label:
            text.append('<label for="%s">%s</label>' % (control.attributes["id"], control.label))
        text += [ '</div>' ]

        if control.error:
            text.append('<div class="error">%s</div>' % control.error)

        if control.help:
            text.append('<div class="formfieldHelp">%s</div>' % control.help)

        text += control.identify(self)
        
        text.append(self.tagger.onElementEnd(field))

        return text


    def onFormHiddenInput(self, control):
        text = [
            self.tagger.onElement(control)
            ]

        return text


    def onInput(self, control):
        text = []
        
        text.append(self.tagger.onElement(control))

        return text


    def onSelector(self, selector):

        text = [
            self.tagger.onElementBegin(selector)
            ]

        for value, description in selector.entries:
            if value == selector.selection:
                selected = "selected"
            else:
                selected = ""
            option = '  <option %s value="%s">%s' % (selected, value, description)
            text.append(option)

        text += [
            self.tagger.onElementEnd(selector),
            ]

        return text


    def onTextArea(self, area):

        default = area.default
        if default:
            text = [
                self.tagger.onElementBegin(area),
                area.default,
                self.tagger.onElementEnd(area),
                ]
        else:
            text = [
                self.tagger.onElementBegin(area),
                self.tagger.onElementEnd(area),
                ]

        return text


    def __init__(self, tagger):
        ContentMill.__init__(self)
        self.tagger = tagger
        return

# version
__id__ = "$Id: DocumentMill.py,v 1.7 2007-10-04 00:23:57 aivazis Exp $"

# End of file 
