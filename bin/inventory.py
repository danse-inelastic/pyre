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


class App(Script):


    class Inventory(Script.Inventory):

        import pyre.inventory

        name = pyre.inventory.str("name", default="simple")


    def main(self, *args, **kwds):

        self.weaver.begin()
        self.weaver.contents(self._template())
        self.weaver.end()

        filename = self.inventory.name + '.pml'
        print("creating inventory template in '{0!s}'".format(filename))

        stream = open(filename, "w")
        for line in self.weaver.document():
            print(line, file=stream) 
        stream.close()
        
        return


    def __init__(self):
        Script.__init__(self, "inventory")
        return


    def _init(self):
        Script._init(self)
        self.weaver.language = 'xml'
        return


    def _template(self):
        name = self.inventory.name
        text = [
            "",
            "",
            "<!DOCTYPE inventory>",
            "",
            "<inventory>",
            "",
            "  <component name={0!r}>".format(self.inventory.name),
            "    <property name='key'>value</property>",
            "  </component>",
            "",
            "</inventory>",
            "",
            ]

        return text


# main

if __name__ == "__main__":
    app = App()
    app.run()


# version
__id__ = "$Id: inventory.py,v 1.1.1.1 2006-11-27 00:09:50 aivazis Exp $"

# End of file
