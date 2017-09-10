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


class Component(Script):


    class Inventory(Script.Inventory):

        import pyre.inventory

        name = pyre.inventory.str("name", default="component")
        name.meta['tip'] = "the name of the component"
        
        facility = pyre.inventory.str("facility", default="facility")
        facility.meta['tip'] = "the facility this component implements"
        
        base = pyre.inventory.str("base", default="Component")
        facility.meta["tip"] = "the name of the base class for this component"


    def main(self, *args, **kwds):

        self.weaver.begin()
        self.weaver.contents(self._template())
        self.weaver.end()

        name = self.inventory.name
        filename = name + '.py'
        print("creating component '{0!s}' in {1!s}'".format(name, filename))

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
        base = self.inventory.base
        name = self.inventory.name
        facility = self.inventory.facility

        if self.inventory.base == "Component":
            importStmt = "from pyre.components.Component import Component"
        else:
            importStmt = "from {0!s} import {1!s}".format(self.inventory.base, self.inventory.base)
        
        text = [
            "",
            "",
            importStmt,
            "",
            "",
            "class {0!s}({1!s}):".format(name, base),
            "",
            "",
            "    class Inventory({0!s}.Inventory):".format(base),
            "",
            "        import pyre.inventory",
            "",
            "",
            "    def __init__(self, name):",
            "        if name is None:",
            "            name = '{0!s}'".format(facility),
            "",
            "        {0!s}.__init__(self, name, facility={1!r})".format(base, facility),
            "",
            "        return",
            "",
            "",
            "    def _defaults(self):",
            "        {0!s}._defaults(self)".format(base),
            "        return",
            "",
            "",
            "    def _configure(self):",
            "        {0!s}._configure(self)".format(base),
            "        return",
            "",
            "",
            "    def _init(self):",
            "        {0!s}._init(self)".format(base),
            "        return",
            "",
            ]

        return text


# main

if __name__ == "__main__":
    app = Component()
    app.run()


# version
__id__ = "$Id: component.py,v 1.1.1.1 2006-11-27 00:09:50 aivazis Exp $"

# End of file
