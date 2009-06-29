Debugging pyre applications
===========================

.. _journal:

Journal
-------

Pyre's native debugger is called journal and is a daemon similar to log4j.  It is also a good model of a pyre application as discussed in :ref:`a section on advanced pyre <journal-structure>`.  Because journal is a daemon, it produces debugging info for all application types, whether distributed or local.

To start using journal, first execute the journal daemon by typing::

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

This is done intrinsically for all components in Configurable.py, a superclass of Component.py::

    def __init__(self, name):
	...
        self._info = journal.info(name)
        self._debug = journal.debug(name)

so that if one desires to debug components or scripts, one only has to call::

    self._debug.log(something-you'd-like-to-see)

(ps: describe difference between info and debug)


.. _debugger:

Debugging pyre apps with a debugger such as in eclipse
------------------------------------------------------

In addition to journal, and especially for routine debugging of individual components, native ide debuggers (such as in Eclipse) maybe used.  Pyre is particularly amenable to this type of testing since all parameters may be input via the commandline, which in eclipse maybe be set, stored, and exported as a wide variety of run/debug configuration files.

Alternatively, one may store the run configurations themselves as pml files.
