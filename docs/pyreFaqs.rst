Pyre FAQs:
==========
    
Basic pyre:
-----------

    - How is a script different from a component? How do I decide which to use?
    - What does pyre require of the format (input/output, etc) of my code?
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
    
    
    
    
    
    
    
