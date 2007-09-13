#!/usr/bin/env python
# 
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2007 All Rights Reserved
# 
#  <LicenseText>
# 
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 


class Locator(object):


    def __init__(self, file, line, column):

        self.filename = file
        self.line = line
        self.column = column

        return


    __slots__ = ("column", "filename", "line")


# version
__id__ = "$Id: Locator.py,v 1.1 2007-09-13 15:53:29 aivazis Exp $"

#  End of file 
