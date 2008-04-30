#!/usr/bin/env python
# 
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2005  All Rights Reserved
# 
#  <LicenseText>
# 
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 

if __name__ == "__main__":

    import nttcp
    from nttcp import nttcp as nttcpmodule

    print "copyright information:"
    print "   ", nttcp.copyright()
    print "   ", nttcpmodule.copyright()

    print
    print "module information:"
    print "    file:", nttcpmodule.__file__
    print "    doc:", nttcpmodule.__doc__
    print "    contents:", dir(nttcpmodule)


# version
__id__ = "$Id: signon.py,v 1.1.1.1 2006-11-27 00:09:45 aivazis Exp $"

#  End of file 
