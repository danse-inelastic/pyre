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


from pyre.applications.Script import Script


class ClientServer(Script):


    class Inventory(Script.Inventory):

        import pyre.inventory

        # support for client and server modes
        client = pyre.inventory.bool("client", default=False)
        server = pyre.inventory.bool("server", default=False)

        # delay before client is spawned
        delay = pyre.inventory.float("delay", default=2.0)


    def main(self, *args, **kwds):

        if self._doClient and self._doServer:
            self._info.log("in split mode")
            self._both()
        elif self._doClient:
            self._info.log("in client mode")
            self.onClient()
            self._info.log("client finished")
        elif self._doServer:
            self._info.log("in server mode")
            self.onServer()
            self._info.log("server finished")
        else:
            import journal
            journal.warning(self.name).log("nothing to do; exiting")

        return


    def __init__(self, name):
        Script.__init__(self, name)
        self._delay = 0
        self._doClient = False
        self._doServer = False
        return


    def _configure(self):
        Script._configure(self)
        self._delay = self.inventory.delay
        self._doClient = self.inventory.client
        self._doServer = self.inventory.server
        return


    def _both(self):
        import os

        # the process id of the main script
        pid = os.getpid()

        child = os.fork()
        if child > 0:
            # in the parent process
            self._info.log("server({0!r}): spawned client({1!r})".format(pid, child))
            self._info.log("server({0!r}): proceeding in server mode".format(pid))
            self.onServer()
            self._info.log("server({0!r}): finished".format(pid))
        elif child == 0:
            pid = os.getpid()

            self._info.log("client({0!r}): sleeping for {1!r} seconds".format(pid, self._delay))
            import select
            select.select([], [], [], self._delay)

            self._info.log("client({0!r}): proceeding in client mode".format(pid))
            self.onClient()
            self._info.log("client({0!r}): finished".format(pid))
        else:
            import journal
            journal.error(self.name).log("fork: error {0!s}".format(child))
            
        return



# version
__id__ = "$Id: ClientServer.py,v 1.1.1.1 2006-11-27 00:09:54 aivazis Exp $"

# End of file 
