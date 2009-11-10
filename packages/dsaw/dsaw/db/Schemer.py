#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                  Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


# Modified from pyre.db.Schemer
# 


from Column import Column
import weakref


from pyre.db.Schemer import Schemer as base

class Schemer(base):
    """scan the class record for implied attributes 
    and put those in columnRegistry.
    
    check if the types are
    actual instances of int,str,float,list,tuple,dict, a subclasses of Column, or a 
    reference to an object that is a subclass of Table
    and then attempt to store them if their name matches up   
    
    todo: add possibility of getting table name from the class name.lower()
    """

    def __init__(cls, name, bases, dict):    
        # the base class will get all the publicly declared columns and make them
        # part of the registry
        base.__init__(cls, name, bases, dict)
        # TODO: when this Schemer and pyre.db Schemer are combined, this registering
        # of classes should be combined
        
        #now we get the 'implied columns' (those without an explicit declaration)
        for name, item in cls.__dict__.iteritems():
            
#            if name in ('Schemer','_columnRegistry','_writeable','name','dsaw','VersatileReference'):
#                continue
            if name in ('_columnRegistry','_writeable','name'):
                continue
            # disregard entries that are already in the column registry
            if name in cls._columnRegistry.keys():
                continue
            # disregard metadata
            if name[:2]=='__' and name[-2:]=='__':
                continue
#            # disregard functions
#            if type(item).__name__=='function':
#                continue

            # register it and apply automatic type detector
            assignType(cls, item)
            
            if not cls._columnRegistry[item.name].auto:
                cls.writeable.append(item.name)
        
        # now get each column and add a weak reference to it's table
        for name, item in cls._columnRegistry.iteritems():
            # XXX: Jiao Lin:
            # added so that the column descriptor knows
            # the table it belongs to
            item.parent_table = weakref.ref(cls)

        return
    
def assignType(cls, item):
    # this could obviously be expanded
    import dsaw.db
    #attributeType = type(item).__name__ or for class do type(self).__name__
    if isinstance(item,type(1)):
        cls._columnRegistry[item.name] = dsaw.db.integer(name=item.name, default=item)
    elif isinstance(item,type(1.0)):
        cls._columnRegistry[item.name] = dsaw.db.double(name=item.name, default=item)
    elif isinstance(item,type([])) or isinstance(item,type((1,))):
        cls._columnRegistry[item.name] = dsaw.db.varcharArray(name=item.name, length=64, default=item)
    elif isinstance(item,type({})):
        cls._columnRegistry[item.name+'_keys'] = dsaw.db.varcharArray(name=item.name+'_keys', length=64, default=item.keys())
        cls._columnRegistry[item.name+'_values'] = dsaw.db.varcharArray(name=item.name+'_values', length=64, default=item.values())
    elif isinstance(item,type('abc')):
        cls._columnRegistry[item.name] = dsaw.db.varchar(name=item.name, length=64, default=item)
    elif isinstance(item, Column):
        #this is taken care of for now by the parent Schemer
        pass
    elif isinstance(item, Table):
        cls._columnRegistry[item.name] = dsaw.db.reference()

            
            
            


# version
__id__ = "$Id$"

# End of file 
