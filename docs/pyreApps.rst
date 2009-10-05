.. applications-that-use-pyre

Applications that use pyre
==========================

A number of applications use the pyre framework and are good examples of how to effectively employ components to make developmenet of scientific applications easier, more cost-effective, and less prone to architectual design flaws.  We discuss a few of those here.

.. _drchopsandpyre:

DrChops
-------

DrChops is a reduction package o reduce data from direct-geometry time-of-flight neutron chopper spectrometers. It benefits from pyre and is very flexible and meets needs of users of different
levels. 


.. image:: http://drchops.caltech.edu/Docs/docs/reduction/DeveloperGuide/html/figures/reduction-package-layers.png
   :width: 600px

The design of DrChops follows the guidelines of pyre software-engineering principles.
To ensure that the DrChops software is easy to use for novice users but still
flexible enough and not be a stopper for advanced users, the DrChops software
were built into several layers.

"c/c++" library
    "c/c++" layer is responsible for intensive computations only feasible to be implemented in low level language. For example, this layer includes a class ERebinAllInOne to rebin data in tof bins to data in evenly-spaced energy bins.
"python vector-compatible" function library
    "python vector compatible" layer vectorCompat is the joint point between c++ and python. All c++ codes are implemented to deal with "vector"-like objects, e.g., energy bins. The vectorCompat python package accepts vector arguments and call the corresponding c++ methods to do the real work. This layer separate other python layers from c++ codes and python bindings.
"python histogram-compatible" methods and classes
    "python histogram compatible" layer histCompat allows developers to deal with objects with more physics meanings. This layer is built on top of the vectorCompat layer. A histogram is an object consisting of axes and datasets and meta data. In the histCompat layer, histograms are our focus. Classes in this layer take histograms instead of vectors as arguments, and implementations of those classes decompose histograms to vectors and call the corresponding methods in the vectorCompat layer.
"reduction core" 
    The "reduction core" layer makes use of components in histCompat layer and implement classes that are more high-level. The histCompat layer is more concerned with low-level operations like "rebin to evenly-spaced energy bins" and "fit a curve to gaussian and find the center". The "reduction.core" layer is more concerned with "calculate calibration constants out of calibration data" and "reduce I(det, pix, tof) to S(phi,E)".
"pyre component"
    The "pyre component" layer makes use of methods and classes in the "reduction core" layer and provide those methods and classes easy access to user configurations. 

By careful design and decomposition of reduction procedures, the DrChops software is able to provide
novice users auto-generated GUI to pre-constructed reduction workflows; and also can provide
advanced users great flexibility of using different reduction components in pre-constructed
reduction workflows, or even modifying the reduction workflows by using command-line interface
or xml-based configuration files:

.. image:: http://drchops.caltech.edu/Docs/docs/reduction/DeveloperGuide/html/figures/reduction-package-layers-UIandComputation.png
   :width: 800px


.. _luban_include:

Luban
-----

Luban is a generic user-interface specification language and builder. More information can be found in its documentation, which is linked to below.

.. toctree::

   luban/Introduction
   luban/Installation
   luban/Tutorials
   luban/API
   luban/LubanApp
   luban/Gongshuzi
   luban/History

