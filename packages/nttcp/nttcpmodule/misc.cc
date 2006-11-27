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

#include "misc.h"


// copyright

char pynttcp_copyright__doc__[] = "";
char pynttcp_copyright__name__[] = "copyright";

static char pynttcp_copyright_note[] = 
    "nttcp python module: Copyright (c) 1998-2004 Michael A.G. Aivazis";


PyObject * pynttcp_copyright(PyObject *, PyObject *)
{
    return Py_BuildValue("s", pynttcp_copyright_note);
}
    
// version
// $Id: misc.cc,v 1.1.1.1 2006-11-27 00:09:45 aivazis Exp $

// End of file
