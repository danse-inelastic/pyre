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
        import dsaw.dds.components
        dds = pyre.inventory.facility('dds', factory=dsaw.dds.components.dds)
        

    def main(self, *args, **kwds):
        return


    def test1(self):
        'dds component'
        import os
        from dsaw.dds.components.ComputingNode import ComputingNode
        node1 = ComputingNode()
        node1.address = 'localhost'
        node1.workdir = os.path.abspath('node1')
        node1.port = 22
        node1.username = 'linjiao'
            
        self.test(node1)
        return


    def test(self, node1):
        masterroot = self.dds.dataroot
        # clean up
        if os.path.exists(masterroot): shutil.rmtree(masterroot)

        # obj
        class user:
            id = '12345'
            name = 'users'

        dds = self.dds
        
        # method "remember" on masternode
        try:
            dds.remember(user, 'file1')
        except RuntimeError:
            pass
        else: raise Exception, "should have raised RuntimeError"

        # method "remember" on masternode
        os.makedirs(masterroot)
        dir = os.path.join(masterroot, user.name, user.id)
        os.makedirs(dir)
        open(os.path.join(dir, 'file1'), 'w').write('')

        import time
        time.sleep(0.1)
        dds.remember(user, filename='file1')

        # 
        dds.addComputingNode(node1)
        if os.path.exists(node1.workdir): shutil.rmtree(node1.workdir)
        dds.makeAvailable(obj=user, filename='file1', computingNode=node1)
        assert os.path.exists(os.path.join(node1.workdir,user.name,user.id,'file1'))
        assert dds.isAvailable(obj=user, filename='file1', computingNode=node1)

        open(os.path.join(node1.workdir, user.name, user.id, 'file2'), 'w').write('file2')
        dds.remember(obj=user, filename='file2', computingNode=node1)
        dds.makeAvailable(obj=user, filename='file2')
        assert os.path.exists(os.path.join(masterroot,user.name,user.id,'file2'))
        assert dds.isAvailable(obj=user, filename='file2')
        return        
    

    def __init__(self):
        Script.__init__(self, 'test-dds')
        return


    def _default(self):
        Script._default(self)
        dds = self.inventory.dds
        dds.inventory.dataroot = os.path.abspath('masternode')
        return


    def _configure(self):
        Script._configure(self)
        self.dds = self.inventory.dds
        return


import os, shutil


    
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
    


def pysuite():
    suite1 = unittest.makeSuite(TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    import journal
    journal.info('ssher').activate()
    journal.debug('dds').activate()
    
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()

# version
__id__ = "$Id$"

# End of file 
