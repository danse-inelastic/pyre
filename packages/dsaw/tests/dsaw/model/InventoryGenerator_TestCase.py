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


import dataobjects
from dsaw.model.visitors.InventoryGenerator import InventoryGenerator

import unittest

class TestCase(unittest.TestCase):


    def test1(self):
        I = InventoryGenerator()(dataobjects.Dummy)
        self.assertEqual(I.a.name, 'a')
        self.assertEqual(I.a.type, 'str')
        self.assertEqual(I.a.default, 'aa')
        self.assertEqual(I.vec.name, 'vec')
        self.assertEqual(I.vec.type, 'array')
        self.assertEqual(I.vec.shape, (3,))
        self.assertEqual(I.vec.elementtype, 'float')
        i = I()
        i.vec = 1, 0, 0

        import numpy
        m = numpy.array(range(12))
        m.shape = 4,3
        i.mat = m

        i.mat = range(12)
        
        i.mat = [
            [1,2,3,4],
            [1,2,3,4],
            [1,2,3,4],
            ]
        return
        

    def test2(self):
        I = InventoryGenerator()(dataobjects.Job)

        self.assertEqual(I.server.name, 'server')
        self.assertEqual(I.server.type, 'str')
        self.assertEqual(I.server.default, 'octopod.danse.us')

        self.assertEqual(I.computation.name, 'computation')
        self.assertEqual(I.computation.type, 'reference')
        self.assertEqual(I.computation.targettype, dataobjects.Computation)
        return
        

    def test3(self):
        I = InventoryGenerator()(dataobjects.Structure)
        return

    pass # end of TestCase


def pysuite():
    import journal
    journal.debug('dsaw.model').activate()
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
