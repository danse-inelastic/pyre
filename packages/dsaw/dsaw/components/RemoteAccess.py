# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2007-2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


# interface specification
# remoteaccess components must match this interface.
# remoteaccess components are used to access a remote server.


from pyre.components.Component import Component

class RemoteAccess(Component):

    class Inventory(Component.Inventory):

        pass # end of Inventory
    

    def pushdir( self, path, server, remotepath ):
        'push a local directory to remote server'
        raise NotImplementedError 


    def getfile( self, server, remotepath, localdir ):
        '''retrieve a file from remote server to local path
        server: a server db record
        remotepath: path of the file in the remote server
        localdir: local directory
        '''
        raise NotImplementedError


    def getdir( self, server, remotepath, localdir ):
        'retrieve a directory from remote server to local path'
        raise NotImplementedError


    def copyfile(self, server1, path1, server2, path2, recursive=True):
        'copy a file from server1 to server2'
        raise NotImplementedError


    def execute( self, cmd, server, remotepath, suppressException = False ):
        'execute command in the given directory of the given server'
        raise NotImplementedError

    
class RemoteAccessError(Exception): pass


# this is just a reminder what we are asking for the interface of "Server"
class Server:

    # need following attributes:
    address = None
    username = None
    port = None

    pass # end of Server

# version
__id__ = "$Id$"

# End of file 
