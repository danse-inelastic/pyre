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


    def perform(self, director, routine=None, debug=False):
        """construct an actual page by invoking the requested routine"""

        if routine is None:
            routine = "default"

        try:
            behavior = self.__getattribute__(routine)
        except AttributeError:
            self._info.log("routine '%s' is not yet implemented" % routine)
            behavior = self.nyi

        if debug:
            # avoid the try net so cgitb can dump the exception
            return behavior(director)

        try:
            page = behavior(director)
        except:
            self._info.log("routine '%s' is not implemented correctly" % routine)
            import traceback
            self._debug.log( traceback.format_exc() )
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
__id__ = "$Id: Actor.py,v 1.2 2008-04-21 07:51:55 aivazis Exp $"

# End of file 
