Advanced topics
===============

.. _moreMakemm:

More about the Make.mm build system
-----------------------------------

Introduction
^^^^^^^^^^^^

We now describe the structure and usage of the build procedure that compiles and links pyre projects and other packages that they depend on. The build procedure is designed to make our codes easily portable to a very wide variety of compiler and platform targets. Furthermore, it allows for customization of the compilation process at several different levels.

The core of the build procedure is embodied in the shell script mm. Code packages are built and installed by invoking this script, which automatically determines the host target, locates the appropriate compiler commands and options for this target platform, and issues the necessary commands to build the code packages. The mm script relies on a layered set of definition files that customize behavior and recursive processing of makefiles that describe a package and any subpackages it may contain.
The mm Script

The mm script is meant to be used in a manner similar to the standard make tool. mm is invoked in the following way::

    mm [-f <makefile>] [target]

The -f option allows a code package to use makefiles with a different name other than the default name, which is Make.mm. If any target is specified, then mm will build that target rather than the default target given by the makefiles.

Before we can properly use the mm script, we must set three environment variables::

    * BLD_ROOT --- path of the root of the build tree
    * EXPORT_ROOT --- path of the root of the products tree
    * TARGET --- comma-delineated list of desired compilation options 

The source code for any package to be built using the build procedure is typically stored in a directory below the common root BLD_ROOT. (The files for the build system itself are also assumed to be located beneath this common root directory in $BLD_ROOT/config, although this can be overridden by setting the environment variable BLD_CONFIG to a different path.) Product libraries and binaries are built in subdirectories lib and bin beneath $BLD_ROOT. Once a code package has been built, we can use the make target export to install it in a directory below EXPORT_ROOT. The contents of TARGET indicate any special compile options. (These targets are not to be confused with the make targets, which are defined within the makefiles of a code package in the standard way.) The current valid target options for mm are::

    * debug --- compile with debugging on
    * opt --- compile with optimization on
    * insure --- instrument code with Insure++ code checking tool
    * purify --- link with Purify memory analysis libraries
    * prof --- generate extra code to write profiling information
    * mpi --- include MPI header and library files 

When mm is invoked, it will first check for the existence of the directories indicated by BLD_ROOT and EXPORT_ROOT. Next, it uses the uname utility to determine the operating system and machine type. This information is later used to select a platform-specific definitions file, which indicates what compilers and standard options to use. Once this is done, mm parses the contents of TARGET and looks for corresponding target-specific definitions files. These files contain the special flags and definitions that are needed for these compilation options. In addition, a target tag is constructed by combining the name of the target platform with any user-specified targets, and this tag is later used to create target-specific subdirectories where the code package will be built. This allows the build system to simultaneously maintain builds of a code package for many different potential targets. The final setup step is to get the user's name and check for any user-specific file of definitions which may override the standard settings and behaviors.

With all of these preliminaries completed, the actual work of processing the make command begins. mm checks for the -f option and changes the name of the code package makefile it will look for if requested. If the environment variable LOGTAGS is set, mm will echo the makefile name and the selected platform and user targets. Finally, mm invokes make on the makefile std-make.def and passes along the target (if any) from the mm command line. The special makefile std-make.def coordinates the inclusion of all the various platform-specific, compiler-specific, target-specific and user-specific definitions files that set options for the build system.

Definitions Files
^^^^^^^^^^^^^^^^^

The build system contains several sets of definitions files with a .def extension. These files set the values of various macros that control the behavior of the build system. std-make.def, located in directory $BLD_CONFIG/make, is the primary file which includes all the other definitions files. It first includes several other files from the same directory that provide some default settings. These files set up things such as the standard names for certain Unix tools and standard filename extensions. They also initialize with no value many compiler- and project-specific macros that may be overridden in other definitions files. After this, std-make.def includes all of the target-specific definitions files, which are located within $BLD_CONFIG/target. In this directory are subdirectories named after the possible targets (both platform targets and user-specified targets), each containing a target.def definitions file. For user-specific targets like debug, the definitions file merely adds the correct flags to the list of target-specific compiler options. For the various platform targets, such as Linux-2.0_x86, this file sets macros indicating the platform we are building on and the default compilers we will use for Fortran, C, and C++. The platform name is used to locate and include a definitions file platform.def from beneath the directory $BLD_CONFIG/platform that sets any platform-specific compiler or linker flags. The compiler names are used to locate and include files f77.def, c.def and cpp.def from beneath the directory $BLD_CONFIG/compiler, which set up any compiler-specific flags that are needed. (The user-specific definitions file, if present in $BLD_CONFIG/make, is included just prior to the compiler-specific files, so that the user can override the default compiler choices for this platform.)

Once all of these various macros have been defined, make is directed to include the local makefile for the current code package being built, which is normally called Make.mm. This local makefile should define macros which include what source files are to be compiled and what libraries or binaries need to be built. The contents of the local makefile will be discussed in the next section. After the local makefile for the code package has been processed, std-make.def includes more definitions files from $BLD_CONFIG/make. These files give the build rules for compiling Fortran, C and C++ source code files, archiving object files into libraries, and linking application codes. These build rules are written in terms of all the macros that were defined earlier. In addition, there are definitions for many different standard make targets in the files std-targets.def and std-test.def. These targets do things such as create new directory structures, export code package files, remove old files from previous builds, and print out information about the current build configuration. All of these targets, along with any make targets defined by the local makefile for the code package, constitute the set of valid targets that can be passed as an argument on the mm command line.

The Local Makefile
^^^^^^^^^^^^^^^^^^

Each code package must provide a makefile or set of makefiles that tells the build system what source code files are contained in this package and what libraries or binary executables can be produced. The mm script has the ability to recursively invoke make commands within the current directory and all subdirectories below it. Thus, each local makefile should describe the source files and potential products of the current directory and provide a rule for recursing into any subdirectories. As mentioned earlier, the local makefile is normally named Make.mm, but this choice can be overridden by setting the environment variable LOCAL_MAKEFILE or using mm with the -f option.

There are several examples of local makefiles in $BLD_CONFIG/tests that show how to construct a makefile for building a library or an application code. In general, the first thing to do in your Make.mm file is include a project-specific definitions file (with a .def filename extension). This file can be used to set special behaviors for this project, such as using certain compiler options or linking with certain libraries. The file $BLD_CONFIG/tests/local.def illustrates how to do this. The macros beginning with PROJ\_ are project-specific settings. For each compiler (Fortran, C, and C++), there are macros that add compiler flags, -D options to define macros for the preprocessor, -I options for adding directories to the include file search path, linker flags, and -L options for adding directories to the library file search path. (Note that for the macro defines, include file paths, and library file paths, the -D, -I, or -L will be prepended automatically, so they do not need to be included here. Hence, setting PROJ_CC_DEFINES = FOO, for example, will add the flag -DFOO to all C compilation commands for this project.) This file can also be used to define the library (PROJ_LIB) and object files (PROJ_OBJS) that are produced in this project, although this is typically done within the Make.mm file itself. It is not necessary to include a project-specific definitions file if nothing special is required for this project; this is merely another degree of freedom for customizing the build procedure for each project.

After including any project-specific definitions, the local makefile should define its make targets, which at the bare minimum includes the default make target all. Let us look at the Make.mm file in directory $BLD_CONFIG/tests/projlib as an example. The purpose of this makefile is to compile a C source file and a C++ source file into object files and archive these two object files into a library. We first define the macro PROJECT to be the name of our project (in this case, test). Next we define PROJ_LIB to be the name of the library we are building here. We make use of the macros LIBDIR and EXT_AR, which were previously defined by the build system in file std-macros.def. LIBDIR is the full path of the directory where libraries are built, and EXT_AR is set to a, the extension for a static library on Unix systems. Note that the value of LIBDIR uses the macro TARGET_TAG, so that versions of a library for different targets are placed in separate subdirectories. After PROJ_LIB, we set PROJ_SRCS equal to the list of source code files that are to be compiled into the library. This is converted into a list of object files PROJ_OBJS by a definition in std-builds.def that changes the filename extension of each file to the value of EXT_OBJ, which is normally o on Unix file systems. (The list PROJ_OBJS actually contains the library filename followed by each object filename in parentheses, which tells make to consider the timestamp of each object file within the library archive separately when checking dependencies.)

In this example, we have source files c_hello.c and cpp_hello.cc being compiled into a library. Each file is recognized as a source code file by its filename extension, with the supported extensions being defined in std-macros.def. As usual, these conventions for filename extensions can be overridden by redefining the appropriate macros in a user-specific or project-specific definitions file. The files std-fortran.def, std-c.def and std-cpp.def contain make rules for compiling Fortran, C and C++ source code files and adding the resulting object files to a library archive. Note that these files also define macros which gather up all of the compiler flags and options from any definitions files specific to the current platform, compiler, target, user or project, and pass them all on to the appropriate compiler or archiver command.

Next in this sample Make.mm file are definitions of the macros PROJ_CLEAN and PROJ_DISTCLEAN. The build system definitions file std-targets.def defines make targets clean and distclean which remove the files specified by PROJ_CLEAN and PROJ_DISTCLEAN. Typically, we use the command mm clean to remove products previously built using this makefile and the command mm distclean to remove all files created during previous builds (including dependency files, for example). Thus, we have in this example defined PROJ_CLEAN to be PROJ_LIB, the library produced by this makefile. PROJ_DISTCLEAN is set equal to PROJ_DEPENDENCIES, which is defined by std-builds.def to contain the list of PROJ_SRCS with the EXT_DEPEND extension appended to each filename.

At last, we get to the key definition of the make target all. This is the default target that will be built when we invoke mm with no target specified on the command line. In this case, our primary build target is the PROJ_LIB, and the build system already has a rule for how to build this in std-builds.def. The rule will first echo to the screen information about what library is being updated. Then it will ensure that the directory structure for building the library exists, creating it if necessary. Finally, it will build each of the items in PROJ_OBJS and add it to the library archive using standard compiler and archiver commands. Because of the way in which the dependencies have been arranged, only source files that have been updated more recently than the corresponding object file within the library archive are actually recompiled when rebuilding an existing target.

This completes our description of the most basic local makefile required for placing a code package under the build procedure. To summarize, the local makefile should define PROJ_LIB to be the full pathname of the library that is the product of this package. PROJ_SRCS is a list of the local source code files to be compiled into this product library. In addition, the makefile should define the make target all, which is the default product built by the mm command.

Beyond these basics, there are several other actions that may be defined in Make.mm using the make targets in std-targets.def. For example, one can create an export make target that will copy the source code files and product library into a subdirectory under $EXPORT_ROOT. The pre-defined make targets export-headers and export-libraries will copy over any files listed in the macros EXPORTABLES and EXPORT_LIBS, respectively. Another key capability is recursion into subdirectories. If a code package consists of several subpackages, this can be handled using the recurse make target. This target will visit each of the subdirectories listed in RECURSE_DIRS and invoke mm there with the target specified by BLD_ACTION. As an example, the definition::

    SUBPACKAGES = Foo Bar
    clean::
        BLD_ACTION="clean" RECURSE_DIRS="$(SUBPACKAGES)" $(MM) recurse

would indicate that the command mm clean should execute not only in the current directory, but also in the subdirectories Foo and Bar. Using this recursion technique, we can construct libraries that require sources from multiple subpackages in a simple manner. In addition to the top-level Make.mm file, we create another Make.mm file in each subdirectory that describes the local source files that must be compiled in this directory. This allows us to rebuild modified source code files only in one directory or recursively below the current directory.

Finally, we should note that we have thus far only described the process of compiling source code files and archiving the resulting object files into libraries. One can also define in Make.mm binary executable targets which compile source code files and link them together with libraries to form an executable. There are examples of this in the Make.mm file in $BLD_CONFIG/tests/mixed. Notice how make targets such as c_f77 write the compile and link commands using macros from the std-fortran.def, std-c.def and std-cpp.def definition files. This ensures that these executables will be built with the same compilers and options as everything else in the build procedure.

Summary
^^^^^^^

Here is a list of the steps to take in order to use the build procedure with a new code package:

    * Check out the CVS module config, which contains the mm script and all the basic definitions files for the build system (as well as this documentation).
    * Set BLD_ROOT to the root directory for building product libraries and executables and EXPORT_ROOT to the root directory for exporting header files and pre-built libraries or binaries. Also set BLD_CONFIG to the root directory for the build system files if this is not the same as $BLD_ROOT/config.
    * Ensure that $BLD_CONFIG/make is in your PATH variable, so that you can execute the mm script.
    * Create a local makefile for each directory within the directory structure of your code package that contains header files to be exported and/or source code files to be compiled into libraries or applications.
    * Set TARGET to a comma-delineated list of compilation targets such as debug compilation or linking with MPI.
    * Invoke mm to build the default target all or any other make target defined in std-targets.def or the local makefile. 



.. _pyre-inventory-implementation:

Inventory, Trait, and Notary
----------------------------

Inventory has descriptors as its static members. 
Descriptors are special python objects that define __get__ (and __set__) methods. 

.. note:: Descriptors are not instances of pyre.inventory.Descriptor.Descriptor. The class pyre.inventory.Descriptor.Descriptor is not a real descriptor class in the sense of `this discussion <http://users.rcn.com/python/download/Descriptor.htm>`_. In pyre, pyre.inventory.Trait.Trait is the real descriptor class. 

An instance of a descriptor describes a property of its parent, but **does not hold the value of this property**. This is why you can inherit Inventory but its static members do not conflict with different instances of Inventory classes.

For example ::

  class Inventory(Component.Inventory):
  
      import pyre
  
      a = pyre.inventory.str('a', default="" )

Here pyre.inventory.str makes a Str instance. Str is a subclass of Trait. 
So the instance Inventory.a is a descriptor that says the instance of 
Inventory class will have a property called a. 
This property is a string, and it defaults to be empty.

When Inventory class is instantiated, ::

  inventory = Inventory(...)

and when we are asking for its property, ::

  inventory.a

The __set__ and __get__ functions of Trait class will get called and which, 
in turn, calls getTraitValue and setTraitValue of the Inventory class. 

So you can see the class Trait and Inventory have to cooperate to
implement this idea of Descriptor.

Notary
^^^^^^
Inventory has its metaclass pyre.inventory.Notary.Notary. 
The metaclass's __init__ will be called when the object of the class 
(Note: the class object != the class instance) is built. 
In Notary's __init__, all traits of an Inventory class will be 
collected to two registries, one for properties, and one for facilities.


.. _weaver:

Pyre rendering: Weaver
----------------------

A typical pyre pattern is to move rendering methods to a class which subclasses Weaver:

.. inheritance-diagram:: pyre.weaver.Weaver
   :parts: 1

which makes use of the visitor pattern while traversing data structures:

.. inheritance-diagram:: pyre.weaver.components.BlockComments pyre.weaver.components.BlockMill pyre.weaver.components.CommentingStrategy pyre.weaver.components.Indenter pyre.weaver.components.LineComments  pyre.weaver.components.LineMill pyre.weaver.components.Mill pyre.weaver.components.Stationery
   :parts: 1

using a number of underlying rendering classes called "mills":  

.. inheritance-diagram:: pyre.weaver.mills.CMill pyre.weaver.mills.CshMill pyre.weaver.mills.CxxMill pyre.weaver.mills.Fortran77Mill pyre.weaver.mills.Fortran90Mill pyre.weaver.mills.HTMLMill pyre.weaver.mills.MakeMill pyre.weaver.mills.PerlMill pyre.weaver.mills.PythonMill pyre.weaver.mills.ShMill pyre.weaver.mills.TeXMill pyre.weaver.mills.XMLMill 
   :parts: 1

Examples where this has been done include generating html pages in :ref:`opal<opal>` or gemetrical pml files in :ref:`pyre.geometry <pyre-geometry>`.




.. _mystic:

Science tutorial: Distributed optimization
==========================================





