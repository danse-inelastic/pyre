.. _pyre-tutorials:


Tutorials
===========

If you have not done so, please 
:ref:`install <installation>`
pythia-0.8 before you start playing with the following examples.


Hello World
-----------
This is the pyre version of hello world. It introduces some structures into the simple one-liner ::

    print "Hello World!"


In this tutorial we will build the pyre application step-by-step
by gradually adding structure to this simple application,
and explain the reasons why those structures are needed.


.. _helloworld1:

The simplest pyre application
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Please open your favorite editor and type in the following (or download it: `hello1.py <tutorials/hello1.py>`_)::

  #!/usr/bin/env python

  from pyre.applications.Script import Script as base

  class HelloApp(base):

      def main(self):
	  print "Hello World!"
	  return

      def __init__(self, name='hello1'):
	  super(HelloApp, self).__init__(name=name)
	  return

  # main
  if __name__ == "__main__":
      app = HelloApp()
      app.run()

  # End of file


Please save it as hello1.py and run it ::

  $ python hello1.py
  Hello World!

Here are a few things to note:

 * A pyre application needs to inherit from pyre.applications.Script.Script.
 * It needs a method named "main". This method will be executed when the application is launched.
 * The application's constructor has a keyword argument "name", and this name 
   is the key the pyre framework will use to find the application's
   configuration items.

You may wonder why we need this larger pyre application instead of
just using the python one-liner to achieve the same effect::

  >>> print "Hello World!"

This will become apparent in the next few sections.  The next step is to make this application a little more configurable
and interesting.


Say Hello to Someone
^^^^^^^^^^^^^^^^^^^^
Please create a new python file "hello2.py" and type in the following code 
(or download it: `hello2.py <tutorials/hello2.py>`_)::

  #!/usr/bin/env python

  from pyre.applications.Script import Script as base

  class HelloApp(base):

      class Inventory(base.Inventory):

	  import pyre.inventory

	  name = pyre.inventory.str(name='name', default='World')


      def main(self):
	  print "Hello " + self.name + "!"
	  return


      def _configure(self):
	  super(HelloApp, self)._configure()
	  self.name = self.inventory.name
	  return


      def __init__(self, name='hello2'):
	  super(HelloApp, self).__init__(name=name)
	  return


  # main
  if __name__ == "__main__":
      app = HelloApp()
      app.run()

  # End of file

To try it out, please type in the following command::

  $ python hello2.py
  Hello World!

And you can change the person you want to say hello::

  $ python hello2.py --name=Bob
  Hello Bob!

Comparing this to :ref:`the previous example <helloworld1>`, we note a few things 
are added or modified:


Inventory
""""""""""
There is an inner class called Inventory, where publicly cofigurable items are listed.
In the simple application above, Inventory has one item,
"name", which is the name of the one whom we would like to say
hello::

  name = pyre.inventory.str(name='name', default='World')

This statement declares there is a public property for
this application, its type is a string, its name is "name",
and its default value is "World".
Pyre instantiates Inventory with the lower case name "inventory", looks
for user inputs for its properties when the application is
launched, parses user inputs to appropriate data types,
and feeds the value to::

  self.inventory.name

where self is the application.


_configure
""""""""""
In the _configure method, we create a local variable and pass it the value of the property
"name", which is managed by the pyre framework::

  self.name = self.inventory.name


main
""""
In the main method, we change the print message so that we
will say hello to the person defined by the variable "name"::

  print "Hello "+self.name+"!"
 

.. brandon: need a better introduction to pml files here...and utilities like invenetory.py
constructor __init__
""""""""""""""""""""""""""""""
In the constructor, we give this application the name "hello2".
This name is a identifier that pyre framework will use to
look for configurations.  


Although it is useful to have a system to manage commandline inputs, both to an application and to its subapplications, called "components" in pyre, wouldn't it be useful to have alternative ways to configure a program? Pyre has this in the form of xml files, which are given the .pml ending.  Pml files are created by...(outline structure of pml file), discuss utitlies, 
For example, we can use pml files
to configure pyre applications.  Let us create a pml file by::

  $ inventory.py --name=hello2
  creating inventory template in 'hello2.pml'

Now we edit the hello2.pml to look like ::

  <!DOCTYPE inventory>

  <inventory>

    <component name='hello2'>
      <property name='name'>Alice</property>
    </component>

  </inventory>

With this file in your current directory, you will see something
different::

  $ python hello2.py
  Hello Alice!

Pyre looks for pml files by looking for the
names of the pyre components (pyre application is also a pyre component),
and it found "hello2.pml", and the configurations in this
file is used.

If you change the name of the pml file, for example, to hello2a.pml,
you will end up with ::

  $ python hello2.py
  Hello World!

because pyre framework cannot recognize your pml file as the one
to configure hello2.py.


.. _helloworld-greet.py:

Say Some Greetings to Someone
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
In this example we need two python modules (you can download them: 
`greet.py <tutorials/greet.py>`_ ,
`Greeter.py <tutorials/Greeter.py>`_ 
). The first one is the
pyre application "greet.py"::

  #!/usr/bin/env python

  from pyre.applications.Script import Script as base

  class GreetApp(base):

      class Inventory(base.Inventory):

	  import pyre.inventory

	  from Greeter import Greeter
	  greeter = pyre.inventory.facility(name='greeter', factory=Greeter)
	  name = pyre.inventory.str(name='name', default='World')


      def main(self):
	  self.greeter.greet(self.name)
	  return


      def _configure(self):
	  super(GreetApp, self)._configure()
	  self.name = self.inventory.name
	  self.greeter = self.inventory.greeter
	  return


      def __init__(self, name='greet'):
	  super(GreetApp, self).__init__(name=name)
	  return


  # main
  if __name__ == "__main__":
      app = GreetApp()
      app.run()

  # End of file

and the second one is a pyre component "Greeter.py"::

  # -*- Python -*-

  from pyre.components.Component import Component


  class Greeter(Component):


      class Inventory(Component.Inventory):

	  import pyre.inventory

	  greetings = pyre.inventory.str('greetings', default='Hello')


      def greet(self, name):
	  print self.greetings + ' ' + name + '!'
	  return


      def __init__(self, name='greeter'):
	  Component.__init__(self, name, facility='greeter')
	  return


      def _configure(self):
	  super(Greeter, self)._configure()
	  self.greetings = self.inventory.greetings
	  return


  # End of file 

Let us try it out. 

Default configuration::
   
   $ python greet.py
   Hello World!

Hello Bob!::

  $ python greet.py --name=Bob
  Hello Bob!

Hi Bob!::

  $ python greet.py --name=Bob --greeter.greetings=Hi
  Hi Bob!

You see we can now not only configure the target of the greetings,
but also the content of the greetings.

Facility
""""""""
In this example, an important concept is introduced: "facility".
Facility is a way that a component can declare that he needs 
another component to perform some work for him.
This is a very useful feature of pyre, which enables developers
to construct pyre applications in layers, and keep each component
small, dedicated and manageable.

This "greet" pyre application now delegates its functionality to
the pyre component "greeter". The pyre application itself just
simply calls the greeter to do the real work. 
It may look unecessary at the first glance, but you will see
the benefit of this delegation even for this simple demo application
a bit later in this tutorial. Here, let us first see how we declare
that a component needs another component::

  greeter = pyre.inventory.facility(name='greeter', factory=Greeter)

The greeter is declared as a facility in the inventory of the pyre
application "greet", which means the app "greet" needs a component
"greeter" to work correctly. The "name" keyword in this declaration
tells pyre framework that it needs to look for the name "greeter"
in order to configure this facility. The "factory" keyword tells
pyre framework that it can use the assigned factory method
to create a pyre component and use that component as the default
component for this greeter facility.

Now let us take a look at the Greeter component. The Greeter component
is constructed in a way quite similar to the way we construct the
pyre applications hello1.py, hello2.py, and greet.py. 
We inherit from class pyre.components.Component.Component to 
create a new component class, then we add public settable 
property "greetings" to its inventory, and touch the "_configure"
method and the constructor "__init__" a little bit to fit this component. 

One extra thing worth mentioning is that we create a method
"greet" for this component, which takes an argument "name"
which is the target of greetings. This method
is called by the pyre app "greet" in its method "main".

In the example ::

  $ python greet.py --name=Bob --greeter.greetings=Hi
  Hi Bob!

we notice something interesting::

  --greeter.greetings=Hi

The string "greeter" denotes the "greeter" component,
and the string "greeter.greetings" deontes the property
"greetings" of the component "greeter".

Easy to plug in a different component for a facility
""""""""""""""""""""""""""""""""""""""""""""""""""""
Now we create another pyre component to show the benefit
of using pyre facility. Please create file
`fancy-greeter.odb <tutorials/fancy-greeter.odb>`_
with the following content::

  # -*- Python -*-

  from pyre.components.Component import Component


  class Greeter(Component):


      class Inventory(Component.Inventory):

	  import pyre.inventory

	  decoration = pyre.inventory.str('decoration', default='*')
	  greetings = pyre.inventory.str('greetings', default='Hello')


      def greet(self, name):
	  s = self.greetings + ' ' + name + '!'
	  s = ' '.join([self.decoration, s, self.decoration])

	  print self.decoration*(len(s))
	  print s
	  print self.decoration*(len(s))
	  return


      def __init__(self, name='fancy-greeter'):
	  Component.__init__(self, name, facility='greeter')
	  return


      def _configure(self):
	  super(Greeter, self)._configure()
	  self.greetings = self.inventory.greetings
	  self.decoration = self.inventory.decoration
	  return


  def greeter(): return Greeter()

  # End of file 


Try the following command::

  $ python greet.py --name=Bob --greeter.greetings=Hi --greeter=fancy-greeter
  ***********
  * Hi Bob! *
  ***********

The extra command line option ::

  --greeter=fancy-greeter

tells pyre to use the component named "fancy-greeter" instead
of the default component for the facility "greeter". 
Pyre then looks for this "fancy-greeter" component
by looking for "fancy-greeter.odb" in a few directories 
(~/.pyre and current directory). 
The fancy-greeter.odb file must have a method "greeter", which
is the name of the facility this component will be plugged into.
The method "greeter" returns a pyre component, which will 
be harnessed by pyre framework and used as the "greeter" component
for the "greet" pyre application.

Apparently this feature is very useful since you can switch the computation
engine easily with pyre applications. For example, if you have
an application that does parametric fitting and this application makes use
of a optimizer, you can declare an "optimizer" facility and use pyre's internal component-handling machinery to tell the application to switch optimizers from the command line.

