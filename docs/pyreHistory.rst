Pyre history
============

Historically, pyre was created to bring a degree of order to the complex task of staging large parallel scientific simulations. Applications support a command-line, serial execution model. This has been extended to command-line parallel execution. Most of the procedures for creating serial applications are the same for parallel applications, so learning about serial apps is a good way to get started. 

Pyre 1.0 is being actively developed currently and will soon be ready for general usage.  Upcoming changes include a more seamless inventory, better db support, and many new additions for creating and staging web applications.


Discussion of Pyre improvements
=======================================

Pyre is not perfect and is undergoing continued development.  Here are a few issues currently being worked on:

Pyre
----

* code bloat
  - use annotations as much as possible rather than subclassing, factory functions, etc.
* need online services with good lifecycle management and message-passing capabilities...see OSGI and ServiceMix 4.0 for examples


Opal
----

* actors are too big--need to break it up more
* not enough design capabilities
