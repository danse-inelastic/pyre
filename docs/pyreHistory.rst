Pyre history
============

Historically, pyre was created to bring a degree of order to the complex task of staging large parallel scientific simulations. Applications support a command-line, serial execution model. This has been extended to command-line parallel execution. Most of the procedures for creating serial applications are the same for parallel applications, so learning about serial apps is a good way to get started. 

Pyre 1.0 is being actively developed and will soon be ready for general use.  Upcoming changes include a more seamless inventory, better db support, and many new additions for creating and staging web applications.


..	Discussion of pyre improvements
	===============================
	
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
	
	.. _scons:
	
	Scons
	-----
	
	There is some desire to introduce a more pythonic build system into pyre by using scons instead of Make.mm.  Inserting more than one build system (alongside Make.mm) has already been done for gnu autoconf, for example, in other pyre projects.  Advantages would be: (1) removal of the need to edit Make.mm every time a new file is added in the :ref:`directory structure <pyre-directory-structure>` (2) less of a learning curve for new pyre developers since scons is more widely known,...
