#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2009 All Rights Reserved 
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from dsaw.model.visitors.DeepCopier import DeepCopier


import unittest

class TestCase(unittest.TestCase):


    def test1(self):
        'simple object with just string'
        # create a simple data object type
        class Dummy:
            a = 3

        dummy = Dummy()
        dummy.a = 5

        dc = DeepCopier()
        dummy1 = dc(dummy)

        self.assertEqual(dummy.a, dummy1.a)
        self.assertNotEqual(dummy, dummy1)
        return
    
    
    def test2(self):
        'object with not-owned reference'

        from dsaw.model.Inventory import Inventory as InventoryBase
        
        # create data object types
        class Computation:

            about = ''
            
            def __init__(self, about):
                self.about = about
                return

        class Job:

            def __init__(self, server, computation):
                self.server = server
                self.computation = computation

            class Inventory(InventoryBase):

                server = InventoryBase.descriptors.str(name='server')
                computation = InventoryBase.descriptors.reference(name='computation', targettype=Computation, owned=False)
                

        # create data objects
        computation = Computation(about='what?')
        job = Job('a.b.c', computation)

        dc = DeepCopier()
        job1 = dc(job)

        self.assert_(job is not job1)
        self.assert_(job.computation is job1.computation)
        return
    
    
    def test3(self):
        'object with owned reference'

        from dsaw.model.Inventory import Inventory as InventoryBase
        
        # create data object types
        class Computation:

            about = ''
            
            def __init__(self, about):
                self.about = about
                return

        class Job:

            def __init__(self, server, computation):
                self.server = server
                self.computation = computation

            class Inventory(InventoryBase):

                server = InventoryBase.descriptors.str(name='server')
                computation = InventoryBase.descriptors.reference(name='computation', targettype=Computation, owned=True)
                

        # create data objects
        computation = Computation(about='what?')
        job = Job('a.b.c', computation)

        dc = DeepCopier()
        job1 = dc(job)

        self.assert_(job is not job1)
        self.assert_(job.computation is not job1.computation)
        self.assert_(job.computation.about == job1.computation.about)
        return
    
    
    pass # end of TestCase


def pysuite():
    suite1 = unittest.makeSuite(TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id$"

# End of file 
