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


def v3(v):
    if len(v)!=3: raise ValueError, "vector must have 3 elements"
    return v


import unittest

class TestCase(unittest.TestCase):


    def test(self):
        #import pdb; pdb.set_trace()
        from dsaw.model.Inventory import Inventory as base
        class Inventory(base):

            # no validator
            vec = base.d.array(name='vec', shape=3, default=[0,0,1], elementtype='float')
            # has element validator
            vec2 = base.d.array(
                name='vec2', shape=3, default=[0,0,1],
                elementtype='float', elementvalidator=base.v.nonnegative,
                )
            # has validator 
            vec3 = base.d.array(
                name='vec3', shape=None, default=[0,0,1],
                elementtype='float', validator=v3,
                )
            # has both validator and elementvalidator
            vec4 = base.d.array(
                name='vec4', shape=None, default=[0,0,1],
                elementtype='float', validator=v3, elementvalidator=base.v.nonnegative,
                )

        i = Inventory()
        i.vec = 1,0,0
        self.assertEqual(i.vec[0], 1.)
        i.vec = -1,0,0
        self.assertExecRaises(ValueError, "i.vec = 1,0", locals())

        i.vec2 = 1,0,0
        self.assertExecRaises(ValueError, "i.vec2 = -1,0,0", locals())
        self.assertExecRaises(ValueError, "i.vec2 = 1,0", locals())

        i.vec3 = 1,0,0
        i.vec3 = -1,0,0
        self.assertExecRaises(ValueError, "i.vec3 = 0,0", locals())

        i.vec4 = 1,0,0
        self.assertExecRaises(ValueError, "i.vec4 = -1, 0,0", locals())
        self.assertExecRaises(ValueError, "i.vec4 = 0,0", locals())
        
        return


    def assertExecRaises(self, exception, expr, env):
        try:
            exec expr in env
        except exception:
            return
        else:
            raise AssertionError, "expect exception %s" %exception.__name__
        

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
