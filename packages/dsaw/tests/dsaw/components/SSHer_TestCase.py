#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                Jiao Lin
#                      California Institute of Technology
#                        (C) 2008  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from pyre.applications.Script import Script


class Server:

    def __init__(self, address, port, username):
        self.address = address
        self.port = port
        self.username = username
        return


    def __eq__(self, rhs):
        return self.address == rhs.address and self.port == rhs.port and self.username == rhs.username
    


class App(Script):


    class Inventory(Script.Inventory):

        import pyre.inventory
        import dsaw.components
        ssher = pyre.inventory.facility('ssher', factory=dsaw.components.ssher)
        

    def main(self, *args, **kwds):
        return


    def test1(self):
        'ssher.copyfile'
        testfile = 'testfile'

        # create testfile if not exists
        if not os.path.exists(testfile):
            open(testfile, 'w').write('')

        #
        ssher = self.ssher
        ssher.copyfile(
            Server(None, None, None), testfile,
            Server('upgrayedd.danse.us', None, 'linjiao'), '/tmp',
            )
        ssher.copyfile(
            Server('upgrayedd.danse.us', None, 'linjiao'), '/tmp/testfile',
            Server(None, None, None), testfile,
            )
        ssher.copyfile(
            Server('upgrayedd.danse.us', None, 'linjiao'), '/tmp/testfile',
            Server('upgrayedd.danse.us', None, 'linjiao'), '/tmp/ssher1.py',
            )
        ssher.copyfile(
            Server(None, None, None), testfile,
            Server('login.cacr.caltech.edu', None, 'linjiao'), '/tmp',
            )
        ssher.copyfile(
            Server('login.cacr.caltech.edu', None, 'linjiao'), '/tmp/testfile',
            Server('upgrayedd.danse.us', None, 'linjiao'), '/tmp/ssher1.py',
            )
        return


    def test2(self):
        'ssher.pushdir'
        ssher = self.ssher

        testdir = 'testdir'
        
        #
        if not os.path.exists(testdir):
            os.makedirs(testdir)
        elif not os.path.isdir(testdir):
            raise RuntimeError, "%s is not a directory" % testdir
        
        ssher.pushdir( 'testdir',
                       Server('login.cacr.caltech.edu', None, 'linjiao'),
                       '/tmp')
        return


    def __init__(self):
        Script.__init__(self, 'test-ssher')
        return


    def _configure(self):
        Script._configure(self)
        self.ssher = self.inventory.ssher
        return


import os


    
import unittest

class TestCase(unittest.TestCase):

    def __init__(self, *args, **kwds):
        super(TestCase, self).__init__(*args, **kwds)
        self.app = App()
        self.app.run()
        return

    def test1(self):
        self.app.test1()
        return
    
    def test2(self):
        self.app.test2()
        return
    


def pysuite():
    suite1 = unittest.makeSuite(TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    import journal
    journal.info('ssher').activate()
    
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()

# version
__id__ = "$Id$"

# End of file 
