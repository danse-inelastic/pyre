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


from pyre.applications.Script import Script


class Languages(Script):


    def main(self, *args, **kwds):

        weaver = self.weaver

        languages = weaver.languages()
	print "languages:", ", ".join(languages)
        return


    def __init__(self):
        Script.__init__(self, "languages")
        return


# main

if __name__ == "__main__":
    app = Languages()
    app.run()


# version
__id__ = "$Id: languages.py,v 1.1.1.1 2006-11-27 00:10:13 aivazis Exp $"

# End of file
