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


class Stationery(Script):


    class Inventory(Script.Inventory):

        import pyre.inventory

        name = pyre.inventory.str("name")
        language = pyre.inventory.str("language", default="python")


    def main(self, *args, **kwds):

        for line in self.weaver.render():
            print(line, file=self.stream) 
        
        return


    def __init__(self):
        Script.__init__(self, "stationery")
        self.stream = None
        return


    def _init(self):
        Script._init(self)
        
        # configure the weaver
        self.weaver.language = self.inventory.language

        # prepare the output stream
        filename = self.inventory.name
        if filename:
            print("creating '{0!s}'".format(filename))
            self.stream = open(filename, "w")
        else:
            import sys
            self.stream = sys.stdout
            
        return


# main

if __name__ == "__main__":
    app = Stationery()
    app.run()


# version
__id__ = "$Id: stationery.py,v 1.1.1.1 2006-11-27 00:09:51 aivazis Exp $"

# End of file
