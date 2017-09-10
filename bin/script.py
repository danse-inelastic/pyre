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

        filename = self.inventory.name + '.py'
        print("creating script '{0!s}'".format(filename))

        stream = open(filename, "w")
        for line in self.weaver.document():
            print(line, file=stream) 
        stream.close()
        
        import os
        os.chmod(filename, 0775)
        
        return


    def __init__(self):
        Script.__init__(self, "app")
        return


    def _init(self):
        Script._init(self)
        self.weaver.language = 'python'
        return


    def _template(self):
        text = [
            "",
            "",
            "def test():",
            "    return",
            "",
            "",
            "# main",
            "if __name__ == '__main__':",
            "    test()",
            "",
            ]

        return text


# main

if __name__ == "__main__":
    import journal
    app = App()
    app.run()


# version
__id__ = "$Id: script.py,v 1.1.1.1 2006-11-27 00:09:51 aivazis Exp $"

# End of file
