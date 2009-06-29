Debugging pyre applications
===========================

.. _journal:

Journal
-------

Pyre's native debugger is called journal
(that, for java developers, is kind of similar to log4j).
It allows developers to insert into their codes journalling instructions that produce
pyre application diagnostics such as
error reporting, warnings, and debugging.

Here is the cheat sheet of creating a journal channel and writing to it::

  >>> import journal
  >>> debug = journal.debug('myproject')
  >>> debug.activate()
  >>> debug.log( 'This is a debugging message' )

and this would be the output::

   >> <stdin>:1:<module>
   >> myproject(debug)
   -- This is a debugging message
  <journal.diagnostics.Diagnostic.Diagnostic object at 0x956910>

The factory ::

  journal.debug

creates journal channels of "debug" type. And this call ::

  journal.debug("myproject")

creates a journal debug channel named "myproject".
The call ::

  >>> debug.activate()

activates this journal channel.
And now you are ready to output to the newly created journal stream::

  >>> debug.log( 'This is a debugging message' )


Journal types
^^^^^^^^^^^^^
Following types are available
 * debug: debugging information. Default off.
 * error: unrecoverable runtime error. Default on.
 * firewall: fatal programming error. Default on.
 * info: descriptive information. Default off.
 * warning: recoverable runtime error. Default off.


Journal devices
^^^^^^^^^^^^^^^

Journals can be easily directed to different devices. By default, journal
writes to a terminal-like device that directly outputs to screen.
Another very useful device is actualy a journal daemon.


Journal daemon
""""""""""""""
It is also a good model of a pyre application as discussed in :ref:`a section on advanced pyre <journal-structure>`.  Because journal is a daemon, it produces debugging info for all application types, whether distributed or local.

To start using journal daemon, first execute the journal daemon by typing::

    $ journald.py	

from the command line.  (also talk about having the right pml files set up and making sure journal is "pointing" to them).  Then insert the following at the top of your pyre app::

    import journal
    journal.info(name).activate()
    journal.debug("journal").activate()

Then in the constructor, information about the code part may be labeled in order to discern which, of the many parts of your code, is outputting the information:

    i = journal.info(codepart)
    d = journal.debug(codepart)

and as the need arises, insert debugging statements in your code::

    i.log(something-you'd-like-to-see)
    d.log(something-you'd-like-to-see)


Journaling for pyre components
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Journaling channels are automatically set up for all pyre components.
In Configurable.py, a superclass of Component.py::

    def __init__(self, name):
	...
        self._info = journal.info(name)
        self._debug = journal.debug(name)

so that if one desires to debug pyre components or pyre scripts, one only has to call::

    self._debug.log(something-you'd-like-to-see)



.. _debugger:

Debuggers
---------

In addition to journal, and especially for routine debugging of individual components, native ide debuggers (such as in Eclipse) may be used.  Pyre is particularly amenable to this type of testing since all parameters may be input via the commandline, which in Eclipse maybe be set, stored, and exported as run/debug configuration files.

Alternatively, one may store the run configurations themselves as pml files.
