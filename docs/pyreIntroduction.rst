Pyre overview
=============

Pyre is an integration framework for high-performance computing based on `python <http://www.python.org>`_.  

Pyre provides developers of scientific computing software with a set of tools, such as :ref:`easy specification <pyre-inventory>` of user inputs for computing engines, :ref:`a decomposition scheme<pyre-component>` to construct sophisticated scientific software in a layered architecture, and :ref:`distributed debugging support <journal>`. Pyre also promotes **intellitgent software development** through patterns of componentization, reusability, and application of design patterns. 

.. Pyre also provides a variety of useful tools, following are some of them:
 * :ref:`Units <pyre-units>`
 * :ref:`Database access <pyre-db>`
 * :ref:`Geometry <pyre-geometry>`
 * :ref:`XML support <pyre-xml>`
 * `Opal: web application builder <http://danse.us/trac/pyre/wiki/Opal>`_

Pyre aims to be *universal scientific middleware*: it provides standard ways to interact with any number of subcomponents from an application's interface and pass settings in a top-down way, such as when configuring a distributed computational job prior to launch.  Future versions of pyre may also include support for dynamically loading/unloading components/bundles and message-passing between them.

In short, pyre attempts to solve a very hard problem: make independently developed applications work together. Pyre developers benefit from shorter concept-to-deployment and reduced development costs because pyre technology provides for the integration of pre-built and pre-tested component subsystems.  **Scientific projects using pyre** include the `Center for Simulation of Dynamic Response of Materials <http://csdrm.caltech.edu/>`_, the `Center for the Predictive Modeling and Simulation of High-Energy Density Dynamic Response of Materials <http://www.psaap.caltech.edu/>`_, `Computational Infrastructure for Geodynamics <http://www.geodynamics.org/cig/>`_, and `Distributed Data Analysis for Neutron Scattering Experiments <http://danse.us/>`_.

To learn more, browse :ref:`these tutorials <pyre-tutorials>`.

