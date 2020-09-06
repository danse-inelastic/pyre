#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                             Michael A.G. Aivazis
#                      California Institute of Technology
#                      (C) 1998-2005  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


import sys
from future.utils import with_metaclass

from .Trait import Trait
from .Interface import Interface

class Facility(with_metaclass(Interface, Trait)):

    def __init__(self, name, family=None, default=None, factory=None, args=(), meta=None):
        Trait.__init__(self, name, 'facility', default, meta)

        self.args = args
        self.factory = factory

        if family is None:
            family = name
        self.family = family

        return

    def _getDefaultValue(self, instance):
        component = self.default

        # build a default locator
        import pyre.parsing.locators
        here = pyre.parsing.locators.simple('default')

        if component is not None:
            # if we got a string, resolve
            if sys.version_info[:2] == (2, 7): 
                if isinstance(component, basestring):
                    component, locator = self._retrieveComponent(instance, component, args=())
                    here = pyre.parsing.locators.chain(locator, here)
            elif sys.version_info[0] == (3,):
                if isinstance(component, str):
                    component, locator = self._retrieveComponent(instance, component, args=())
                    here = pyre.parsing.locators.chain(locator, here)
            else:
                raise RuntimeError("Incompatible version of Python. This code requires Python 2.7 or Python 3.") 
                
            return component, here

        if self.factory is not None:
            # instantiate the component
            component =  self.factory(*self.args)
            # adjust the configuration aliases to include my name
            aliases = component.aliases
            if self.name not in aliases:
                aliases.append(self.name)
            
            # build a default locator
            import pyre.parsing.locators
            locator = pyre.parsing.locators.simple('default')
            # return
            return component, locator

        # oops: expect exceptions galore!
        import journal
        firewall = journal.firewall('pyre.inventory')
        firewall.log(
            "facility {0!r} was given neither a default value nor a factory method".format(self.name))
        return None, None


    def _set(self, instance, component, locator):
        if sys.version_info[:2] == (2,7):
            if isinstance(component, basestring):
                try:
                    name, args = component.split(":")
                    args = args.split(",")
                except ValueError:
                    name = component
                    args = []
                
                component, source = self._retrieveComponent(instance, name, args)

                import pyre.parsing.locators
                locator = pyre.parsing.locators.chain(source, locator)
        elif sys.version_info[0] == (3,):
            if isinstance(component, str):
                try:
                    name, args = component.split(":")
                    args = args.split(",")
                except ValueError:
                    name = component
                    args = []
                
                component, source = self._retrieveComponent(instance, name, args)

                import pyre.parsing.locators
                locator = pyre.parsing.locators.chain(source, locator)
        else:
            raise RuntimeError("Incompatible version of Python. This code requires Python 2.7 or Python 3.") 

        if component is None:
            return

        # get the old component
        try:
            old = instance._getTraitValue(self.name)
        except KeyError:
            # the binding was uninitialized
            return instance._initializeTraitValue(self.name, component, locator)

        # if the previous binding was non-null, finalize it
        if old:
            old.fini()
        
        # bind the new value
        return instance._setTraitValue(self.name, component, locator)


    def _retrieveComponent(self, instance, componentName, args):
        component = instance.retrieveComponent(name=componentName, factory=self.family, args=args)

        if component is not None:
            locator = component.getLocator()
        else:
            import pyre.parsing.locators
            imported = self._import(componentName)
            if imported:
                component, file = imported
            else:
                component = None

            if component:
                locator = pyre.parsing.locators.simple('imported from {0!s}'.format(file))
            else:
                locator = pyre.parsing.locators.simple('not found')

                return None, locator

        # adjust the names by which this component is known
        component.aliases.append(self.name)
            
        return component, locator


    def _import(self, name):
        # convert 'a/b/c' to 'a.b.c' so we can directly import the module
        # 'a/b/c' is better than 'a.b.c' because command line configuration in pyre 0.8
        # won't work for components with names including dots.
        name  = name.replace('/', '.')
        try:
            module = __import__(name, {}, {}, [''])
        except ImportError:
            import traceback
            tb = traceback.format_exc()
            
            import journal
            journal.error("pyre.inventory").log(
                "could not bind facility '{0!s}': component '{1!s}' not found:\n{2!s}".format(self.name, name, tb))
            return
        except ValueError:
            import traceback
            tb = traceback.format_exc()
            
            import journal
            journal.error("pyre.inventory").log(
                "could not bind facility '{0!s}': component '{1!s}' not found:\n{2!s}".format(self.name, name, tb))
            return

        try:
            factory = module.__dict__[self.family]
        except KeyError:
            import journal
            journal.error("pyre.inventory").log(
                "no factory for facility '{0!s}' in '{1!s}'".format(self.name, module.__file__))
            return

        try:
            item = factory(*self.args)
        except TypeError:
            import journal
            journal.error("pyre.inventory").log(
                "no factory for facility '{0!s}' in '{1!s}'".format(self.name, module.__file__))
            return

        return item, module.__file__


    # interface registry
    _interfaceRegistry = {}

# version
__id__ = "$Id: Facility.py,v 1.1.1.1 2006-11-27 00:10:00 aivazis Exp $"

# End of file 
