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


"""
Limitation: only works with tables with one key column
"""


strategies = {
    'o': 'overwrite',
    's': 'skip',
    }


class Unpickler(object):


    def __init__(self, db, inputdir):
        self.db = db
        self.inputdir = inputdir
        if not os.path.exists(inputdir):
            raise RuntimeError, 'input directory %s does not exist' % inputdir
        return
    

    def load(self, tables, strategy=None, idcol='id'):
        """load the given tables to the db

        idcol: the name of column that identify the record.
        strategy:
          - overwrite: overwrite the existing records
          - prompt: prompt user for action when there is existing record with the same id
          - skip: skip the record that has an existing record wiith the same idin the db
        """
        inputdir = self.inputdir
        db = self.db

        order = self._readResolveOrder()
        self._checkTables(tables, order)

        name2table = self._createName2TableMap(tables)
        
        for name in order:
            table = name2table[name]
            self._load(table, strategy=strategy, idcol=idcol)
            continue
        
        return


    def _load(self, table, strategy=None, idcol='id'):
        db = self.db
        inputdir = self.inputdir

        #
        db.registerTable(table)
        try:
            db.createTable(table)
        except:
            pass

        #
        pkl = os.path.join(inputdir, table.getTableName())
        if not os.path.exists(pkl):
            return
        tablename, fields, records = pickle.load(open(pkl))
        for r in records:
            row = table()
            for field, value in zip(fields, r):
                col = table._columnRegistry[field]
                row._setColumnValue(field, value)
                continue
            # try to see if there is an existing record
            filterkwds = {idcol:getattr(row, idcol)}
            rowsindb = db.query(table).filter_by(**filterkwds).all()
            # if yes, we need to apply a strategy
            if rowsindb:
                if strategy == 'prompt':
                    while 1:
                        p = raw_input('Record %s, overwrite(o)/skip(s)? ' % row)
                        if p in ['o', 's']:
                            break
                        continue
                    strategy = strategies[p]
                    
                if strategy == 'overwrite':
                    db.updateRecord(row)
                    continue

                if strategy == 'skip':
                    continue

                raise RuntimeError, "Record %s already exists in db %s: %s, but you did not specify a strategy to deal with this" % (row, rowsindb, db)

            db.insertRow(row)
            continue
        return


    def _readResolveOrder(self):
        inputdir = self.inputdir
        from Pickler import Pickler
        order = open(os.path.join(inputdir, Pickler.resolve_order_filename)).read()
        order = order.splitlines()
        return order


    def _checkTables(self, tables, order):
        '''make sure all table definitions are provided
        '''
        names = [t.getTableName() for t in tables]
        for t in order:
            assert t in names, "Table %r is not provided" % t
            continue
        return


    def _createName2TableMap(self, tables):
        m = {}
        for t in tables:
            m[t.getTableName()] = t
            continue
        return m
    

import os, pickle
        

# version
__id__ = "$Id$"

# End of file 
