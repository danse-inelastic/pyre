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


class PreformattedFactory(object):


    def preformatted(self, **kwds):
        from Preformatted import Preformatted
        preformatted = Preformatted(**kwds)

        self.contents.append(preformatted)

        return preformatted


# version
__id__ = "$Id: ParagraphFactory.py,v 1.1.1.1 2006-11-27 00:09:48 aivazis Exp $"

# End of file 
