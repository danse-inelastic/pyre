// -*- C++ -*-
// 
//  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// 
//                               Michael A.G. Aivazis
//                        California Institute of Technology
//                        (C) 1998-2005  All Rights Reserved
// 
//  <LicenseText>
// 
//  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// 

#include <portinfo>

#include <Python.h>

#include "exceptions.h"
#include "bindings.h"


char pynttcp_module__doc__[] = "";

// Initialization function for the module (*must* be called initnttcp)
extern "C"
void
initnttcp()
{
    // create the module and add the functions
    PyObject * m = Py_InitModule4(
        "nttcp", pynttcp_methods,
        pynttcp_module__doc__, 0, PYTHON_API_VERSION);

    // get its dictionary
    PyObject * d = PyModule_GetDict(m);

    // check for errors
    if (PyErr_Occurred()) {
        Py_FatalError("can't initialize module nttcp");
    }

    // install the module exceptions
    pynttcp_runtimeError = PyErr_NewException("nttcp.runtime", 0, 0);
    PyDict_SetItemString(d, "RuntimeException", pynttcp_runtimeError);

    return;
}

// version
// $Id: nttcpmodule.cc,v 1.1.1.1 2006-11-27 00:09:45 aivazis Exp $

// End of file
