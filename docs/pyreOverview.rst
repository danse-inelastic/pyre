Pyre Documentation
===================

Basic pyre:
-----------

    - pyre as an application framework
    - pyre scripts and components
    - pyre properties and facilities
    - How is a script different from a component? How do I decide which to use?
    - What does pyre require of the format (input/output, etc) of my code?
    - What is the difference between a facility and an component?
    - What is a factory?
    - What is a .pml file? How and when is it intended to be used?
    - What is a .obd file? How and when is it intended to be used?
    - How is a .odb file different from the same file with a .py extension?
    - Should I write an additional python layer around my code, or should all of that go into a pyre component? 


The pyre inventory:
-------------------

    - What goes in the inventory, versus what is a state variable?
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

    - Are there reserved method names within pyre, and how can I find out what they are?
    - My component needs to inherit from something else, can pyre handle that?
    - Do I have to include methods like "_defaults" if I don't use them?
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

    - What is a factory?
    - What can a pyre factory do and not do?
    - How can I override args to a component factory from command line? From .pml file?
    - Is it possible to have multiple components in an application that use the same factory name? 


Miscellaneous:
--------------

    - Does pyre understand swig?
    - What is the ~/.pyre directory for? 


Journal:
--------

    - Is there a journal tutorial, possibly incomplete?
    - How do I turn a journal on or off from command line? 
    
    

Pyre: an application framework
==============================

The pyre framework is a Python-based system for constructing applications. Applications consist of a top level application component and a set of lower level components. The framework performs services such as instantiating components, configuring them, and cleaning up.

Pyre is one package of pythia, a larger collection of related systems such as a distributed communication system (journal), code-generators (weaver), GUI generators (blade), and a build system (merlin).


Pyre scripts and components
===========================

A script is an application meant to be run from the command line. A script usually inherits from the Script class in pyre.applications.Script. For convenience, a "hello world" script may be auto-generated using app.py in pyre.applications, and users may then customize that script to fit their needs.

An application is a special component that manages and coordinates the work of other components. Application inherits from pyre.inventory.Component.

A component is an instance of the class pyre.inventory.Component. Components are the basic chunk of code managed by the pyre framework.

To make your own component, subclass Component. Component has an embedded class Inventory; subclasses of Component should similarly have an embedded class Inventory which inherits from Component.Inventory. The inventory is the designated place for the public to interact with components. By having an explicit place to interact with the component, components gain the ability to control whether they accept a given change, and what to do with that setting.

Components are closely related to facilities. Every component specifies the facility to which it can be bound.


Facility
---------
A facility is how one component (let's call it A) specifies that it would like another component to do some work for it. It's a bit like a help-wanted ad. As part of the facility spec, A gets to recommend a default component to do the job, or it can recommend a way to build a component to do the job (factory). Users get the final decision: they can direct that a different component be used, specifying that on the command line or through .pml file(s).

Property
----------
A component requests user input by declaring a property in its inventory. All properties are instances of pyre.inventory.property, and usually they are instances of a property subclass, such as int, float, str, etc. The programmer can specify the public name of a property, a default value, and a validator.




Binding
---------
Binding is the process of making a piece of code callable. In the DANSE project, we frequently use Python bindings for code written in C, C++, and FORTRAN; that means that we use pieces of code that make functions written in those languages callable from Python. Python bindings involve several components including wrappers; the process is described in Writing C extensions for Python.

Template
----------
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


Wrapping
---------
Wrapping is the process of providing a new interface to an already existing piece of code. The code that does this is a wrappe



    
    
    
    
    
    
    
    
