Intermediate Pyre
=================

.. _pyre-directory-structure:

Pyre Project Structure
------------------------

A pyre project typically contains a number of directories.  For example, supposing one wishes to create a pyre module wrapping several plane wave abinitio codes.  The pyre application directory structure would be configured with the following subdirectories, assuming the project name (and top-level directory) is named pwabinit::


is could be done in the following way, supposing the project is named p for native python, switchable component factor functesting, c extensions, c-python binding code, 

applications
^^^^^^^^^^^^
Pyre applications typically are put in this directory with a :ref:`Make.mm <make-mm>`_ that exports them to the pythia-0.8/bin directory.  :ref:`Pyre convention <pyre-style>`_ appends a "d" to the app name if it is a service.

etc
^^^
* carries odb files for switching facilities




Much of this structure can be generated automatically by using the package utility.  However, appli

.. _pyre-inventory-implementation:

Inventory, Trait, and Notary
----------------------------

Inventory has descriptors as its static members. 
Descriptors are special python objects that defines __get__ (and __set__) methods. 
(Note: they are not instances of pyre.inventory.Descriptor.Descriptor. 
class pyre.inventory.Descriptor.Descriptor is not really a Descriptor class meant by
http://users.rcn.com/python/download/Descriptor.htm. 
In pyre, pyre.inventory.Trait.Trait is the real Descriptor class.) 
An instance of descriptor describe a property of his parent, but does not hold the
value of this property. 
This is why you can inherit Inventory but its static members do not conflict in 
different instances of Inventory classes.

For example ::

  class Inventory(Component.Inventory):
  
      import pyre
  
      a = pyre.inventory.str('a', default="" )

Here pyre.inventory.str makes a Str instance. Str is a subclass of Trait. 
So the instance Inventory.a is a descriptor that says the instance of 
Inventory class will have a property called a. 
This property is a string, and it defaults to be empty.

When Inventory class is instantiated, ::

  inventory = Inventory(...)

and when we are asking for its property, ::

  inventory.a

The __set__ and __get__ functions of Trait class will get called and which, 
in turn, calls getTraitValue and setTraitValue of the Inventory class. 

So you can see the class Trait and Inventory have to cooperate to
implement this idea of Descriptor.

Notary
^^^^^^
Inventory has its metaclass pyre.inventory.Notary.Notary. 
The metaclass's __init__ will be called when the object of the class 
(Note: the class object != the class instance) is built. 
In Notary's __init__, all traits of an Inventory class will be 
collected to two registries, one for properties, and one for facilities.


Listing of Pyre Reserved Methods 
--------------------------------




