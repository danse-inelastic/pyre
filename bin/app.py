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
        name.meta['tip'] = 'the name of the application to generate'

        path = pyre.inventory.list("path")
        path.meta['tip'] = 'a list of directories to include in the python path'
        

    def main(self, *args, **kwds):

        self.weaver.begin()
        self.weaver.contents(self._template())
        self.weaver.end()

        appname = self.inventory.name.capitalize()
        filename = self.inventory.name + '.py'
        print("creating application '{0!s}' in '{1!s}'".format(appname, filename))

        stream = open(filename, "w")
        for line in self.weaver.document():
            print(line, file=stream)
        stream.close()
        
        import os
        os.chmod(filename, 0o775)
        
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
        appName = name.capitalize()
        
        text = [
            "",
            "",
            "def main():",
            "",
            "",
            "    from pyre.applications.Script import Script",
            "",
            "",
            "    class {0!s}App(Script):".format(appName),
            "",
            "",
            "        class Inventory(Script.Inventory):",
            "",
            "            import pyre.inventory",
            "",
            "            name = pyre.inventory.str('name', default='world')",
            "            name.meta['tip'] = 'the entity to greet'",
            "",
            "",
            "        def main(self, *args, **kwds):",
            "            print('Hello {0!s}!'.format(self.friend))",
            "            return",
            "",
            "",
            "        def __init__(self):",
            "            Script.__init__(self, {0!r})".format(name),
            "            self.friend = ''",
            "            return",
            "",
            "",
            "        def _defaults(self):",
            "            Script._defaults(self)",
            "            return",
            "",
            "",
            "        def _configure(self):",
            "            Script._configure(self)",
            "            self.friend = self.inventory.name",
            "            return",
            "",
            "",
            "        def _init(self):",
            "            Script._init(self)",
            "            return",
            "",
            "",
            "    app = {0!s}App()".format(appName),
            "    return app.run()",
            "",
            "",
            "# main",
            "if __name__ == '__main__':",
            ]

        path = self.inventory.path
        if path:
            text += [
                "    # adjust the python path",
                "    import sys",
                "    sys.path = {0!r} + sys.path".format(path),
                ""
                ]

        text += [
            "    # invoke the application shell",
            "    main()",
            "",
            ]

        return text


# main

if __name__ == "__main__":
    app = App()
    app.run()


# version
__id__ = "$Id: app.py,v 1.1.1.1 2006-11-27 00:09:50 aivazis Exp $"

# End of file
