Pyre basics: Inventory, Component, and Application
==================================================

.. The pyre framework is a Python-based system for constructing applications. Applications consist of a top level application component and a set of lower level components. The framework performs services such as instantiating components, configuring them, and cleaning up. A pyre component is the basic chunk of code managed by the pyre framework.  A component contains a "unit of functionality", whether one class or many, which requires certain settings before runtime.  A component may in turn pass settings to a subcomponent and so on.  The power of pyre is in taking an arbitrarily long, complex, interrelated set of configurations and being able to sort them out and pass them to all the underlying subcomponents so that they are configured in the correct order and dependencies are satisfied.

.. As the component "unit of functionality" is left undefined, it is up to the pyre architect to decide at what level they would like to divide their code into components.  Some may choose to create entire computational engines as components that can be swapped in and out based on a user's preferences.  Others may elect to fine-grain the component nature of their engines, such as creating components for a forcefield within a physics engine that can be altered at configuration time, or even the individual forcefield components.

.. Pyre is one package of pythia, a larger collection of related systems such as a distributed communication system (journal), code-generators (weaver), GUI generators (blade), and a build system (merlin).

If you have not read :ref:`the tutorial <pyre-tutorials>`, please read it through
and try out examples there to get a feeling of pyre components and pyre applications.
Here, we are trying to explain a few key concepts in pyre:

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
`pyre.inventory.dimensional <http://docs.danse.us/pyre/pythia-0.8/pyre.inventory-module.html#dimensional>`_
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


.. _pyre-component:

Components
---------------

Pyre component structure is relatively straightforward.  The component class is inherited from pyre.inventory.Component.  It should contain an inner class called Inventory, which usually subclass the Inventory class of the parent component class.  An example is::

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
            ipa = pyre.inventory.facility("session", family="ipa", factory=pyre.ipa.session)
            ipa.meta['tip'] = "the ipa session manager"
    
    
        def authenticate(self):
	    ...
    
    
        def __init__(self, name=None):
            if name is None:
                name = 'sentry'
    
            super(Sentry, self).__init__(name, facility='sentry')
	    ...    
    
    
        def _configure(self):
            Component._configure(self)
            self.username = self.inventory.username
            self.passwd = self.inventory.passwd
            self.ticket = self.inventory.ticket
            self.attempts = self.inventory.attempts
    
            self.ipa = self.inventory.ipa
    
            return

Note the presence of an inner class called Inventory, which contains settings such as username and password, as well as specifications of subcomponents (ipa).  Allowed inventory types are stored in the
`pyre.inventory <http://danse.us/trac/pyre/browser/pythia-0.8/packages/pyre/pyre/inventory/__init__.py>`_ 
package. 

Methods that are useful to communicate to pyre framework for a pyre component are:

__init__: the constructor
^^^^^^^^^^^^^^^^^^^^^^^^^
The constructor must contains a call to parent's constructor::

            super(Sentry, self).__init__(name, facility='sentry')

here the name is the name of this component, and it is the key that pyre framework
uses to look for its configuration.


_defaults: setting default values
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
You can set the default value for an inventory item when declaring them 
in the Inventory class. 
Beyond that, you get another chance to set the default values
in this _defaults method.
You can do sth like ::

  self.inventory.username = 'bob'

and this will override the default value. But if users specify another value
for this property thruough command line or configuration files, it will
be overriden.


_configure: transfer user inputs to local variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
In the _configure method, the user inputs are already parsed by the framework,
checked for errors, and store in the object "self.inventory".
Any property or component is accessed as the attribute of this inventory object.
For example, if you declare a str property in the inventory::

  filename = pyre.inventory.str('filename')

self.inventory.filename now contains the value of "filename" provided by user.
In the _configure method, you could transfer this value to local variables of this
component::

  self.filename = self.inventory.filename

_init: initialization of computing engine
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
This method will be called after every component is configured. 
The method _configure
for all components will be called already at this time.
This is the place where the computing engine should be constructed.



Layered structure of pyre
^^^^^^^^^^^^^^^^^^^^^^^^^
Pyre encourages decomposition of large, complex computing system to small, dedicated
computing engines by providing a architecture allowing construction of
components in a layored structure. 
:ref:`Application greet.py <helloworld-greet.py>` is a good example
showing the benefit of decomposition.


More texts here...


.. Sentry, represents a "unit of functionality" in the opal web framework.  It performs the task of authenticating new users.  As such it contains a subcomponent called Ipa which manages sessions, either by authenticating new logins against a database or keeping track of login time and issuing tickets to authenticate.  As such Ipa must maintain state, and is, in fact, a daemon.  However, it is treated exactly like any other subcomponent by Sentry.  As a subcomponent Ipa is stored in Sentry's inventory as a facility, whose method signature is pyre.inventory.facility("session", family="ipa", factory=pyre.ipa.session), containing a name, family, and factory.  These are all discussed in the next section.  



Applications
------------
A pyre application is simply the top-level component that can also be "executed".  
As such it can be run from the command line or started as a daemon.

Constructions of pyre applications are very similar to constructions
of pyre components. 
Here is 
`an example <tutorials/greet.py>`_
.

Instead of subclassing pyre.components.Component.Component, you need to
subclass pyre.applications.Script.Script.
Other than that, all pyre applications must declare method "main",
which is like the "main" function in c/c++.



Pyre .odb and .pml files
------------------------

A .pml file is an XML file that assigns values to properties, components, and facilities in an application, allowing a user to override the default values assigned in the respective inventories.

The name of the .pml file must be <component_name>.pml.

Change value of a property
^^^^^^^^^^^^^^^^^^^^^^^^^^

By editing this file one can change the properties of the application named "test". For instance, suppose test has a property named "property1", and you want to set it to 3.14159. You could edit the line::

    <property name='key'>value</property>

to read::

    <property name='property1'>3.14159</property>

.

See also 
:ref:`where to put .pml files<where-to-put-pml-odb>`
.


Change the component for a facility
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Say if we have a greeter component in our hello application::

     class Hello(Script):
     
         class Inventory(Script.Inventory):
     
             greeter = pyre.inventory.facility( 'greeter', default = Greeter('greeter') )
     
             ...

And we want to change the default choice of greeter to a odb file called morning.odb::

     # morning.odb

     from Greeter import Greeter
     
     def greeter():
         from Greeter import Greeter
         class Morning (Greeter):
             def _defaults(self): self.inventory.greetings = "Good morning"
         return Morning('morning')


What we could do is to change the application pml file hello.pml::

       <facility name='greeter'>morning</facility>


.. _where-to-put-pml-odb:

Where to put .pml/.odb files
----------------------------

There are several places to put .pml files, depending on the scope you'd like them to have.

   1. Files meant to override variables system-wide should be put with the pyre installation, in pythia-m.n/etc/<comp_name>/<comp_name>.pml, where m.n is the pythia version number, and <comp_name> is the name of the component. Example: the system-wide .pml file for myApp with pythia-0.8 should be .../pythia-0.8/etc/myApp/myApp.pml
   2. Files meant to override variables for just one user should be in a directory called .pyre immediately beneath the user's home directory. Example: /home/tim/.pyre/myApp/myApp.pml
   3. Files meant to be local overrides should go in the local directory: ./myApp.pml 

3 beats the others, 2 beats 1, 1 beats whatever the default is. 












..  also The inventory stores all the settings for the component as properties, as well as additional subcomponents as facilities.  Each of these may have multiple options.  For example, in the 

.. By having an explicit place to interact with the component, components gain the ability to control whether they accept a given change, and what to do with that setting.   External inputs such as those from the command line, a higher-level component, or a GUI, are stored in inventory items.    




.. (incorporate pyre class diagrams, possibly activity diagrams)




