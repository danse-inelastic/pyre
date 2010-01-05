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


def array(**kwds):
    """array(name, elementtype=, default=, validator=,
    elementconverter=, elementvalidator=, shape=, string_max_length=)

    string_max_length: only good when elementtype is str
    """
    return Array(**kwds)

def date(**kwds):
    '''str(name, default=, validator=)
    '''
    return Date(**kwds)

def reference(**kwds):
    return Reference(**kwds)

def referenceSet(**kwds):
    return ReferenceSet(**kwds)

import pyre.inventory
def str(**kwds):
    '''str(name, default=, validator=, max_length=)
    '''
    return _hackProperty(pyre.inventory.str, **kwds)
def float(**kwds):
    '''float(name, default=, validator=)
    '''
    return _hackProperty(pyre.inventory.float, **kwds)
def bool(**kwds):
    '''bool(name, default=, validator=)
    '''
    return _hackProperty(pyre.inventory.bool, **kwds)
def int(**kwds):
    '''int(name, default=, validator=)
    '''
    return _hackProperty(pyre.inventory.int, **kwds)



# pyre.inventory.Property does not accept arguments other than those
# in the following list, so we have to use this hackish approach.
_keys_for_original_property_class = [
    'name', 'type', 'default', 'validator', 'meta',
    ]
def _hackProperty(factory, **kwds):
    kwds2 = {}
    others = {}
    for k, v in kwds.iteritems():
        if k in _keys_for_original_property_class:
            kwds2[k] = v
        else:
            others[k] = v
        continue
    r = factory(**kwds2)
    for k, v in others.iteritems():
        setattr(r, k, v)
    return r
    

from pyre.inventory.Property import Property as base

class Date(base):
    
    def __init__(self, name, default=None, meta=None, validator=None):
        base.__init__(self, name, "date", default, meta)
        return

    def __get__(self, instance, cls=None):
        ret = base.__get__(self, instance, cls = cls)
        if ret is None:
            import time
            return time.ctime()
        return ret

import numpy
class Array(base):

    def __init__(self, name, elementtype=None, default=None, validator=None, elementconverter=None, elementvalidator=None, shape=None, **kwds):
        if elementtype not in ['str', 'bool', 'int', 'float']:
            raise NotImplementedError
        
        if not elementconverter:
            elementconverter = __builtins__[elementtype]

        self.elementconverter = elementconverter # this is not in use yet. should be useful when elementtype is not limited to basic types str, bool, int, float
        
        self.elementtype = elementtype
        self.elementvalidator = elementvalidator
        self.shape = shape

        validator = self._createValidator(validator, elementvalidator)
        
        super(Array, self).__init__(
            name, "array",
            default=default, validator=validator,
            **kwds
            )
        return


    def _createValidator(self, validator, elementvalidator):
        if elementvalidator:
            vev = numpy.vectorize(elementvalidator)
        else:
            vev = None
        if validator:
            if vev:
                def _(value):
                    return validator(vev(value))
                return _
            else:
                return validator
        else:
            return vev
        raise RuntimeError        

        
    def _cast(self, text):
        if isinstance(text, basestring):
            if text and text[0] in '[({':
                text = text[1:]
            if text and text[-1] in '])}':
                text = text[:-1]
                
            value = text.split(",")
        else:
            value = text

        try:
            value = numpy.array(value, dtype=self.elementtype)
        except:
            import traceback as tb
            raise TypeError(
                "property '%s': could not convert '%s' to an array of %ss.\n%s" % (
                self.name, text, self.elementtype, tb.format_exc()))

        if self.shape:
            try:
                value.shape = self.shape
            except:
                raise ValueError, "shape mismatch: cannot cast %r to an array of shape %s" % (
                    value, self.shape)
        return value
   
        
class Property(base):

    def __init__(self, name, type, default=None, validator=None, **kwds):
        super(Property, self).__init__(name, type, default, validator)
        for k, v in kwds.iteritems():
            setattr(self, k, v)
        return


class ReferenceSet(Property):

    
    def __init__(self, name=None, targettype=None, targettypes=[], owned=False,
                 default=None, validator=None, **kwds):
        default = self._cast(default)
        self._checkTargetTypes(targettypes)
        super(ReferenceSet, self).__init__(
            name, "referenceset",
            default=default, validator=validator,
            targettype=targettype, targettypes=targettypes,
            owned=owned,
            **kwds
            )
        return
    
    
    def isPolymorphic(self):
        return self.targettype is None or self.targettype.__name__.startswith('Abstract')


    def _cast(self, value):
        value = value or []
        return value


    def _checkTargetTypes(self, targettypes):
        import inspect
        for t in targettypes:
            assert inspect.isclass(t), "%s is not a type" % (t,)



class Reference(Property):


    def __init__(self, name=None, targettype=None, targettypes=[], owned=False,
                 default=None, validator=None, **kwds):
        self._checkTargetTypes(targettypes)
        super(Reference, self).__init__(
            name, "reference",
            default=default, validator=validator,
            targettype=targettype, targettypes=targettypes,
            owned=owned,
            **kwds
            )
        return
    
    
    def isPolymorphic(self):
        return self.targettype is None or self.targettype.__name__.startswith('Abstract')
    
    
    def _cast(self, value):
        # 
        return value


    def _checkTargetTypes(self, targettypes):
        import inspect
        for t in targettypes:
            assert inspect.isclass(t), "%s is not a type" % (t,)


import _validators as validators


# version
__id__ = "$Id$"

# End of file 
