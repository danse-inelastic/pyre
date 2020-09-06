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


class Table(Script):


    class Inventory(Script.Inventory):

        import pyre.inventory

        name = pyre.inventory.str("name", default="table")
        name.meta['tip'] = "the name of the table"
        
        base = pyre.inventory.str("base", default="Table")
        base.meta['tip'] = "the name of the base class for this table"
        

    def main(self, *args, **kwds):

        self.weaver.begin()
        self.weaver.contents(self._template())
        self.weaver.end()

        name = self.inventory.name
        filename = name + '.py'
        print("creating table '{0!s}' in '{1!s}'".format(name, filename))

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

        text = [
            "",
            "",
            "from {0!s} import {1!s}".format(base, base),
            "",
            "",
            "class {0!s}({1!s}):".format(name, base),
            "",
            "",
            "    import pyre.db",
            "",
            "    # the table name",
            '    name = "{0!s}s"'.format(name.lower()), 
            "",
            "    # the table columns",
            "",
            ]

        return text


# main

if __name__ == "__main__":
    app = Table()
    app.run()


# version
__id__ = "$Id: table.py,v 1.1.1.1 2006-11-27 00:09:51 aivazis Exp $"

# End of file
