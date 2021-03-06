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


from pyre.components.Component import Component


class UserManager(Component):


    class Inventory(Component.Inventory):

        import pyre.weaver
        import pyre.inventory

        passwd = pyre.inventory.str("passwd", default="users.odb")
        weaver = pyre.inventory.facility('weaver', factory=pyre.weaver.weaver)


    def authenticate(self, username, cleartext):
        if self._reload:
            self.load()

        if not username or not cleartext:
            self._info.log("empty username or password")
            return

        try:
            cryptotext = self._users[username]
        except KeyError:
            self._info.log("bad username '{0!s}'".format(username))
            return

        if not self._decoder(cleartext, cryptotext):
            self._info.log("bad password '{0!s}' for user '{1!s}'".format(cleartext, username))
            return
        
        self._info.log("accepted password for user '{0!s}'".format(username))
        return cryptotext


    def register(self, username, cleartext):
        if username in self._users:
            return False
        
        crypto = self._encoder(cleartext)
        self._users[username] = crypto

        self.save()
        
        return True


    def load(self):
        self._info.log("reading user records from '{0!s}'".format(self.passwd))

        context = {}
        try:
            exec(open(self.passwd).read(), context)
        except IOError as error:
            self._info.log("error opening user db '{0!s}': {1!s}".format(self.passwd, error))
            return

        try:
            users = context["users"]
            method = context["method"]
        except KeyError:
            self._info.log("user db '{0!s}' is malformed: no 'users' or 'method'".format(self.passwd))
            return

        count = len(users)
        if count == 1:
            suffix = ''
        else:
            suffix = 's'
        self._info.log("'{0!s}': found {1:d} user record{2!s}".format(self.passwd, count, suffix))

        self.method = method

        self._users = users
        self._reload = False

        self._encoder = self._encoders[method]
        self._decoder = self._decoders[method]

        return


    def save(self):
        text = [
            "",
            "",
            "method = {0!r}".format(self.method),
            "",
            "",
            "users = {"
            ]

        usernames = list(self._users.keys())
        usernames.sort()

        for name in usernames:
            text += [
                "    '{0!s}': '{1!s}',".format(name, self._users[name]),
                ]

        text += [
            "    }",
            "",
            ]

        self.weaver.begin()
        self.weaver.contents(text)
        self.weaver.end()

        stream = open(self.passwd, "w")
        for line in self.weaver.document():
            stream.write("{0!s}\n".format(line))
        stream.close()
        
        return


    def onReload(self):
        self._reload = True
        return


    def __init__(self, name):
        if name is None:
            name = "user-manager"

        Component.__init__(self, name, facility="userManager")

        # public data
        self.home = ""
        self.passwd = None
        self.method = None
        
        self._users = {}
        self._reload = True
        self._encoder = None
        self._decoder = None

        # encoders
        self._encoders = {
            'md5': self._md5Encoder,
            'sha': self._shaEncoder,
            'crypt': self._cryptEncoder,
            }

        # decoders
        self._decoders = {
            'md5': self._md5Decoder,
            'sha': self._shaDecoder,
            'crypt': self._cryptDecoder,
            }

        return


    def _init(self):
        Component._init(self)

        # locate the user database
        import os
        self.passwd = os.path.join(self.home, self.inventory.passwd)
        self._info.log("user database in '{0!s}'".format(self.passwd))

        # configure the weaver
        self.weaver = self.inventory.weaver
        self.weaver.language = "python"

        return


    def _cryptEncoder(self, cleartext):
        return


    def _cryptDecoder(self, cleartext, cryptotext):
        import crypt
        return crypt.crypt(cleartext, cryptotext[:2]) == cryptotext
            

    import sys
    vinfo = sys.version_info; del sys
    if vinfo[0] == 2:
        if vinfo[1] < 5:
            
            def _md5Encoder(self, cleartext):
                import md5
                return md5.new(cleartext).hexdigest()


            def _md5Decoder(self, cleartext, cryptotext):
                import md5
                return md5.new(cleartext).hexdigest() == cryptotext


            def _shaEncoder(self, cleartext):
                import sha
                return sha.new(cleartext).hexdigest()


            def _shaDecoder(self, cleartext, cryptotext):
                import sha
                return sha.new(cleartext).hexdigest() == cryptotext
            
        else:
            def _md5Encoder(self, cleartext):
                import hashlib
                return hashlib.md5(cleartext).hexdigest()


            def _md5Decoder(self, cleartext, cryptotext):
                import hashlib
                return hashlib.md5(cleartext).hexdigest() == cryptotext


            def _shaEncoder(self, cleartext):
                import hashlib
                return hashlib.sha1(cleartext).hexdigest()


            def _shaDecoder(self, cleartext, cryptotext):
                import hashlib
                return hashlib.sha1(cleartext).hexdigest() == cryptotext
    else:
        raise NotImplementedError
    del vinfo


# version
__id__ = "$Id: UserManager.py,v 1.1.1.1 2006-11-27 00:10:03 aivazis Exp $"

# End of file 
