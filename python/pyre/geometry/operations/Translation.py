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

from Transformation import Transformation


class Translation(Transformation):


    def identify(self, visitor):
        return visitor.onTranslation(self)


    def __init__(self, body, vector):
        Transformation.__init__(self, body)
        self.vector = tuple(vector)

        self._info.log(str(self))

        return


    def __str__(self):
        return "translation: body={{0!s}}, vector={1!r}".format(self.body, self.vector)



# version
__id__ = "$Id: Translation.py,v 1.1.1.1 2006-11-27 00:09:57 aivazis Exp $"

#
# End of file
