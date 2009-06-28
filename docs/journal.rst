Debugging pyre applications
===========================

.. _journal:

Journal
-------

For those used to debugging daemons such as log4j or inserting print statements, journal is the debugging tool for you.  It is also a good model of a pyre application as discussed in :ref:`the section on advanced pyre <journal-structure>`.  Because journal is a daemon, it produces debugging info for all application types, whether distributed or local.

To start using journal, first execute the journal daemon by typing::

    $ journald.py	

from the command line.  Then insert the following at the top of your pyre app::

    import journal
    journal.info(name).activate()

As the need arises, insert debugging statements in your code.  


.. _debugger:

Debugging pyre apps with a debugger such as in eclipse
------------------------------------------------------

Many powerful debuggers exist which allow one to step through even distributed applications one line at a time, set breakpoints, and watch the values of program variables change over time.  For those coding in eclipse, one can configure a large variety of runs by simply inputing all the command line variables in a given run configuration, and then storing these configurations to.

Another option is to either store a number of pml files and switching 
