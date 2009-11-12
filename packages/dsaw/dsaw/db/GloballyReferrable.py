# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from VersatileReference import global_pointer


from Table import Table

class GloballyReferrable(Table):

    from Reference import Reference
    globalpointer = Reference(name='globalpointer', table=global_pointer)


    def getReferences(self, db, table, refname, **kwds):
        opts = {refname: self.globalpointer.id}
        opts.update(kwds)
        return db.query(table).filter_by(**opts).all()


    def establishGlobalPointer(self, db):
        # create a new global_pointer
        gptr = global_pointer()
        # the type of the pointer
        try:
            gptr.type = self.name
        except:
            gptr.type = self.__class__.__name__.lower()
        # insert it to db to have a new id
        gptr = db.insertRow(gptr)
        db.commit()
        # now we have a new id
        gid = gptr.id
        # and we need to update the target
        # so that it has the new global id
        db.updateRow(
            self.__class__,
            [('globalpointer', gid)],
            where="id='%s'" % self.id)
        # update the target instance as well
        self.globalpointer = gid
        # commit now
        db.commit()
        return
        
    

# version
__id__ = "$Id$"

# End of file 
