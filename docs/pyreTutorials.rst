.. _pyre-tutorials:

Tutorials
==========

Hello World
--------------------
This is the pyre version of hello world. It introduces some structures into the simple one-liner ::

    print "Hello World!"


In this tutorial we will build the pyre application step-by-step
by gradually adding structure to this simple application,
and explain the reasons why those structures are needed.


.. _helloworld1:

The simplest pyre application
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Please open your favorite editor and type in the following::

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

Here are a few things needs attention:

 * A pyre application needs to be inherited from pyre.applications.Script.Script
   class.
 * The new application class needs a method "main". This method will be executed   when the application is launched.
 * The application's constructor has a keyword argument "name", and this name 
   is the key that the pyre framework will use to find the application's
   configuration items.

You may wonder why we need to create this pyre application instead of
just simply using the python one-liner to achieve the same effect::

  >>> print "Hello World!"

In the next step we will make this application a little bit more configurable
and interesting.


Say Hello to Someone
^^^^^^^^^^^^^^^^^^^^
Please create a new python file "hello2.py" and type in the following code::

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

Compare this example to :ref:`the previous example <helloworld1>`, a few things 
are added or modified

  * An Inventory class
  * The _configure method
  * The main method
  * The constructor 


Inventory
""""""""""
In the inventory, the public cofigurable items are presented.
In this simple pyre application, the inventory has one item,
"name", which is the name of the one who we would like to say
hello::

  name = pyre.inventory.str(name='name', default='World')

This statement declares that there is a public property for
this application, and its type is a string, its name is "name",
and its default value is "World".
Pyre framework will keep this declaration in mind, and look
for user inputs for this property when this application is
launched, and parse user inputs to appropriate data type,
and feed the value to::

  self.inventory.name

where self is the application.


_configure
""""""""""
In the _configure method, we pass create a variable of this
hello2 application, and pass it the value of the property
"name", which is handed out by the pyre framework::

  self.name = self.inventory.name


main
""""

In the main method, we change the print message so that we
will say hello to the person defined by the variable "name"::

  print "Hello "+self.name+"!"
 

constructor __init__
""""""""""""""""""""""""""""""

In the constructor, we gives this application a name "hello2".
This name is a identifier that pyre framework will use to
look for configurations.  For example, we can use pml files
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

The pyre framework looks for pml files by looking for the
names of the pyre components (pyre application is also a pyre component),
and it found "hello2.pml", and the configurations in this
file is used.

If you change the name of the pml file, for example, to hello2a.pml,
you will end up with ::

  $ python hello2.py
  Hello World!

because the pyre framework cannot recognize your pml file as the one
to configure hello2.py.


