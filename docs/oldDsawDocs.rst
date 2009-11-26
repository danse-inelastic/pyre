Automatic creation of tables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
In other ORMs, such as SQLAlchemy, tables in which to store objects must be created "by hand", declaring each column and what type it is.  In dsaw tables are created automatically from the class itself::

    from dsaw.db import connect
    db = connect(db ='postgres:///test')
    
    from dsaw.db.WithID import WithID
    class User(WithID):
        username = 'bob'
        
    db.createTable(User)
   
Implied types
^^^^^^^^^^^^^
Dsaw implements all the types of pyre.db with the additional feature of not having to explicitly declare these types.  This has the desirable feature of rapid prototyping of a dataobject.  An example is the following:

.. literalinclude:: ../packages/dsaw/examples/impliedTypes.py

The only restrictions are that all implied types of stored attributes *must be initialized in the constructor* with an appropriate primitive type, reference, or list of references (see list below).  A temporary restriction is that the object must also currently inherit from pyre.db.Table, although this is more of a programming convenience than a necessity and will soon be relaxed.  Users achieve this inheritance when they also inherit from dsaw.db.WithID.WithID.

The rules for converting an implied type to a database type are the following:

* 'str' --> dsaw.db.varchar(length=64)
* 'int' --> dsaw.db.integer()
* 'real' --> dsaw.db.real()
* 'bool' --> dsaw.db.boolean()
* 'list' or 'tuple' --> dsaw.db.varcharArray(length=64)
* 'dict' --> dsaw.db.varcharArray(length=64) for keys, dsaw.db.varcharArray(length=64) for values
* a Table instance --> dsaw.db.reference()
* a list/tuple of Table instances --> dsaw.db.referenceSet()

The way this works is an on-the-fly conversion just before the object is serialized to the above dsaw types, then a just-in-time conversion back to typical python primitive types and references when the object is deserialized.  Additionally, users can mix normal python object representation with dsaw types as they desire (or for backwards compatibility).

Advanced data objects with dsaw
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dsaw is very powerful when implementing data objects.  By simply iheriting from Table, data objects can now not only refer to an instance of a given class, but also a *specific* instance (using the globally unique identifier).  As before, data objects do not have to declare data members with specific type information, as this will be inferred by the dsaw db manager.  

Example 1: matter classes
"""""""""""""""""""""""""""
The `matter data objects <http://danse.us/trac/inelastic/wiki/crystal>`_ are a complex set of classes for describing virtually any atomic structure, using (possibly) multiple lattices, space group symmetry, and look-up functions for atomic properties. However, even these complex data structures can be mapped automatically using dsaw's implied types, thereby allowing users to freely serialize their structures without inputing type information for all it's parameters and/or maintaining separate databasable objects for matter information.  Here is an example of how to database a lattice:


Example 2: vsat classes
"""""""""""""""""""""""


Example 3: bvk modules
""""""""""""""""""""""

     
        
* an example is http://danse.us/trac/VNET/browser/vnf/trunk/content/data/bvkmodels/bvk_ag_293.py


Optional types and name declaration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Users may also explicitly declare types for types using standard factory functions::
        
    from dsaw.db.WithID import WithID
    class DoubleArrayTest(WithID):
        import dsaw.db
        arr = dsaw.db.doubleArray(name='arr')
        
A complete list is given below:
        
.. autofunction:: dsaw.db.bigint
.. autofunction:: dsaw.db.boolean
.. autofunction:: dsaw.db.char
.. autofunction:: dsaw.db.date
.. autofunction:: dsaw.db.double
.. autofunction:: dsaw.db.doubleArray
.. autofunction:: dsaw.db.integer
.. autofunction:: dsaw.db.integerArray
.. autofunction:: dsaw.db.interval
.. autofunction:: dsaw.db.real
.. autofunction:: dsaw.db.smallint
.. autofunction:: dsaw.db.time
.. autofunction:: dsaw.db.timestamp
.. autofunction:: dsaw.db.varchar
.. autofunction:: dsaw.db.varcharArray
   
Optionally, a table name may be added within the class using the reserved keyword 'name' as an attribute::

    from dsaw.db.WithID import WithID
    class Test(WithId):
    
        name = 'mytablename'
        
        def sayhi(self):
            print 'hi'
            
which must be all lowercase.  This name will be used instead of the class name as the table name.  

.. _references:
   
References and versatile references
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   
Dsaw implements some interesting additional features to pyre.db:
        
* Dsaw starts to form a plug-in architecture for addtional backends such as SQLAlchemy.  This allows pyre developers to use additional features beyond those immediately available in pyre.db, such as filtering.

* Dsaw implements two system-wide tables, called _____referenceset_____ and global_pointers, which aid in linking objects. Global_pointers is a table that gives any record (which inherits from GloballyReferrable) a unique identifier. With a global pointer esablished, any object that wants to refer to any other object can use this global pointer.  Thus it has two columns, one of the table name and another for the unique id. _____referenceset_____ is a "hidden" table. It allows a table to declare that it has an association with other things.  For example, the data object Instrument consists of a list of neutron components in table "instrument".  Its components are declared as a reference set listed in the _____referenceset_____ table, which basically has a pointer to the "parent" and a pointer to the "child".  Multiple rows with the same parent give a set. The table _____referenceset_____ uses the concept of a "versatile reference", which is a reference to a set of tables rather than to a specific table. For example, the Component reference in an Instrument record is versatile.  Also, all "computationresult" tables have a pointer "origin", which is a versatile reference.  Origin is the computation that the result is calculated from. PhononDispersion is derived from ComputationResult, as are many other types of computations. Thus a versatile reference is versatile because it can refer to more than one type of table, and it usually points to a superclass of a desired table.

Consider the following example of how a reference works:

.. literalinclude:: ../packages/dsaw/examples/references.py

A longer example of how a versatile reference works is the following:

.. literalinclude:: ../packages/dsaw/examples/versatileReferences.py

Miscillaneous:

One may use db.createTable() or db.registerTable(); db.createAllTables()...the second form is mandatory for versatile references. Some api changes might be:
createTable() --> storeClass()
insertRow() --> storeObject()
