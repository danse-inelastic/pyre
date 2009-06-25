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



.. Sentry, represents a "unit of functionality" in the opal web framework.  It performs the task of authenticating new users.  As such it contains a subcomponent called Ipa which manages sessions, either by authenticating new logins against a database or keeping track of login time and issuing tickets to authenticate.  As such Ipa must maintain state, and is, in fact, a daemon.  However, it is treated exactly like any other subcomponent by Sentry.  As a subcomponent Ipa is stored in Sentry's inventory as a facility, whose method signature is pyre.inventory.facility("session", family="ipa", factory=pyre.ipa.session), containing a name, family, and factory.  These are all discussed in the next section.  



Applications
------------
Pyre applications are special kind of pyre components.
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

The name of the .pml file must be <applicationName>.pml.

Empty pml files can be generated using the inventory.py script distributed with pyre. For example, to generate a pml file for the application named "test"::

    $ python inventory.py --name=test
    creating inventory template in 'test.pml'

generates a file containing this::

    <?xml version="1.0"?>
    <!--
    ! ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~!
    !                                 T. M. Kelley
    !                   (C) Copyright 2005  All Rights Reserved
    !
    ! {LicenseText}
    !
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

By editing this file one can change the properties of the application named "test". For instance, suppose test has a property named "property1", and you want to set it to 3.14159. You could edit the line::

    <property name='key'>value</property>

to read::

    <property name='property1'>3.14159</property>

.

See also where to put .pml files
[edit]
change the choice of a component

Say if we have a greeter component in our hello application::

     class Hello(Script):
     
         class Inventory(Script.Inventory):
     
             greeter = pyre.inventory.facility( 'greeter', default = Greeter('greeter') )
     
             ...

And we want to change the default choice of greeter to a odb file called morning.odb::

 #morning.odb
     from Greeter import Greeter
     
     def greeter():
         from Greeter import Greeter
         class Morning (Greeter):
             def _defaults(self): self.inventory.greeting = "Good morning"
         return Morning('morning')

What we could do is to change the application pml file hello.pml::

     <component name='hello'>
       <facility name='greeter'>morning</facility>

Where to put .pml files
-----------------------

There are several places to put .pml files, depending on the scope you'd like them to have.

   1. Files meant to override variables system-wide should be put with the pyre installation, in pythia-m.n/etc/<comp_name>/<comp_name>.pml, where m.n is the pythia version number, and <comp_name> is the name of the component. Example: the system-wide .pml file for myApp with pythia-0.8 should be .../pythia-0.8/etc/myApp/myApp.pml
   2. Files meant to override variables for just one user should be in a directory called .pyre immediately beneath the user's home directory. Example: /home/tim/.pyre/myApp/myApp.pml
   3. Files meant to be local overrides should go in the local directory: ./myApp.pml 

3 beats the others, 2 beats 1, 1 beats whatever the default is. 












 also The inventory stores all the settings for the component as properties, as well as additional subcomponents as facilities.  Each of these may have multiple options.  For example, in the 

By having an explicit place to interact with the component, components gain the ability to control whether they accept a given change, and what to do with that setting.   External inputs such as those from the command line, a higher-level component, or a GUI, are stored in inventory items.    




(incorporate pyre class diagrams, possibly activity diagrams)

A script is simply the top-level component that can also be "executed".  As such it can be run from the command line, started as a daemon, or copied to a remote cluster and put in a scheduler. A script inherits from the Script class in pyre.applications.Script. An example is::

    from pyre.applications.Script import Script
    
    
    class DbApp(Script):
    
    
        class Inventory(Script.Inventory):
    
            import pyre.inventory
    
            import vnf.components
            clerk = pyre.inventory.facility(name="clerk", factory=vnf.components.clerk)
            clerk.meta['tip'] = "the component that retrieves data from the various database tables"
    
            import pyre.idd
            idd = pyre.inventory.facility('idd-session', factory=pyre.idd.session, args=['idd-session'])
            idd.meta['tip'] = "access to the token server"
    
            wwwuser = pyre.inventory.str(name='wwwuser', default='')
    
            tables = pyre.inventory.list(name='tables', default=[])
    
    
        def main(self, *args, **kwds):
    
            self.db.autocommit(True)
    
            tables = self.tables
            if not tables:
                from vnf.dom import alltables
                tables = alltables()
            else:
                tables = [self.clerk._getTable(t) for t in tables]
    
            for table in tables:
                #self.dropTable( table )
                self.createTable( table )
                if self.wwwuser: self.enableWWWUser( table )
                continue
    
            for table in tables:
                self.initTable( table )
    
            return
    
    
        def createTable(self, table):
            # create the component table
            print " -- creating table %r" % table.name
            try:
                self.db.createTable(table)
            except self.db.ProgrammingError, msg:
                print "    failed; table exists?"
                print msg
            else:
                print "    success"
    
            return
    
    
        def dropTable(self, table):
            print " -- dropping table %r" % table.name
            try:
                self.db.dropTable(table)
            except self.db.ProgrammingError:
                print "    failed; table doesn't exist?"
            else:
                print "    success"
    
            return
    
    
        def initTable(self, table):
            module = table.__module__
            m = __import__( module, {}, {}, [''] )
            inittable = m.__dict__.get( 'inittable' )
            if inittable is None: return
            print " -- Inialize table %r" % table.name
            try:
                inittable( self.db )
            except self.db.IntegrityError:
                print "    failed; records already exist?"
            else:
                print "    success"
                
            return
    
    
        def enableWWWUser(self, table):
            print " -- Enable www user %r for table %r" % (self.wwwuser, table.name)
            sql = 'grant all on table "%s" to "%s"' % (table.name, self.wwwuser)
            c = self.db.cursor()
            c.execute(sql)
            return
    
    
        def __init__(self):
            Script.__init__(self, 'initdb')
            self.db = None
            return
    
    
        def _configure(self):
            Script._configure(self)
            self.clerk = self.inventory.clerk
            self.clerk.director = self
            self.wwwuser = self.inventory.wwwuser
            self.tables = self.inventory.tables
            return
    
    
        def _init(self):
            Script._init(self)
    
            self.db = self.clerk.db
            self.idd = self.inventory.idd
    
            # initialize table registry
            import vnf.dom
            vnf.dom.register_alltables()
    
            # id generator
            def guid(): return '%s' % self.idd.token().locator
            import vnf.dom
            vnf.dom.set_idgenerator( guid )
            return
    
    
        def _getPrivateDepositoryLocations(self):
            return ['../config']
        
    
    
    def runScript():
        import journal
        journal.debug('db').activate()
        app = DbApp()
        return app.run()
    
    
    if __name__ == '__main__':
        runScript()

This application does....Notice the only real difference between a script and a Component is that it has a main() method. It is instantiated in the typical way and then executed by calling the run() method of the superclass pyre.applications.Script.







Binding
---------
Binding is the process of making a piece of code callable. In the DANSE project, we frequently use Python bindings for code written in C, C++, and FORTRAN; that means that we use pieces of code that make functions written in those languages callable from Python. Python bindings involve several components including wrappers; the process is described in Writing C extensions for Python.

Template
----------
In C++, a template function (or class) is a technique for defining function (or class) implementation while not specifying types used in the interface. Loosely speaking, templates define implementation but leave interface to be defined later, while inheritance defines interface but delays deciding implementation.

For example, suppose you have two functions:

float addf(float a, float b){return a + b;}
double add( double a, double b){return a + b;}

One template function could replace both of these functions:

template <typename T> 
T add( T a, T b){ return a + b;}

This simplifies writing the code: there's only one function to keep track of, instead of one function for every type. Strictly speaking, this is not a function definition: it is a blueprint for the compiler to create a function definition ("instantiate" the template). The programmer has deferred until later the decision of what type(s) to use in this function. This function will work for any type for which the "+" operator is defined.

The person using this function has to make it clear to the compiler which types are to be involved:

float a=1.2, b=2.3;
float c = add<float>( a,b);

double d = 3.4, e = 4.5;
double f = add<double>( d, e);


Wrapping
---------
Wrapping is the process of providing a new interface to an already existing piece of code. The code that does this is a wrappe





