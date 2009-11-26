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


import unittest

class TestCase(unittest.TestCase):


    def dbManager(self):
        from dsaw.db import connect
        db = connect(db ='postgres:///test')
        db.autocommit(True)
        return db


    def test1(self):
        'dsaw.db.ReferenceSet: '
        db = self.dbManager()

        defaults = {
            'boolean': True,
            'integer': 10,
            'real': 100.,
            'char': 'abc',
            #'doubleArray': [1,2,3],
            }
        initkwds = {
            'char': {'length': 10},
            }

        from dsaw.db.Table import Table
        class Test(Table):

            name = "test"

            import dsaw.db

            for type, default in defaults.iteritems():
                kwds = initkwds.get(type) or {}
                name = '%svar' % type
                code = '%s = dsaw.db.%s(name="%s", default=%r, **kwds)' % (
                    name, type, name, default)
                exec code
                continue

        t = Test()

        for type, default in defaults.iteritems():
            varname = '%svar' % type
            self.assertEqual(getattr(t, varname), default)
            continue

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
