Advanced pyre I: pyre packages
==============================


.. _pyre-units:

pyre.units
----------

`pyre.units <http://danse.us/trac/pyre/browser/pythia-0.8/packages/pyre/pyre/units>`_ provides developers an easy way to work with quantities with units. It is fairly easy and intuitive to use. For example, to create velocity quantity of 3000 meter/second, you will do ::


    from pyre.units import time, length
    velocity = 3000 * length.meter/time.second


Modules
^^^^^^^

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

Pyre contains the groundwork for an Object Relational Mapper (ORM) in pyre.db.  A class diagram is:

.. image:: images/PyreDbClassDiagram.png

As apparent, pyre.db offers a number of variable types (inheriting from "Column"), which are part of "Table".  These are managed by a subclass of DBManager, currently implemented with a postgres db backend by "Psycopg2", for example, which overrides DBManager's commit() method.  This class name is also the name of the python wrapper for postgres.

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

    >>> dbm = DbManager()
    >>> dbm.createTable(Cylinder)
    >>> cylinder = Cylinder()
    >>> dbm.insertRow(cylinder)

as well as execute other methods in the DbManager interface.


.. _pyre-xml:

Pyre's xml processor: pyre.xml
------------------------------

Here is the class diagram:

.. image:: images/PyreXmlClassDiagram.png



.. _pyre-services:

Pyre server base: pyre.services
-------------------------------

Here is the class diagram for pyre's services base:

.. image:: images/PyreServicesClassDiagram.png


.. _idd:

Generating globally unique identifiers: pyre.idd
------------------------------------------------

Here is the class diagram for pyre's idd daemon:

.. image:: images/PyreIddClassDiagram.png


.. _ipa:

Managing user sessions: pyre.ipa
--------------------------------

Here is the class diagram for pyre's ipa daemon:

.. image:: images/PyreIpaClassDiagram.png


.. _ipc:

Pyre.ipc
--------------------------------

Here is the class diagram for pyre.ipc:

.. image:: images/PyreIpcClassDiagram.png



.. _pyre-geometry:

Using and manipulating basic geometrical shapes: pyre.geometry
--------------------------------------------------------------

Pyre.geometry is a complex collection of geometry-related classes and utilities.  Let us examine the class structure.  Here is the top level diagram:

.. image:: images/PyreGeometryClassDiagram.png

In the solids package we see the differing geometrical solids available to pyre users:

.. image:: images/PyreGeometrySolidsClassDiagram.png

In the operations package we have:

.. image:: images/PyreGeometryOperationsClassDiagram.png

where we see the types of boolean operations that can be done on basic geometrical shapes.  In the pml package we have:

.. image:: images/PyreGeometryPmlClassDiagram.png

where we see classes related to rendering and parsing pml files for geometrical structure objects.  In the pml.parsing:

.. image:: images/PyreGeometryPmlParserClassDiagram.png

there are :ref:`weaver-like<weaver>` classes using the visitor pattern to render and parse data in pml format about the geometrical objects.
