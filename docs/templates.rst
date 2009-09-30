.. _templates:

Pyre templates
==============

Create a component or application templates
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Pythia-0.8/bin comes with a number of programmer's utilities, including scripts for creating component and application templates.  For example, suppose one is creating a virtual laboratory and wishes to create a component for an nmr device.  One would simply type this at the command line::

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

Create a pml template
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
  

Create a pyre service template
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Service templates can be generated using the service.py script distributed with pyre::

    $ python service.py --name=giveAdvice
    creating service 'giveAdvice' in 'giveAdvice.py'

generates a file containing this::

    # -*- Python -*-
    #
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #
    #
    # {LicenseText}
    #
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #
    
    
    from pyre.components.Service import Service
    
    
    class giveAdvice(Service):
    
    
        class Inventory(Service.Inventory):
    
            import pyre.inventory
    
    
        def serve(self):
            return
    
    
        def __init__(self, name=None):
            if name is None:
                name = 'service'
    
            Service.__init__(self, name)
    
            return
    
    
        def _defaults(self):
            Service._defaults(self)
            return
    
    
        def _configure(self):
            Service._configure(self)
            return
    
    
        def _init(self):
            Service._init(self)
            return
    
    
    # version
    __id__ = "$Id$"
    
    # Generated automatically by PythonMill on Tue Jun 30 10:03:10 2009
    
    # End of file 


.. _create-a-pyre-project:

Create a pyre project template
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Pyre project directory templates can be generated using the package.sh utility. Simply type the utility followed by the name of the project, such as "CoolIdea"::

    $ package.sh CoolIdea
    $ cd CoolIdea/
    $ ls
    CoolIdea  CoolIdeamodule  examples  libCoolIdea  Make.mm  tests
    $ ls CoolIdea
    __init__.py  Make.mm
    $ ls CoolIdeamodule/
    bindings.cc  CoolIdeamodule.cc  exceptions.h  Make.mm  misc.h
    bindings.h   exceptions.cc      local.def     misc.cc
    $ ls libCoolIdea/
    hello.cc  hello.h  local.def  Make.mm
    $ ls tests/
    hello.cc  Make.mm  signon.py

and :ref:`traditional pyre directories <pyre-directory-structure>` will be generated below a directory with the indicated name, each filled with Make.mm files and initialization files.


