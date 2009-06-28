Utilities for pyre developers
=============================

Create a component or application skeleton
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Pythia-0.8/bin comes with a number of programmer's utilities.  There are templates for creating components and scipts.  For example, suppose one is creating a virtual laboratory and wishes to create a component for an nmr device.  One would simply type this at the command line::

 $ component.py --name=NmrMachine

which generates::

    # -*- Python -*-
    #
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # {LicenseText}
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
    
    # End of file 

The same may also be done for scripts--a "hello world" script may be auto-generated using app.py in pyre.applications, and users may then customize that script to fit their needs::

  $ app.py --name=myapp-name

Create a pml skeleton
^^^^^^^^^^^^^^^^^^^^^

Empty pml files can be generated using the inventory.py script distributed with pyre. For example, to generate a pml file for a component named "test"::

    $ python inventory.py --name=test
    creating inventory template in 'test.pml'

generates a file containing this::

    <?xml version="1.0"?>
    <!--
    ! ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~!
    ! {LicenseText}
    ! ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~-->
    
    
    <!DOCTYPE inventory>
    
    <inventory>
    
      <component name='test'>
        <property name='key'>value</property>
      </component>
    
    </inventory>
    
    
    <!-- version-->
    <!-- $Id$-->
    
    <!-- Generated automatically by XMLMill on Tue Apr 12 17:36:35 2005-->
    
    <!-- End of file -->
  

