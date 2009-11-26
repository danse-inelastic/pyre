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

'''
for a class that has class attributes defined:

class A:

    x = 1.0
    s = "abc"
    b = B()

automatically generate a model.Inventory class
'''

class InventoryGenerator(object):

    opts = {
        'skip': None, # function(name, value) that returns boolean to indicate whether we should skip this attribute
        'references-are-owned': True, # by default, references auto-generated are acutally objects owned by the host object
        }

    def __init__(self, **kwds):
        self.opts = self.__class__.opts.copy()
        self.opts.update(kwds)
        return
    

    import types
    untranslatable_types = [
        types.BuiltinFunctionType, types.BuiltinMethodType, types.BufferType,
        types.ClassType, types.CodeType, types.DictionaryType, types.DictProxyType,
        types.FrameType, types.FunctionType,
        types.GeneratorType, types.GetSetDescriptorType,
        types.LambdaType,
        types.MemberDescriptorType, types.MethodType, types.ModuleType,
        types.NotImplementedType, 
        types.TracebackType, types.TypeType,
        types.UnboundMethodType,
        types.XRangeType,
        ]
    del types
    def __call__(self, kls):
        skip = self.opts.get('skip')

        descriptors = []
        
        for name, value in kls.__dict__.iteritems():
            # private attribute skip
            if name.startswith('_'): continue
            # skip classes
            if type(value) in self.untranslatable_types:
                continue
            # apply skip option
            if skip and skip(name=name, value=value):
                continue
            #
            descriptor = self._createDescriptor(name, value)
            descriptors.append(descriptor)
            continue

        class _(Inventory):
            for descriptor in descriptors:
                exec '%s=descriptor' % descriptor.name
            # clean up
            try:
                del descriptor
            except:
                pass
                
        return _


    def _createDescriptor(self, name, value):
        type = value.__class__.__name__
        handler = '_on'+type.capitalize()
        if handler in self.__class__.__dict__:
            handler = getattr(self, handler)
            return handler(name, value)
        return self._onReference(name, value)


    def _onStr(self, name, value):
        return Inventory.descriptors.str(name=name, default=value)


    def _onFloat(self, name, value):
        return Inventory.descriptors.float(name=name, default=value)
    
        
    def _onInt(self, name, value):
        return Inventory.descriptors.int(name=name, default=value)


    def _onBool(self, name, value):
        return Inventory.descriptors.bool(name=name, default=value)


    def _onList(self, name, value):
        elementtype = _getElementType(value)
        if not elementtype:
            return self._onReferenceSet(name, value)
        shape = _getShape(value)
        return Inventory.descriptors.array(
            name=name, default=value,
            elementtype=elementtype,
            shape = shape,
            )


    def _onReference(self, name, value):
        if value.__class__.__name__.startswith('Abstract'):
            return self._onPolymorphicReference(name, value)
        owned = self.opts['references-are-owned']
        return Inventory.descriptors.reference(name=name, default=value, targettype=value.__class__, owned=owned)


    def _onPolymorphicReference(self, name, value):
        return Inventory.descriptors.reference(name=name, default=value, targettype=None, owned=1)

    def _onReferenceSet(self, name, value):
        assert len(value)==1
        elem = value[0]
        if elem.__class__.__name__.startswith('Abstract'):
            targettype = None
        else:
            targettype = elem.__class__
        owned = self.opts['references-are-owned']
        return Inventory.descriptors.referenceSet(
            name=name, targettype=targettype, owned=owned)
        
    pass


from dsaw.model.Inventory import Inventory


import numpy
def _getElementType(l):
    try:
        l1 = numpy.array(l)
    except:
        return
    shape = l1.shape
    dims = len(shape)
    e0 = l1[tuple([0]*dims)]
    t = type(e0).__name__
    if t.startswith('str'):
        try:
            s = str(e0)
        except:
            return
        return 'str'
    elif t.startswith('int'):
        try:
            s = int(e0)
        except:
            return
        return 'str'
    elif t.startswith('float'):
        try:
            s = float(e0)
        except:
            return
        return 'float'
    elif t.startswith('bool'):
        try:
            s = bool(e0)
        except:
            return
        return 'bool'
    return


def _getShape(l):
    return numpy.array(l).shape

# version
__id__ = "$Id$"

# End of file 
