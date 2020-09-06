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


class Module(Script):


    class Inventory(Script.Inventory):

        import pyre.inventory

        name = pyre.inventory.str("name", default="__init__")


    def main(self, *args, **kwds):

        for line in self.weaver.render():
            print(line, file=self.stream) 
        
        return


    def __init__(self):
        Script.__init__(self, "module")
        self.stream = None
        return


    def _init(self):
        Script._init(self)
        
        # initialize the weaver
        self.weaver.language = 'python'

        # prepare the output stream
        filename = self.inventory.name
        if filename:
            filename += '.py'
            print("creating '{0!s}'".format(filename))
            self.stream = file(filename, "w")
        else:
            import sys
            self.stream = sys.stdout

        return


# main

if __name__ == "__main__":
    app = Module()
    app.run()


# version
__id__ = "$Id: module.py,v 1.1.1.1 2006-11-27 00:09:51 aivazis Exp $"

# End of file
