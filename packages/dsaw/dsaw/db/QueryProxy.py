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


class QueryProxy(object):

    def __init__(self, sa_query, db):
        self.sa_query = sa_query
        self.db = db
        return


    def __getattr__(self, name):
        f = getattr(self.sa_query, name)
        if callable(f): return QueryCallProxy(f, self.db)
        return f


class QueryCallProxy(object):

    def __init__(self, f, db):
        self.callable = f
        self.db = db
        return


    def __call__(self, *args, **kwds):
        args = list(args)
        for i, arg in enumerate(args):
            if isinstance(arg, QueryProxy):
                args[i] = arg.sa_query
                
        ret = self.callable(*args, **kwds)
        if isinstance(ret, SAQuery): return QueryProxy(ret, self.db)

        # XXX: this is not a good implementation. please improve
        try: 
            return map(self.db.objectToRecord, ret)
        except:
            try:
                return self.db.objectToRecord(ret)
            except:
                return ret


from sqlalchemy.orm.query import Query as SAQuery

# version
__id__ = "$Id$"

# End of file 
