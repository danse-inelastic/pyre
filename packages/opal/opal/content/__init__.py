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


def element(**kwds):
    from Element import Element
    return Element(**kwds)


def head(**kwds):
    from Head import Head
    return Head(**kwds)


def page(**kwds):
    from Page import Page
    return Page(**kwds)


def portlet(**kwds):
    from Portlet import Portlet
    return Portlet(**kwds)


def selector(**kwds):
    from Selector import Selector
    return Selector(**kwds)


# version
__id__ = "$Id: __init__.py,v 1.1.1.1 2006-11-27 00:09:48 aivazis Exp $"

# End of file 
