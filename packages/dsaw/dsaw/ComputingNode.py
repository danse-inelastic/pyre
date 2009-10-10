# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


class ComputingNode:

    address = None
    port = None
    username = None
    workdir = None


    def isLocalhost(self):
        if self.username: return False
        address = self.address
        port = self.port
        return (port in self.localport_aliases) and (address in self.localhost_aliases)
    
    
    def __str__(self):
        return '%s@%s(%s)' % (self.username, self.address, self.port)

    
    def __eq__(self, rhs):
        return self.username == rhs.username \
               and self.port == rhs.port \
               and self.address == rhs.address


    localhost_aliases = [
        None, 'localhost', '127.0.0.1', '',
        ]

    localport_aliases = [
        None, '',
        ]


# version
__id__ = "$Id$"

# End of file 
