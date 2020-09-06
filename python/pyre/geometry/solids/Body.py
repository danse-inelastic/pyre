#!/usr/bin/env python
#
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2005 All Rights Reserved
# 
#  <LicenseText>
# 
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

class Body(object):


    def identify(self, inspector):
        raise NotImplementedError(
            "class '{0!s}' should override method '{1!s}'".format(self.__class__.__name__, "identify"))



# version
__id__ = "$Id: Body.py,v 1.1.1.1 2006-11-27 00:09:58 aivazis Exp $"

#
# End of file
