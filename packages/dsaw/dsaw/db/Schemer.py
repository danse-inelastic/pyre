#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
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
from pyre.db.Table import Table
import weakref

import dsaw.db
import numpy
from pyre.db.Schemer import Schemer as base

class Schemer(base):
    """scan the class record for implied attributes 
    and put those in columnRegistry.
    
    check if the types are
    actual instances of int,str,float,list,tuple,dict, a subclasses of Column, or a 
    reference to an object that is a subclass of Table
    and then attempt to store them if their name matches up   
    """

    def __init__(cls, name, bases, dict):    
        # the base class will get all the publicly declared columns and make them
        # part of the registry
        base.__init__(cls, name, bases, dict)

        #this should not go here--it should go in the dsaw-sqlalchemy converter
        #Schemer.automaticallyAssign(cls, name, bases, dict)
        
        # now get each column and add a weak reference to its table
        for name, item in cls._columnRegistry.iteritems():
            # XXX: Jiao Lin:
            # added so that the column descriptor knows
            # the table it belongs to
            item.parent_table = weakref.ref(cls)


    @staticmethod
    def automaticallyAssign(cls, name, bases, dict):
        # TODO: when this Schemer and pyre.db Schemer are combined, this registering
        # of classes should be combined
        
        #now we get the 'implied columns' (those without an explicit declaration)
        for name, item in cls.__dict__.iteritems():
            
            # disregard if parts of Schemer
            if name in ('Schemer','_columnRegistry','_writeable','name'):
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
            Schemer.assignType(cls, name, item)
            
            # i don't think we need this anymore so it's being commented out
#            if not cls._columnRegistry[item.name].auto:
#                cls.writeable.append(item.name)


    # for now just replace everything with a dsaw.db type...eventually use proxy class
    @staticmethod
    def assignType(cls, name, item):
        #attributeType = type(item).__name__ or for class do type(self).__name__
        if isinstance(item, basestring):
            dict[name]=dsaw.db.varchar(name=name, length=64, default=item)
            cls._columnRegistry[name] = dict[name]
        elif item.__class__.__name__=='int' or item.__class__.__name__=='long':
            cls.__dict__[name] = dsaw.db.integer(name=name, default=item)
            cls._columnRegistry[name] = cls.__dict__[name]
        elif isinstance(item, float):
            cls.__dict__[name] = dsaw.db.real(name=name, default=item)
            cls._columnRegistry[name] = cls.__dict__[name]
        elif item.__class__.__name__=='bool':
            cls.__dict__[name] = dsaw.db.boolean(name=name, default=item)
            cls._columnRegistry[name] = cls.__dict__[name]
        elif isinstance(item, list) or isinstance(item, numpy.ndarray) or isinstance(item, tuple):
            #we support nested arrays
    #            if isinstance(item[0],type(list)):
    #  
    #            else: 
            cls.__dict__[name] = dsaw.db.varcharArray(name=name, length=64, default=item)
            cls._columnRegistry[name] = cls.__dict__[name]
        elif isinstance(item, dict):
            cls._columnRegistry[name+'_keys'] = dsaw.db.varcharArray(name=name+'_keys', length=64, default=item.keys())
            cls._columnRegistry[name+'_keys'] = cls.__dict__[name+'_keys']
            cls._columnRegistry[name+'_values'] = dsaw.db.varcharArray(name=name+'_values', length=64, default=item.values())
            cls._columnRegistry[name+'_values'] = cls.__dict__[name+'_values']
        elif isinstance(item, Column):
            #this is taken care of for now by the parent Schemer
            pass
        elif isinstance(item, Table):
            cls.__dict__[name] = dsaw.db.reference(name=name, table=item.__class__)#, default=item)
            cls._columnRegistry[name] = cls.__dict__[name]
    #    elif isinstance(item, type(None)):
    #        cls._columnRegistry[name] = dsaw.db.varchar(name=name, length=64)
    

            
            
            


# version
__id__ = "$Id$"

# End of file 
