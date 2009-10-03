.. _pyre-basics:

Pyre basics: Inventory, Component, and Application
==================================================

.. The pyre framework is a Python-based system for constructing applications. Applications consist of a top level application component and a set of lower level components. The framework performs services such as instantiating components, configuring them, and cleaning up. A pyre component is the basic chunk of code managed by the pyre framework.  A component contains a "unit of functionality", whether one class or many, which requires certain settings before runtime.  A component may in turn pass settings to a subcomponent and so on.  The power of pyre is in taking an arbitrarily long, complex, interrelated set of configurations and being able to sort them out and pass them to all the underlying subcomponents so that they are configured in the correct order and dependencies are satisfied.

.. As the component "unit of functionality" is left undefined, it is up to the pyre architect to decide at what level they would like to divide their code into components.  Some may choose to create entire computational engines as components that can be swapped in and out based on a user's preferences.  Others may elect to fine-grain the component nature of their engines, such as creating components for a forcefield within a physics engine that can be altered at configuration time, or even the individual forcefield components.

.. Pyre is one package of pythia, a larger collection of related systems such as a distributed communication system (journal), code-generators (weaver), GUI generators (blade), and a build system (merlin).

If you have not read :ref:`the tutorial <pyre-tutorials>`, please read it through
and try out examples there to get a feeling of pyre components and pyre applications.
Here, we cover in more depth these key concepts in pyre:

 * Inventory

   * Trait(Descriptor)
   * Property
   * Facility

 * Component
 * Application
 

.. _pyre-inventory:

Inventory: properties and facilities
-----------------------------------------
In pyre, a component's inventory is the place where user inputs are 
connected to a pyre component.
In the inventory of a pyre component, all public configurable items
are declared using descriptors (traits).

Descriptors are special python objects that describe attributes
of a python instance.
If you want to know more about descriptors, this is a good place to start
http://users.rcn.com/python/download/Descriptor.htm. 

For details of how pyre inventory works, please consult
:ref:`pyre-inventory-implementation`.

There are two kinds of descriptors for a pyre inventory: properties or facilities.
All properties are instances of pyre.inventory.Property.Property, and usually they are instances of a property subclass, such as int, float, str, etc. The programmer can specify the public name of a property, a default value, and a validator. For example::

  import pyre.units.energy
  energy = pyre.inventory.dimensional(
      name='energy', 
      default=50*pyre.units.energy.meV, 
      validator=pyre.inventory.less(1*pyre.units.energy.eV))

Here the factory 
`pyre.inventory.dimensional </pyre/api/pyre.inventory-module.html#dimensional>`_
is a factory method creating a property of dimensional type, and all user inputs
for this property will be casted into this type.
For more factories, please consult 
`this page <http://danse.us/trac/pyre/browser/pythia-0.8/packages/pyre/pyre/inventory/__init__.py>`_ .
Keyword "name" specifies the name of the property, and this name will be
the key that pyre framework will use to find its user configuration.
Keyword "default" specifies the default value;
Keyword "validator" specifies a method that validate the user input.
In this example, a pyre built-in validator pyre.inventory.less is used.
You can find more builtin validators 
`here <http://danse.us/trac/pyre/browser/pythia-0.8/packages/pyre/pyre/inventory/__init__.py>`_ 
near the end of the file.



A facility is how one component (let's call it A) specifies that it would like another 
component to do some work for it. 
It's a bit like a help-wanted ad. 
As part of the facility declaration, A gets to recommend a default component to do the job,
or it can recommend a way to build a component to do the job 
(:ref:`factory <what-is-factory>`). 
Users get the final decision: they can direct that a different component be used, 
specifying that on the command line or through a configuration file (.pml).

In this example::

   greeter = pyre.inventory.facility(name='greeter', factory=Greeter)

A factory method is given and the default component is to be used is created from
calling the factory method

In this example::

   greeter = pyre.inventory.facility(name='greeter', default=Greeter())

A default component is specified.

The difference between this two approaches is that in the second case
the default component is one single instance, like a singleton.
This could lead to some strange behavior of your application if you
don't design your application carefully. 
On the other hand, using the first approach is a safe choice.

A full list of all invenetory properties is shown below:

.. automodule:: pyre.inventory.__init__
   :members: array bool dimensional float inputFile int list outputFile preformatted slice str
   :undoc-members:

.. automodule:: pyre.inventory.__init__
   :members: array bool dimensional float inputFile int list outputFile preformatted slice str
   :undoc-members:


   :exclude-members: codecPML 


.. _pyre-component:

Components
---------------

Pyre component structure is relatively straightforward.  The component class is inherited from pyre.inventory.Component.  It should contain an inner class called Inventory, which usually subclasses the Inventory class of the parent.  An example is Sentry, which performs the task of authenticating new users::

    from pyre.components.Component import Component
    
    
    class Sentry(Component):
    
    
        class Inventory(Component.Inventory):
    
            import pyre.inventory
    
            username = pyre.inventory.str('username')
            username.meta['tip'] = "the requestor's username"
    
            passwd = pyre.inventory.str('passwd')
            passwd.meta['tip'] = "the requestor's passwd"
    
            ticket = pyre.inventory.str('ticket')
            ticket.meta['tip'] = "the requestor's previously obtained ticket"
    
            attempts = pyre.inventory.int('attempts')
            attempts.meta['tip'] = "the number of unsuccessful attempts to login"
    
            import pyre.ipa
            ipa = pyre.inventory.facility("session", factory=pyre.ipa.session)
            ipa.meta['tip'] = "the ipa session manager"
    
    
        def authenticate(self):
	    ...
    
    
        def __init__(self, name=None):
            if name is None:
                name = 'sentry'
    
            super(Sentry, self).__init__(name)
	    ...    
    
    
        def _configure(self):
            Component._configure(self)
            self.username = self.inventory.username
            self.passwd = self.inventory.passwd
            self.ticket = self.inventory.ticket
            self.attempts = self.inventory.attempts
    
            self.ipa = self.inventory.ipa
    
            return

As a component, Sentry represents a "unit of functionality".  Note Inventory contains settings, such as username and password.  Allowed Inventory types are stored in the
`pyre.inventory <http://danse.us/trac/pyre/browser/pythia-0.8/packages/pyre/pyre/inventory/__init__.py>`_ 
package. 



.. automodule

Sentry's Inventory class also contains a reference to a subcomponent called "ipa".  Such references are termed facilities.  

Facilities: including and configuring pyre subcomponents 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Users place subcomponents in their inventory by specifiying a name and factory function::

  ipa = pyre.inventory.facility("session", factory=pyre.ipa.session)

The name "session" is the internal reference to ipa in the pyre framework. Facilities may be swapped in and out at run time using command line arguments or pml files as discussed in :ref:`odb-pml-files`.

Another thing to note is methods such as _defaults(), which communicate directly with the framework.  Examples of these include:

__init__(): the constructor
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The constructor must call the parent's constructor::

  super(Sentry, self).__init__(name)

Here the name argument specifies the name of this component (i.e. 'sentry'). 


_defaults(): setting default values
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Each command-line configurable item in the inventory may be given a default value when declared in the Inventory class. 
However, you may need to reset them based on some internal configuration within the component.  This maybe done in the _defaults method::

  self.inventory.username = 'bob'

and this will override the default value. However, if users specify another value
for this property through command line or configuration files, it will be overriden.


_configure(): transfer user inputs to local variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
During component configuration, external command-line or configuration file inputs are parsed by the framework,
checked for errors and stored in the object "self.inventory".
Any property or component is accessed as the attribute of this object.
For example, if you declare a string-type property in the inventory::

  filename = pyre.inventory.str('filename')

self.inventory.filename now contains the value of "filename" provided by the user.
In the _configure method, you can transfer this value to local variables of the component::

  self.filename = self.inventory.filename

allowing the component to use these external application-level inputs.


_init(): initialization of computing engine
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
This method will be called after every component is configured. 
The method _configure() will already have been called at this time for all components.
This is the place where the computing engine should be constructed.
Usually, in _init() one will want to prepare everything so that the
component is ready to run; for example, you may want to allocate memory,
open input/output files, initiate c/c++/fortran engines that this
component is depending on, etc.

.. TODO: have a link to a complete listing of these overidable methods 

.. TODO: discuss the order in which these methods are called by the framework

Applications
------------
A pyre application is simply the top-level component that can also be "executed".  
As such it can be run from the command line or started as a daemon.

Constructions of pyre applications are very similar to constructions
of pyre components.  Instead of subclassing pyre.components.Component.Component, you need to
subclass pyre.applications.Script.Script.
Also, all pyre applications must declare a method called "main",
which is called when the user instantiates the application and calls its run() method.

One of the strengths of pyre is a systematic way to configure and distribute from the command line all inventory items at run time.  As shown above, inventories are composed of both properties and facilities.  Changing a property on the command line is as simple as::

  application.py --property=value

but changing the subcomponent of a facility requires the presence of odb files, discussed next. 

.. _odb-files:

Swapping subcomponents
^^^^^^^^^^^^^^^^^^^^^^

To swap subcomponents one must have a factory function in a python file ending in odb.  This factory returns an instance of the subcomponent to be swapped.  For example, suppose we have a greeter component in :ref:`GreetApp <helloworld-greet.py>` from the tutorial::

     class GreetApp(Script):
     
         class Inventory(Script.Inventory):
     
             greeter = pyre.inventory.facility( 'greeter', default = Greeter('greeter') )
     
             ...

And we want to change the default choice of greeter to an odb file called morning.odb::

     # morning.odb

     from Greeter import Greeter
     
     def greeter():
         from Greeter import Greeter
         class Morning (Greeter):
             def _defaults(self): self.inventory.greetings = "Good morning"
         return Morning('morning')

By specifying a different greeter::

  $ python greet.py --greeter=morning
  Good morning World!

We swapped subcomponents dynamically.  

A key strength of pyre is an automatic system to specify all user inputs (items stored in the inventory of each component application) from either the command line or from an xml file.  In pyre these are pml files, discussed next.

.. _pml-files:

Pyre pml files
--------------

A .pml file is an xml file that assigns values to properties, components, and facilities in an application, allowing a user to override the default values assigned in the respective inventories.

To change the values of a property simply hand-edit the value, which has the general form::

    <property name='key'>value</property>

The name of the .pml file must be <component_name>.pml. Facilities may also be configured in a  similar manner::

    <facility name='greeter'>morning</facility>

.. _where-to-put-pml-odb:

There are several places to put .pml files, depending on the scope you'd like them to have.

   1. Files meant to override variables system-wide should be put with the pyre installation, in $EXPORT_ROOT/etc/<app_name>/<comp_name>.pml, where <app_name> is the name of the pyre app, and <comp_name> is the name of the component. For example, system-wide pml files for myApp.py should be in $EXPORT_ROOT/etc/myApp

   2. Files meant to override variables for just one user should be in a directory called .pyre immediately beneath the user's home directory. Example: /home/tim/.pyre/myApp

   3. Files meant to be local overrides should go in the local directory.  For example, for myApp.py one should have myApp.pml in that directory. 

The order of precedence is: 3 beats the others, 2 beats 1, and 1 beats whatever the default is. 


.. _mmtk:

Science tutorial: swapping molecular dynamics engines
=====================================================










..  also The inventory stores all the settings for the component as properties, as well as additional subcomponents as facilities.  Each of these may have multiple options.  For example, in the 

.. By having an explicit place to interact with the component, components gain the ability to control whether they accept a given change, and what to do with that setting.   External inputs such as those from the command line, a higher-level component, or a GUI, are stored in inventory items.    






