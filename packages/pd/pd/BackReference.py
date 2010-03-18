#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                  Jiao Lin
#                      California Institute of Technology
#                        (C) 2008  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


class BackReference(object):


    def __init__(self, reference):
        '''used to represent a back reference

        in srctable, there will be a column named refname and it is
        a foreign key to the id column of targettable.
        This column is a reference:

          srcrow.ref.dereference(db) --> targetrow

        This back reference allows back reference from tagettable to
        srctable:

          targetrow.backref.dereference(db) --> rows in src table that refers to the targetrow
        '''

        self.reference = reference
        return


    def __get__(self, instance, cls = None):
        if instance is None: return self
        
        srctable = self.reference.parent_table()
        refcolname = self.reference.name
        
        return backref(targetrow=instance, srctable=srctable, refcolname=refcolname)

    
    def __set__(self, *args):
        raise RuntimeError, "Cannot set backreference"



class backref(object):

    def __init__(self, targetrow = None, srctable = None, refcolname = None):
        self.targetrow = targetrow
        self.srctable = srctable
        self.refcolname = refcolname


    def dereference(self, db, **kwds):
        return db.dereference(self, **kwds)



# version
__id__ = "$Id$"

# End of file 
