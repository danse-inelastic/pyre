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


class Evaluator(Component):


    def evaluate(self, component, command, args):
        try:
            func = component.__getattribute__(command)
        except AttributeError:
            import journal
            journal.error('pyre.services').log(
                "{0!r} not found in component {1!r}".format(command, component.name))
            return

        if not callable(func):
            import journal
            journal.error('pyre.services').log(
                "component {0!r}: {1!r} is not callable".format(component.name, command))
            return

        try:
            return func(*args)
        except TypeError as msg:
            import journal
            journal.error('pyre.services').log(
                "component {0!r}: {1!s}".format(component.name, msg))

        return


    def __init__(self, name):
        if name is None:
            name = 'evaluator'

        Component.__init__(self, name, facility='serviceRequestEvaluator')

        return


# version
__id__ = "$Id: Evaluator.py,v 1.1.1.1 2006-11-27 00:10:06 aivazis Exp $"

# End of file 
