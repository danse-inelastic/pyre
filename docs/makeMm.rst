Build systems
=============


.. _make-mm:

Make.mm
-------

The build system used by pyre uses the "mm" comand, which activates a file called Make.mm in each directory.  This configuration file can be used to move pyre apps, odb files, components, and c extensions to their appropriate directories in pythia-0.8.


Installing Make.mm
^^^^^^^^^^^^^^^^^^

Installing Make.mm and configuring environment variables useful to pythia-0.8 can be done with the following steps.  Although we assume linux environment and bash shell, scripts for mac and other shells can be found at the end of this section.

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
  $ export TEMPLATES_DIR=${DV_DIR}/templates

next initialize some useful environment variables::

  $ export PYTHIA_VERSION=0.8
  $ export PYTHIA_DIR=${DV_DIR}/pythia-${PYTHIA_VERSION}
  $ export EXPORT_ROOT=${TOOLS_DIR}/pythia-${PYTHIA_VERSION}

and add build procedure to your path
  export PATH=${BLD_CONFIG}/make:${PATH}
  export PATH=${PATH}:${EXPORT_ROOT}/bin
  export LD_LIBRARY_PATH=${EXPORT_ROOT}/lib:${LD_LIBRARY_PATH}

set some general environment variables::

  export PYTHON_VERSION=2.4
  export PYTHON_DIR=/usr/local
# export PYTHON_DIR=$TOOLS_DIR/python-2.3.4  # Python installation directory
  export PYTHON_LIBDIR=${PYTHON_DIR}/lib/python${PYTHON_VERSION}
  export PYTHON_INCDIR=${PYTHON_DIR}/include/python${PYTHON_VERSION}

# Add Python to PATH variables
  export PATH=$PYTHON_DIR/bin:$PATH
  if [ "$PYTHONPATH" = "" ]
  then
    export PYTHONPATH=$EXPORT_ROOT/modules
  else
    export PYTHONPATH=${PYTHONPATH}:${EXPORT_ROOT}/modules
  fi
  export PYTHONSTARTUP=${HOME}/.python


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

Here is an example of how(uncomment as needed)
#
  export GNU_MAKE=make

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

These commands are all found in the following example scripts for linux (`bash <bash_tools.linux>` and `csh <csh_tools.linux>`) and mac (`bash <bash_tools.mac>` and `csh <csh_tools.mac>`).


Directives/options/macros used in Make.mm:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Make.mm format is similar to that of typical linux shell scripting.  A few macros which may be useful are:

 * export-python-package 

 * 


Internals of pyre config
^^^^^^^^^^^^^^^^^^^^^^^^

Maybe Michael Aivazis or Jiao can write this section.


.. _scons:

Scons
-----

There is some desire to introduce a more pythonic build system into pyre by using scons instead of Make.mm.  Inserting more than one build system (alongside Make.mm) has has already been done for gnu autoconf, for example, in other pyre projects.  Advantages would be: (1) removal of the need to edit Make.mm every time a new file is added in the :ref:`directory structure <pyre-directory-structure>` (2) less of a learning curve for new pyre developers since scons is more widely known,...
