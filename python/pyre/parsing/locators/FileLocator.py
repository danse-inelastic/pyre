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


class FileLocator(object):


    def __init__(self, source, line, column):
        self.source = source
        self.line = line
        self.column = column
        return


    def __str__(self):
        s = "file={0!r}, line={1!r}, column={2!r}".format(self.source, self.line, self.column)
        return '{' + s + '}'

    __slots__ = ("source", "line", "column")

# End of file 
