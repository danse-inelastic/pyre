Build systems
=============

Make.mm
-------

The build system used by pyre uses the "mm" comand, which activates a file called Make.mm in each directory.  This configuration file can be used to move pyre apps, odb files, components, and c extensions to their appropriate directories in pythia-0.8.

* more about various directives/options/macros that can be used

* discussion about config


Scons
-----

There is some desire to introduce a more pythonic build system into pyre by using scons instead of Make.mm.  This has already been done for gnu autoconf, for example, in other pyre projects.
