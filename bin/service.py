#!/usr/bin/env python
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
#

from __future__ import print_function

from pyre.applications.Script import Script


class Service(Script):


    class Inventory(Script.Inventory):

        import pyre.inventory

        name = pyre.inventory.str("name", default="service")


    def main(self, *args, **kwds):

        self.weaver.begin()
        self.weaver.contents(self._template())
        self.weaver.end()

        name = self.inventory.name
        filename = name + '.py'
        print("creating service '{0!s}' in '{1!s}'".format(name, filename))

        stream = open(filename, "w")
        for line in self.weaver.document():
            print(line, file=stream) 
        stream.close()
        
        return


    def __init__(self):
        Script.__init__(self, "app")
        return


    def _init(self):
        Script._init(self)
        self.weaver.language = 'python'
        return


    def _template(self):
        name = self.inventory.name
        
        text = [
            "",
            "",
            "from pyre.components.Service import Service",
            "",
            "",
            "class {0!s}(Service):".format(name),
            "",
            "",
            "    class Inventory(Service.Inventory):",
            "",
            "        import pyre.inventory",
            "",
            "",
            "    def serve(self):",
            "        return",
            "",
            "",
            "    def __init__(self, name=None):",
            "        if name is None:",
            "            name = 'service'",
            "",
            "        Service.__init__(self, name)",
            "",
            "        return",
            "",
            "",
            "    def _defaults(self):",
            "        Service._defaults(self)",
            "        return",
            "",
            "",
            "    def _configure(self):",
            "        Service._configure(self)",
            "        return",
            "",
            "",
            "    def _init(self):",
            "        Service._init(self)",
            "        return",
            "",
            ]

        return text


# main

if __name__ == "__main__":
    app = Service()
    app.run()


# version
__id__ = "$Id: service.py,v 1.1.1.1 2006-11-27 00:09:51 aivazis Exp $"

# End of file
