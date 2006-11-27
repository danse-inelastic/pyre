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


class ScriptFactory(object):


    def script(self, **kwds):
        from Script import Script
        script = Script(**kwds)

        self.contents.append(script)

        return script


# version
__id__ = "$Id: ScriptFactory.py,v 1.1.1.1 2006-11-27 00:09:48 aivazis Exp $"

# End of file 
