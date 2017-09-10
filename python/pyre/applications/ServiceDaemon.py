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

from __future__ import print_function

from Application import Application
from Daemon import Daemon as Stager
from ComponentHarness import ComponentHarness


class ServiceDaemon(Application, Stager, ComponentHarness):


    class Inventory(Application.Inventory):

        import pyre.inventory

        client = pyre.inventory.str('client')
        home = pyre.inventory.str('home', default='/tmp')


    def main(self, *args, **kwds):
        # harness the service
        idd = self.harnessComponent()
        if not idd:
            return

        # generate client configuration
        self.generateClientConfiguration(idd)

        # enter the indefinite loop waiting for requests
        idd.serve()
        
        return


    def generateClientConfiguration(self, component):
        clientName = self.inventory.client
        if not clientName:
            clientName = component.name + '-session'

        registry = self.createRegistry()
        componentRegistry = registry.getNode(clientName)
        component.generateClientConfiguration(componentRegistry)

        stream = open(clientName + '.pml', 'w')
        document = self.weaver.render(registry)
        print("\n".join(document), file=stream) 
        stream.close()
            
        return


    def __init__(self, name):
        Application.__init__(self, name, facility='daemon')
        Stager.__init__(self)
        ComponentHarness.__init__(self)
        return


    def _configure(self):
        Application._configure(self)

        import os
        self.home = os.path.abspath(
            os.path.expanduser(self.inventory.home))

        # should the following be in _init?
        import os
        if not os.path.exists(self.home):
            os.makedirs(self.home)
            
        return

    def _init(self):
        Application._init(self)
        return

# version
__id__ = "$Id: ServiceDaemon.py,v 1.1.1.1 2006-11-27 00:09:54 aivazis Exp $"

# End of file 
