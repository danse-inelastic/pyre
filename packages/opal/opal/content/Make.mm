# -*- Makefile -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2005 All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PROJECT = opal
PACKAGE = content

#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
    Banner.py \
    Base.py \
    Body.py \
    ControlBox.py \
    CoreAttributes.py \
    Document.py \
    Element.py \
    ElementContainer.py \
    Form.py \
    FormControl.py \
    FormField.py \
    FormHiddenInput.py \
    Head.py \
    IncludedStyle.py \
    Input.py \
    KeyboardAttributes.py \
    LanguageAttributes.py \
    Link.py \
    Literal.py \
    LiteralFactory.py \
    Logo.py \
    Meta.py \
    Page.py \
    PageContent.py \
    PageCredits.py \
    PageFooter.py \
    PageHeader.py \
    PageLeftColumn.py \
    PageMain.py \
    PageRightColumn.py \
    PageSection.py \
    Paragraph.py \
    ParagraphFactory.py \
    PersonalTools.py \
    Portlet.py \
    PortletContent.py \
    PortletFactory.py \
    PortletLink.py \
    Script.py \
    ScriptFactory.py \
    SearchBox.py \
    Selector.py \
    Style.py \
    TextArea.py \
    Title.py \
    __init__.py \


export:: export-package-python-modules

# version
# $Id: Make.mm,v 1.4 2007-10-03 21:05:01 aivazis Exp $

# End of file
