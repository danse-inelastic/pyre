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

from pyre.inventory.Facility import Facility


class Actor(Facility):


    def __init__(self, family=None, default=None, meta=None):
        Facility.__init__(self, 'actor', family, default, None, (), meta)
        return


    def _retrieveComponent(self, instance, componentName, args):
        actor = instance.retrieveComponent(
            componentName, factory='actor', args=args, vault=['actors'])

        # if we were successful, return
        if actor:
            actor.aliases.append(self.name)
            return actor, actor.getLocator()

        # otherwise, try again
        return Facility._retrieveComponent(self, instance, componentName, args)


# version
__id__ = "$Id: Actor.py,v 1.1.1.1 2006-11-27 00:09:48 aivazis Exp $"

# End of file 
