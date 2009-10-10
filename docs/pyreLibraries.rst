.. _pyrePackages:

Pyre libraries
==============

.. _pyre-units:

Automatic unit conversion: pyre.units
-------------------------------------

`pyre.units <http://danse.us/trac/pyre/browser/pythia-0.8/packages/pyre/pyre/units>`_ provides a no-brainer for unit conversion. For example, to create velocity quantity of 3000 meter/second, you will do ::


    from pyre.units import time, length
    velocity = 3000 * length.meter/time.second

A list of the units that are possible include:

 * `angle <http://danse.us/trac/pyre/browser/pythia-0.8/packages/pyre/pyre/units/angle.py>`_
 * `time <http://danse.us/trac/pyre/browser/pythia-0.8/packages/pyre/pyre/units/time.py>`_
 * `length <http://danse.us/trac/pyre/browser/pythia-0.8/packages/pyre/pyre/units/length.py>`_
 * `mass <http://danse.us/trac/pyre/browser/pythia-0.8/packages/pyre/pyre/units/mass.py>`_
 * `substance <http://danse.us/trac/pyre/browser/pythia-0.8/packages/pyre/pyre/units/substance.py>`_
 * `SI <http://danse.us/trac/pyre/browser/pythia-0.8/packages/pyre/pyre/units/SI.py>`_
 * `area <http://danse.us/trac/pyre/browser/pythia-0.8/packages/pyre/pyre/units/area.py>`_
 * `volume <http://danse.us/trac/pyre/browser/pythia-0.8/packages/pyre/pyre/units/volume.py>`_
 * `density <http://danse.us/trac/pyre/browser/pythia-0.8/packages/pyre/pyre/units/density.py>`_
 * `speed <http://danse.us/trac/pyre/browser/pythia-0.8/packages/pyre/pyre/units/speed.py>`_
 * `force <http://danse.us/trac/pyre/browser/pythia-0.8/packages/pyre/pyre/units/force.py>`_
 * `pressure <http://danse.us/trac/pyre/browser/pythia-0.8/packages/pyre/pyre/units/pressure.py>`_
 * `energy <http://danse.us/trac/pyre/browser/pythia-0.8/packages/pyre/pyre/units/energy.py>`_
 * `power <http://danse.us/trac/pyre/browser/pythia-0.8/packages/pyre/pyre/units/power.py>`_


.. _pyre-db:

Database access and object storage: pyre.db
-------------------------------------------

Pyre's base ORM (Object Relational Mapper) is pyre.db, which has the following types available:

.. .. image:: images/PyreDbClassDiagram.png

.. inheritance-diagram:: pyre.db.BigInt pyre.db.Boolean pyre.db.Char pyre.db.Date pyre.db.BigInt pyre.db.Double pyre.db.DoubleArray pyre.db.Integer pyre.db.IntegerArray pyre.db.Interval pyre.db.Real pyre.db.SmallInt pyre.db.Time pyre.db.Timestamp pyre.db.VarChar pyre.db.VarCharArray
   :parts: 1

which are inserted into a table:

.. inheritance-diagram:: pyre.db.Table
   :parts: 1

The entity which does the insertions is the DBManager, which can be connected to either the Postgres bindings Psycopg (or Psycopg2), or to the SQLite bindings:

.. inheritance-diagram:: pyre.db.Psycopg2 pyre.db.Psycopg pyre.db.SQLite
   :parts: 1

To store objects in a db, one must subclass "Table", such as::

    from Table import Table as base
    class Cylinder(base):
    
        name = 'cylinders'
    
        import pyre.db
    
        idd = pyre.db.varchar(name="id", length=64)
        id.constraints = 'PRIMARY KEY'
    
        height = pyre.db.real( name = 'height', default = 0.1 )
        innerradius = pyre.db.real( name = 'innerradius', default = 0.0 )
        outerradius = pyre.db.real( name = 'outerradius', default = 0.002 )

This table describes cylinders with parameters height, innerradius, and outerradius.  In the `pyre project dsaw <http://danse.us/trac/pyre/browser/branches/patches-from-jiao/packages/dsaw>`_, DbManager is overlaid with additional functionality for creating hierarchical data structures.  

Then users can store objects in the usual way::

    dbm = DbManager()
    dbm.createTable(Cylinder)
    cylinder = Cylinder()
    dbm.insertRow(cylinder)

as well as execute other methods in the DbManager interface. 


.. _dsaw:

Extending the capabilities of pyre.db: dsaw.db
----------------------------------------------

An extension to pyre.db, called dsaw, has recently been developed.  It allows users to access the SQLAlchemy plugin.

.. inheritance-diagram:: dsaw.db.BackReference dsaw.db.Column dsaw.db.DBManager dsaw.db.GloballyReferrable dsaw.db.QueryProxy dsaw.db.Reference dsaw.db.ReferenceSet dsaw.db.restore dsaw.db.Schemer dsaw.db.Table dsaw.db.Table2SATable dsaw.db.TableRegistry dsaw.db.Time dsaw.db.Time dsaw.db.VersatileReference dsaw.db.WithID
   :parts: 1



.. _pyre-geometry:

Constructive solid geometry: pyre.geometry
------------------------------------------

Pyre.geometry is a complex collection of geometry-related classes and utilities.  A user employs the loader and mesh:

.. inheritance-diagram:: pyre.geometry.Loader pyre.geometry.Mesh 
   :parts: 1

.. .. image:: images/PyreGeometryClassDiagram.png

to interact with a variety of basic shapes:

.. inheritance-diagram:: pyre.geometry.solids.Block pyre.geometry.solids.Cone pyre.geometry.solids.Cylinder pyre.geometry.solids.GeneralizedCone pyre.geometry.solids.Prism pyre.geometry.solids.Pyramid pyre.geometry.solids.Sphere pyre.geometry.solids.Torus 
   :parts: 1

.. .. image:: images/PyreGeometrySolidsClassDiagram.png

One can then operate on these shapes with intersections, unions, etc:

.. inheritance-diagram:: pyre.geometry.operations.Difference pyre.geometry.operations.Dilation pyre.geometry.operations.Intersection pyre.geometry.operations.Reflection pyre.geometry.operations.Reversal pyre.geometry.operations.Rotation pyre.geometry.operations.Translation pyre.geometry.operations.Union 
   :parts: 1

to form larger shapes quickly.  Each of these geometric constructions can be serialized via a series of :ref:`weaver-like<weaver>` classes to pml format.  An example of an application that uses pyer.geometry is the danse `geometry <http://dev.danse.us/trac/common/browser/geometry/trunk>`_ package.

.. 2) point me to some pyre.geometry use in your code so i can write a
 brief script...
 This might be helpful:
 http://dev.danse.us/trac/common/browser/geometry/trunk/tests/geometry/geometry_TestCase.py
 The geometry at danse common repo is an extension of pyre geometry.
 Basically it implements some basic visitors. The one tested in that
 testcase is "locate", which tells whether a point is outside, inside,
 or on the border of a shape.


.. _pyre-xml:

Xml processor: pyre.xml  
-----------------------

.. This luban0.1 code, http://dev.danse.us/trac/pyregui/browser/trunk/luban/luban/gml, uses
  pyre.xml to parse xml files. The pyre xml mechanism allows you to
  simplify the xml parsing to just define nodes for parsing (classes in
  http://dev.danse.us/trac/pyregui/browser/trunk/luban/luban/gml/parser).
  Maybe what you can do is to have a simple parser that parse xml
  documents with only two types of nodes, one for a branch-like node,
  one for a leaf-like node.

Pyre.xml allows one to simplify xml parsing by only having to define nodes for parsing.  This is how to proceed:

    1. Create a Parser class by inheriting from pyre.xml.Parser.Parser.
    2. The parse method of this new Parser class should be similar to::
       
        def parse(self, stream, parserFactory=None):
           from parser.Document import Document
           return BaseParser.parse(self, stream, Document(stream.name), parserFactory)
       
    3. Now create a subdirectory named "parser".
    4. In parser, create a Document class that represents an xml document. This Document class must have a property "tags", which is a list of all supported tags.
    5. The Document class must have one method that is used to handle the root node in the xml document. An example is the "onGui" method in::
    
        from pyre.xml.Document import Document as DocumentNode
    
        class Document(DocumentNode):
        
            tags = [
                "Gui", "MainApp", "MainFrame",
                'MenuBar', 'Menu', 'MenuItem',
                "Panel", "Splitter", "Notebook",
                "Sizer",
                "ListBox",
                'HistogramFigure', 'PyShell',
                "Section", "Note", "Paragraph", "Link",
                'Button', 'TextField', 
                "Table", "Row", "Cell",
                'Emphasis',
                "List", 'ListItem',
                'Code',
                'Figure',
                'Dialog',
                ]
        
            def onGui(self, gui):
                self.document = gui
                return

    6. All other "nodes" inherit from pyre.xml.Node.Node:
                
       .
    
       .. literalinclude:: ../packages/pyre/pyre/xml/Node.py
          :lines: 15-20
            
       and need to override methods "notify" and "content"
    7. 'notify' is used to notify the parent this element is here, and parent will takes it in.
    8. 'content' is used to deal with the plain data (not xml nodes) as
       the content of the current node
    
The result of using pyre.xml is a tree structure of nodes (not the pyre.xml.node nodes, but instances of the descriptive classes of what really this xml means). So for example, if you are dealing with an xml file that looks like::
    
    <folder name="abc">
     <file name='file1'/>
     <folder name='folder1'>
       <file name='file2'/>
     </folder>
    </folder>
    
you need to create classes Folder and File to represent folders and files. But you also need xml node classes Folder and File. 

.. This could be confusing and difficult to explain (at least to me).


Here is the class diagram:

.. inheritance-diagram:: pyre.xml.Node pyre.xml.Parser pyre.xml.Document pyre.xml.DTDBuilder 
   :parts: 1


.. _pyre-services:

Pyre server base: pyre.services
-------------------------------

Pyre services are useful when creating servers that need to provide a type of service, such as a :ref:`globally unique string creator daemon<idd>` or an :ref:`authentication daemon<ipa>`.

Here is the class diagram for pyre's services base:

.. .. image:: images/PyreServicesClassDiagram.png

.. inheritance-diagram:: pyre.services.UDPService pyre.services.TCPService pyre.services.Evaluator pyre.services.Pickler pyre.services.TCPSession pyre.services.UDPSession pyre.services.ServiceRequest
   :parts: 1


.. _idd:

Generating globally unique identifiers: pyre.idd
------------------------------------------------

Idd is a daemon which issues globally unique identifiers.  Here is its class diagram:

.. inheritance-diagram:: pyre.idd.IDDSession pyre.idd.IDDService pyre.idd.RecordLocator pyre.idd.Daemon pyre.idd.Token
   :parts: 1

.. .. image:: images/PyreIddClassDiagram.png

Objects that need a unique identifier simply use this as a facility and configure it::

    class Inventory(Base.Inventory):
        import pyre.idd
        idd = pyre.inventory.facility('idd-session', factory=pyre.idd.session, args=['idd-session'])
        idd.meta['tip'] = "access to the token server"

    def _configure(self):
        self.idd = self.inventory.idd

then obtain the identifier::

    id = self.idd.token().locator


.. _ipa:

Managing user sessions: pyre.ipa
--------------------------------

Ipa is a daemon which can manage user sessions by creating hashes, issuing tickets, and verifying passwords. Here is the class diagram:

.. .. image:: images/PyreIpaClassDiagram.png

.. inheritance-diagram:: pyre.ipa.IPASession pyre.ipa.Authentication pyre.ipa.UserManager pyre.ipa.Daemon pyre.ipa.IPAService
   :parts: 1

An example which uses pyre.ipa is the Sentry component, which performs the task of authenticating new users::

    from pyre.components.Component import Component
    
    
    class Sentry(Component):
    
    
        class Inventory(Component.Inventory):
    
            import pyre.inventory
    
            username = pyre.inventory.str('username')
            username.meta['tip'] = "the requestor's username"
    
            passwd = pyre.inventory.str('passwd')
            passwd.meta['tip'] = "the requestor's passwd"
    
            ticket = pyre.inventory.str('ticket')
            ticket.meta['tip'] = "the requestor's previously obtained ticket"
    
            attempts = pyre.inventory.int('attempts')
            attempts.meta['tip'] = "the number of unsuccessful attempts to login"
    
            import pyre.ipa
            ipa = pyre.inventory.facility("session", factory=pyre.ipa.session)
            ipa.meta['tip'] = "the ipa session manager"
    
    
        def authenticate(self):
	    ...
    
    
        def __init__(self, name=None):
            if name is None:
                name = 'sentry'
    
            super(Sentry, self).__init__(name)
	    ...    
    
    
        def _configure(self):
            Component._configure(self)
            self.username = self.inventory.username
            self.passwd = self.inventory.passwd
            self.ticket = self.inventory.ticket
            self.attempts = self.inventory.attempts
    
            self.ipa = self.inventory.ipa
    
            return

As apparent, Sentry's Inventory contains a facility for the factory function "session" which produces an instance of pyre.ipa.Session in the class diagram above.


.. _ipc:

pyre.ipc
--------

Ipc seems to provide ways to create services and clients so that you can pass messages. Here is the class diagram:

.. .. image:: images/PyreIpcClassDiagram.png

.. inheritance-diagram:: pyre.ipc.Selector pyre.ipc.UDPMonitor pyre.ipc.TCPMonitor
   :parts: 1

.. _pyre-simulations: 

Running and steering simulations in pyre: pyre.simulations
----------------------------------------------------------

Here is a solver and simulation controller for running finite element simulations:

.. .. image:: images/PyreSimulationsClassDiagram.png

.. inheritance-diagram:: pyre.simulations.SimpleSolver pyre.simulations.SimulationController
   :parts: 1

.. _pyre-util:

Pyre utilities: pyre.util
-------------------------

Here are various utilities, such as the base class, Singleton, for the singleton design pattern:

.. .. image:: images/PyreUtilClassDiagram.png

.. inheritance-diagram:: pyre.util.Singleton pyre.util.ResourceManager pyre.util.Toggle
   :parts: 1


.. _createPyreProject:

Tutorial: Creating your own pyre project
========================================

We now discuss how to create your own pyre project by reviewing typical pyre project structre and some useful Make.mm directives.

.. _pyre-directory-structure:

Pyre project structure
----------------------

A pyre project typically contains a number of directories.  For example, supposing one creates a pyre project with <package> as it's name:

* applications/

  Pyre applications typically are put in this directory with a :ref:`Make.mm <make-mm>` that exports them to the pythia-0.8/bin directory.  :ref:`Pyre convention <pyre-style>` appends a "d" to the app name if it is a service daemon.  

* etc/

  This directory stores facility factory method files, called :ref:`odb files <odb-files>`, for switching facilities at run time.  The internal structure of etc/ mirrors the structure of the application and its components.  For example suppose the application is called MdApp with the inventory::

    class MdApp(Script):
    
        class Inventory(Script.Inventory):
            import pyre.inventory as inv 
            mdEngine = inv.facility('mdEngine', default='gulp')
            mdEngine.meta['known_plugins'] = ['gulp','mmtk','lammps','cp2k']
            mdEngine.meta['tip'] = 'which md engine to use'

  Then etc/ would have the structure::

    $ ls etc
    Make.mm MdApp
    $ ls etc/MdApp
    gulp.odb mmtk.odb lammps.odb cp2k.odb
    
* <package>/

  This is the top level directory for python source.

* lib<package>/

  This contains possible c extensions.

* <package>module/

  This contains python bindings to the c extensions.

* tests/

  Tests for all parts of the project.

Although this directory structure is not mandatory, it is somewhat conventional.  Much of this structure can be generated automatically by using the :ref:`package utility<create-a-pyre-project>`. 

When creating one's own pyre project, one must learn some internals of the Make.mm build system.  Here we overview some of them.  The rest may be learned by reading config files such as .

Directives/options/macros used in Make.mm
-----------------------------------------

Make.mm format is similar to that of typical linux shell scripting.  A few macros which may be useful are:

 * export-python-package 

 * others to be included

While coding the new pyre project, one may also need to debug.  Pyre's native debugger is called journal.

.. _journal:

Journal
-------

Pyre's native debugger is called journal.
It allows developers to insert journalling instructions in their code that produce
pyre application diagnostics such as
error reporting, warnings, and debugging.

To create a journal channel and write to it include something like the following::

  >>> import journal
  >>> debug = journal.debug('myproject')
  >>> debug.activate()
  >>> debug.log( 'This is a debugging message' )

which gives the output::

   >> <stdin>:1:<module>
   >> myproject(debug)
   -- This is a debugging message
  <journal.diagnostics.Diagnostic.Diagnostic object at 0x956910>

The factory ::

  journal.debug

creates journal channels of "debug" type. And this call::

  journal.debug("myproject")

creates a journal debug channel named "myproject".
The call::

  >>> debug.activate()

activates this channel.
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
Another very useful device is a journal daemon.


Journal daemon
""""""""""""""
.. It is also a good model of a pyre application as discussed in :ref:`a section on advanced pyre <journal-structure>`.  

Because journal is a daemon, it produces debugging info for all application types, whether distributed or local.

To start using journal daemon, first execute the journal daemon by typing::

    $ journald.py	

from the command line.  (also talk about having the right pml files set up and making sure journal is "pointing" to them).  Then insert the following at the top of your pyre app::

    import journal
    journal.info(name).activate()
    journal.debug("journal").activate()

Then in the constructor, information about the code part may be labeled in order to discern which, of the many parts of your code, is outputting the information::

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

and make sure they turn "on" debug or info output for that component.  For example, this can be done with a journal.pml file in one's config directory::





.. _debugger:

Other debuggers
---------------

In addition to journal, and especially for routine debugging of individual components, interactive debuggers (such as in Eclipse) may be useful.  Pyre is particularly amenable to this type of testing since all parameters may be input via the commandline, which in Eclipse may be stored as run configurations.  

In Eclipse these run configuration can also be exported ("Shared File" under the "Common" tab) and archived or shared among developers.  Additionally, each time a developer changes the run configuration, Eclipse automatically updates the exported files.


Create your app
---------------

Once you have created your directory structure and learned how to use a debugger, you are ready to go!  Just type 'mm' to install your resulting code into the pyre installation directory and it should be available on your python path.


.. _mcvine:

Science Tutorial: Conducting a virtual neutron experiment
=========================================================

An interesting problem in scattering science is how to simulate neutron scattering.  Typically this is done via a large number virtual neutrons randomly being projected toward a virtual sample represented by a scattering kernel.




