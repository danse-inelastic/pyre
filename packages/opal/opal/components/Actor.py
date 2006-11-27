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


from pyre.components.Component import Component


class Actor(Component):


    def perform(self, director, routine=None):
        """construct an actual page by invoking the requested routine"""

        if routine is None:
            routine = "default"

        try:
            behavior = self.__getattribute__(routine)
        except AttributeError:
            self._info.log("routine '%s' is not yet implemented" % routine)
            behavior = self.nyi

        try:
            page = behavior(director)
        except TypeError:
            self._info.log("routine '%s' is not implemented correctly" % routine)
            page = self.error(director)

        return page


    def error(self, director):
        """notify the user that a routine is not implemented correctly"""
        page = director.retrievePage("error")
        return page


    def nyi(self, director):
        """notify the user that the requested routine is not yet implemented"""
        page = director.retrievePage("nyi")
        return page


    def __init__(self, name):
        super(Actor, self).__init__(name, facility='actor')
        self.routine = None
        return


# version
__id__ = "$Id: Actor.py,v 1.1.1.1 2006-11-27 00:09:46 aivazis Exp $"

# End of file 
