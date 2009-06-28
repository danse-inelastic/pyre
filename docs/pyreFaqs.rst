FAQs (note: in future this should probably be put into forum or google group..):
=====
    
Basic pyre:
-----------

    - :ref:`What does pyre require of the format (input/output, etc) of my code?<code-requirements>`
    - Should I write an additional python layer around my code, or should all of that go into a pyre component? 


The pyre inventory:
-------------------

    - How do I manipulate a component's inventory after the component has been instantiated?
    - How can I get a component to manipulate its parents inventory?
    - If I use a component as a facility, can I access one of the facility's methods to return a result?
    - In __init__, what is the preferred naming convention for the instance? for the facility?
    - What is the preferred naming convention for the component file versus the component class?
    - Where can I find out more (documentation) on what is available in the inventory?
    - Is it preferred to change a variable in the inventory or at the state level?
    - Behind the scenes: How does the Inventory class work? 


Inheritance:
------------

    - Are there reserved method names within pyre?
    - My component needs to inherit from something else, can pyre handle that?
    - What are the minimum methods I have to include to have a functional pyre component? 


Using pyre:
-----------

    - How do I run everything from the commandline?
    - Can an application/script drive another application/script?
    - How do I have a component use another component?
    - Recombinant graphs: Can two components use the same instance of a child component?
    - Lists & dicts don't work in pyre from the commandline, what am I doing wrong?
    - Can I change the wiring of a pyre application on the fly?
    - What goes in a script's run method versus, say, a 'greet' method?
    - Can I use different explicit functions within my C code as seperate pyre components, or do I have to wrap all of my code at once?
    - How can I replace a method within my C code if all the C code is within a single library?
    - How can I know where user inputs of my application come from (command line? odb? pml?)? How can I track where user inputs of subcomponents ( and subsubcomponents ... ) of my application come from? 


Using component Factories
---------------------------

    - :ref:`What is a factory?<what-is-factory>`
    - What can a pyre factory do and not do?
    - How can I override args to a component factory from command line? From .pml file?
    - Is it possible to have multiple components in an application that use the same factory name? 

.. _code-requirements:

What does pyre require of the format (input/output, etc) of my code?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Nothing, except to feed the inventory items into your code before it is executed.  If your code needs to maintain state between executions, consider wrapping it as a pyre daemon, such as ipa, idd, or :ref:`journal <journal>`.


.. _what-is-factory:

What is factory
^^^^^^^^^^^^^^^
Here, we are describing the factory that can be fed to the facility declaration 
in :ref:`pyre inventory<pyre-inventory>`.

In python, a factory is any callable that creates an object and returns it to the caller. There are many ways to implement factories in Python. The first way is so simple, you probably never realized you were using a factory:

1. A python class is a factory. Whenever you declare a class, the result is that you create a python class, which is a factory of instances of this class::

    class A(object):       
        def __init__( self):
            return 
    # After the class definintion here is executed, class A is created, and it is a factory

The object named A (a python class) is a factory for making objects of type A::

    >>> myA = A()  # This calls the class object "A" to make a new A object for you.

2. A factory could be a simple python method. This example assumes the previous class declaration is in a module named A.py::

    def AFactory_1():
        from A import A
        a = A()
        return a

Here's how this would get used::

    >>> myA = AFactory_1()
    >>> print myA.__class__.__name__
    A

3. A factory could also be another class in its own right, as long that class supplies a function named __call__ (any such class is called a functor). 

One advantage of having all these options is to allow arbitrarily complicated creation schemes. Here's a class that creates objects of class A. All of those objects are one and the same object. That is, every instance from this factory shares the same state::

    class AFactory_2( object):
    
        theInstance = None
    
        def __call__( self):
            if self.theInstance is None:
                from A import A
                self.theInstance = A()
            a = self.theInstance
            return a

Here's how that would be used::

    >>> afactory = AFactory_2()
    >>> a1 = afactory()
    >>> a2 = afactory()
    >>> a1 is a2
    True
    >>> a1
    <__main__.A instance at 0x2a955e3368>
    >>> a2
    <__main__.A instance at 0x2a955e3368>

Note that in this example, every time you ask the afactory for another A, you get exactly the same instance of a. This is actually one way of creating `singleton <http://en.wikipedia.org/wiki/Singleton_pattern>`_.


Miscellaneous:
--------------
    - Does pyre understand swig?
    - What is the ~/.pyre directory for? 
    - :ref:`binding`
    - :ref:`template`
    - :ref:`wrapping`


.. _binding:

Binding
^^^^^^^
Binding is the process of making a piece of code callable. In the DANSE project, we frequently use Python bindings for code written in C, C++, and FORTRAN; that means that we use pieces of code that make functions written in those languages callable from Python. Python bindings involve several components including wrappers; the process is described in Writing C extensions for Python.


.. _template:

Template
^^^^^^^^
In C++, a template function (or class) is a technique for defining function (or class) implementation while not specifying types used in the interface. Loosely speaking, templates define implementation but leave interface to be defined later, while inheritance defines interface but delays deciding implementation.

For example, suppose you have two functions:

float addf(float a, float b){return a + b;}
double add( double a, double b){return a + b;}

One template function could replace both of these functions:

template <typename T> 
T add( T a, T b){ return a + b;}

This simplifies writing the code: there's only one function to keep track of, instead of one function for every type. Strictly speaking, this is not a function definition: it is a blueprint for the compiler to create a function definition ("instantiate" the template). The programmer has deferred until later the decision of what type(s) to use in this function. This function will work for any type for which the "+" operator is defined.

The person using this function has to make it clear to the compiler which types are to be involved:

float a=1.2, b=2.3;
float c = add<float>( a,b);

double d = 3.4, e = 4.5;
double f = add<double>( d, e);


.. _wrapping:

Wrapping
^^^^^^^^
Wrapping is the process of providing a new interface to an already existing piece of code. The code that does this is a wrappe






Journal:
--------
    - Is there a journal tutorial, possibly incomplete?
    - How do I turn a journal on or off from command line? 
    
    
    
    
    
    
    
