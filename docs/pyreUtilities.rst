Utilities for pyre developers
=============================

Pythia-0.8/bin comes with a number of programmer's utilities.  There are templates for creating components and scipts.  For example, suppose one is creating a virtual laboratory and wishes to create a component for an nmr device.  One would simply type this at the command line::

 $component.py --name=NmrMachine

which generates::

    # -*- Python -*-
    #
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #
    #
    # {LicenseText}
    #
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #
    
    
    from pyre.components.Component import Component
    
    
    class NmrMachine(Component):
    
    
        class Inventory(Component.Inventory):
    
            import pyre.inventory
    
    
        def __init__(self, name):
            if name is None:
                name = 'facility'
    
            Component.__init__(self, name, facility='facility')
    
            return
    
    
        def _defaults(self):
            Component._defaults(self)
            return
    
    
        def _configure(self):
            Component._configure(self)
            return
    
    
        def _init(self):
            Component._init(self)
            return
    
    
    # version
    __id__ = "$Id$"
    
    # Generated automatically by PythonMill on Mon Jun 22 17:57:32 2009
    
    # End of file 

The same may also be done for scripts--a "hello world" script may be auto-generated using app.py in pyre.applications, and users may then customize that script to fit their needs.
    

