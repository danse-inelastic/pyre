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

