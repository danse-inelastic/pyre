.. _advancedInstall:

Installing from source
======================

Before installing pyre from source, one must install its build system, popularly called "Make.mm" because it is triggered by the "mm" comand.  It is essentially a set of macros and add-ons to normal make.  Typing 'mm' activates a file called Make.mm in each directory.  This configuration file can be used to compile and install pyre apps, odb files, components, and c extensions.

.. _make-mm:

Installing Make.mm
^^^^^^^^^^^^^^^^^^

Installing :ref:`Make.mm<moreMakemm>` and configuring environment variables useful to pythia-0.8 can be done with the following steps.  Although we assume linux environment and bash shell, scripts containing the following commands can be found in these example scripts for linux (:download:`bash <bash_tools.linux>` and :download:`csh <csh_tools.linux>`) and mac (:download:`bash <bash_tools.mac>` and :download:`csh <csh_tools.mac>`).  Normally one will want to source this script as part of a shell startup routine such as .bashrc.

Pythia-0.8
""""""""""

First, choose an installation directory, which we call DV_DIR.  Export it as environment variable::

  $ export DV_DIR=<your choice here>         

Next create a "tools" directory which will hold the compiled pythia distribution::

  $ export TOOLS_DIR=${DV_DIR}/tools      

then include and lib directories for c extensions::
 
  $ export TOOLS_INCDIR=$TOOLS_DIR/include
  $ export TOOLS_LIBDIR=$TOOLS_DIR/lib

now add "tools" to your path::

  if [ "$PATH" = "" ]
  then
    export PATH=${TOOLS_DIR}/bin
  else
    export PATH=${TOOLS_DIR}/bin:${PATH}
  fi
  if [ "$LD_LIBRARY_PATH" = "" ]
  then
    export LD_LIBRARY_PATH=${TOOLS_DIR}/lib
  else
    export LD_LIBRARY_PATH=${TOOLS_DIR}/lib:${LD_LIBRARY_PATH}
  fi
  if [ "$MANPATH" = "" ]
  then
    export MANPATH=${TOOLS_DIR}/man
  else
    export MANPATH=${TOOLS_DIR}/man:${MANPATH}
  fi

and create a config directory which contains Make.mm and its system of macros::

  $ export BLD_CONFIG=${DV_DIR}/config     # location of build procedure files

and create a build directory containing the compiled versions of pythia::

  $ export BLD_ROOT=${DV_DIR}/builds       # root directory of builds
  $ export TARGET=shared,opt,debug         # build target options

also create a templates directory for pyre utilities::

  $ export TEMPLATES_DIR=${DV_DIR}/templates

next initialize some useful environment variables::

  $ export PYTHIA_VERSION=0.8
  $ export PYTHIA_DIR=${DV_DIR}/tools/pythia-${PYTHIA_VERSION}
  $ export EXPORT_ROOT=${TOOLS_DIR}/pythia-${PYTHIA_VERSION}

and add the config and build directories to your path::

  $ export PATH=${BLD_CONFIG}/make:${PATH}
  $ export PATH=${PATH}:${EXPORT_ROOT}/bin
  $ export LD_LIBRARY_PATH=${EXPORT_ROOT}/lib:${LD_LIBRARY_PATH}

set some general environment variables::

  $ export PYTHON_VERSION=2.5
  $ export PYTHON_DIR=/usr
  $ export PYTHON_LIBDIR=${PYTHON_DIR}/lib/python${PYTHON_VERSION}
  $ export PYTHON_INCDIR=${PYTHON_DIR}/include/python${PYTHON_VERSION}

and add the python modules to the python path::

  $ if [ "$PYTHONPATH" = "" ]
  $ then
      export PYTHONPATH=$EXPORT_ROOT/packages
  $ else
      export PYTHONPATH=${PYTHONPATH}:${EXPORT_ROOT}/packages
  $ fi


MPI/mpich support
"""""""""""""""""

Here is an example of how to include mpi support (uncomment as needed)::

  # export MPI_VERSION=1.2.5
  # export MPI_DIR=/usr/local/mpich            # MPI installation directory
  # export MPI_DIR=${TOOLS_DIR}/mpich-${MPI_VERSION}
  # export MPI_INCDIR=$MPI_DIR/include
  # export MPI_LIBDIR=$MPI_DIR/lib

  # Add MPI to PATH variables if installed in non-standard location.
  # export PATH=$MPI_DIR/bin:$PATH
  # export LD_LIBRARY_PATH=$MPI_DIR/lib:$LD_LIBRARY_PATH
  # export MANPATH=$MPI_DIR/man:$MANPATH


Optional compilers 
""""""""""""""""""

Here are examples of how to add other compilers for use in pyre (uncomment as needed)::

  # export GNU_MAKE=make

  # Absoft Pro FORTRAN compiler
  # export TARGET_F77=Absoft-2.1
  # export ABSOFT=$TOOLS_DIR/ProFortran-7.0  # Absoft installation directory
  # export ABSOFT_DIR=$ABSOFT
  # export ABSOFT_LIBDIR=$ABSOFT/lib
  # export PATH=$ABSOFT/bin:$PATH

  # Portland Group compilers
  # export TARGET_F77=PGI-3.0
  # export TARGET_CC=PGI-3.0
  # export TARGET_CXX=PGI-3.0
  # export PGI_DIR=/usr/pgi                  # PGI installation directory
  # export PGI_LIBDIR=$PGI_DIR/linux86/lib_rh6
  # export LM_LICENSE_FILE=$PGI_DIR/license.dat
  # export PATH=$PGI_DIR/linux86/bin:$PATH
  # export MANPATH=$PGI_DIR/man:$MANPATH

  # KAI C++ Compiler
  # export TARGET_CXX=KAI-4.0
  # export KAI_DIR=/usr/local/KAI            # KCC installation directory
  # export PATH=$KAI_DIR/bin:$PATH

  # GCC 3.x Compiler
  export TARGET_F77=gcc
  # export TARGET_F77=gcc-3.0
  # export TARGET_CC=gcc-3.0
  # export TARGET_CXX=gcc-3.0
  # export GCC_DIR=/usr/local/gnu            # GCC installation directory
  # export PATH=$GCC_DIR/bin:$PATH
  # export LD_LIBRARY_PATH=$GCC_DIR/lib:$LD_LIBRARY_PATH


Setup config and templates
""""""""""""""""""""""""""

Once the above environment variables have been set, download and build config/ and the templates/ with the following steps::

   1. create development directory
          * $ mkdir -p $DV_DIR 
   2. create tools directory
          * $ mkdir -p $TOOLS_DIR 
   3. create builds directory
          * $ mkdir -p $BLD_ROOT 
   4. change to development directory
          * $ cd $DV_DIR 
   5. use anonymous cvs to get config and the templates
          * $ cvs -d :pserver:config@cvs.cacr.caltech.edu:/config login
            [password: config]
          * $ cvs -d :pserver:config@cvs.cacr.caltech.edu:/config co config
          * $ cvs -d :pserver:pyre@cvs.cacr.caltech.edu:/pyre login
            [password: pyre]
          * $ cvs -d :pserver:pyre@cvs.cacr.caltech.edu:/pyre co templates 
   6. change to templates directory
          * $ cd $TEMPLATES_DIR 
   7. build templates
          * $ mm 

$DV_DIR should now have the following structure::

  builds/  config/  templates/  tools/


Testing your installation
"""""""""""""""""""""""""

To test the templates installation::

   1. change to home directory
          * $ cd 
   2. build a template pyre application
          * $ app.py
          * creating application 'Simple' in 'simple.py'

Now that the build system is installed, let's install pyre. 

Installing pyre
^^^^^^^^^^^^^^^

Pyre source including c extensions is available from various svn repositories.  Let's use the DANSE repo.

Checking out the DANSE repo:
""""""""""""""""""""""""""""

Developers participating in Distributed Analysis of Neutron Scattering Experiments (DANSE) should use the "patches-from-jiao" branch which can be checked out from the danse.us/pyre repository.  For example, assuming read-only access::

  $ svn co svn://svn@danse.us/pyre/branches/patches-from-jiao

Read and write access can be obtained by joining the DANSE project and by filling out a `CACR Account request form <http://www.cacr.caltech.edu/main/?page_id=89>`_ for the DANSE project.   

Now go to the base directory of pyre::

  $ cd patches-from-jiao
  $ mm

and type 'mm'.  To test the installation, change to the pyre tests directory::

  $ cd $PYTHIA_DIR/packages/pyre/tests/applications 
  $ python hello.py --name=NewPyreUser
  Good morning NewPyreUser!

and run the hello.py test.  If you have installed the pure python version of pyre from egg or zip previously, uninstall it before trying these tests.


Installing other pythia-0.8 packages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Any package that depends on pyre probably also uses Make.mm as it's build system.  To install it, one may follow the same procedure as above and type 'mm' in the top level directory.

