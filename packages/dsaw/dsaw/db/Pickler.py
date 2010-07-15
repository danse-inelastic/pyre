# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2010  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


class Pickler(object):


    def __init__(self, db, outputdir, chunksize=None):
        self.db = db
        self.outputdir = outputdir
        self.chunksize = chunksize or 10000
        if os.path.exists(outputdir):
            raise RuntimeError, 'output directory %s already exists' % outputdir
        else:
            os.makedirs(outputdir)
        return
    

    def dump(self, table):
        deps = self._findDeps(table)
        all = [table] + deps
        self._saveResolveOrder(all)
        for t in all:
            self._save(t)
        return


    def _save(self, table):
        db = self.db
        records = db.query(table).all()
        if not records: return
        
        tuples = self._toTuples(records, table)
        f = os.path.join(self.outputdir, table.getTableName())
        stream = open(f, 'w')
        import pickle
        pickle.dump(tuples, stream)
        return


    def _toTuples(self, records, table):
        from collections import namedtuple as nt
        r0 = records[0]
        names = r0.getColumnNames()
        tname = table.getTableName()
        def _T(r):
            l = [r.getColumnValue(n) for n in names]
            return tuple(l)
        return tname, tuple(names), map(_T, records)


    def _findDeps(self, table):
        ret = []
        _findDeps(table, ret)
        return ret

    resolve_order_filename = 'resolve-order'
    def _saveResolveOrder(self, tables):
        tables = list(tables)
        f = os.path.join(self.outputdir, self.resolve_order_filename)
        stream = open(f, 'w')
        while tables:
            t = tables.pop()
            name = t.getTableName()
            stream.write(name+'\n')
            continue
        return 


import os

def _findDeps(table, deps):
    from Reference import Reference
    colreg = table._columnRegistry
    for k, v in colreg.iteritems():
        if isinstance(v, Reference):
            t = v.referred_table
            deps.append(t)
            _findDeps(t, deps)
        continue
    return                


# version
__id__ = "$Id$"

# End of file 
