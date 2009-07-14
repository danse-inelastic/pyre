.. _installation:

Installation
=================

Pyre is the base package in a larger group of software packages based upon it and collectively called pythia-0.8.  However, we frequently use the word pyre to represent pythia as well, especially when discussing installation.  Pythia can either be installed as a python-only set of modules or a group of python modules with some c extensions.  Howev

.. _pure-python-distrib:

Pure python distribution
-------------------------

Pure python version of pyre is a good starting point to try out pyre, and for most python applications, is adequate.

From an egg
^^^^^^^^^^^

Assuming you have the `easy install <http://peak.telecommunity.com/DevCenter/EasyInstall>`_   package already on your system::

  $ easy_install -f http://dev.danse.us/packages pythia


From a zip file
^^^^^^^^^^^^^^^

First, download the `zip file <http://www.cacr.caltech.edu/projects/danse/pyre/pythia-0.8-patches.zip>`_. Second, add the zipfile to your $PYTHONPATH. For example, if you are using bash::

  $ export PYTHONPATH=/path/to/downloadedzip:$PYTHONPATH



Python/C distribution
---------------------

A complete installation can be done through svn.  Currently, there are various branches of pyre.  


Checking out the DANSE branch:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Developers participating in Distributed Analysis of Neutron Scattering Experiments (DANSE) should use the "patches-from-jiao" branch which can be checked out from the danse.us/pyre repository.  For example, assuming read-only access::

  $ svn co svn://svn@danse.us/pyre/branches/patches-from-jiao

Read and write access can be done by joining the DANSE project by filling out a `CACR Account request form <http://www.cacr.caltech.edu/main/?page_id=89>`_ for the DANSE project.  Eventually this branch will be merged with the trunk toward the end of the project.


Installing pyre
^^^^^^^^^^^^^^^

To install pyre, one must first install :ref:`make-mm`.  After installing it, one can simply go to the base directory of pyre::

  $ cd patches-from-jiao
  $ mm

and type 'mm'.


Installing other pythia-0.8 packages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Assuming pyre is also installed, one may follow the same procedure as above and type 'mm' in the top level directory.
