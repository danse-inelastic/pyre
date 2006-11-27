// -*- C++ -*-
// 
//  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// 
//                               Michael A.G. Aivazis
//                        California Institute of Technology
//                        (C) 1998-2005 All Rights Reserved
// 
//  <LicenseText>
// 
//  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// 

#include <portinfo>
#include <Python.h>

#include "misc.h"

// copyright

char pyacis_copyright__doc__[] = "";
char pyacis_copyright__name__[] = "copyright";

static char pyacis_copyright_note[] = 
    "acis python module: Copyright (c) 1998-2005 Michael A.G. Aivazis";


PyObject * pyacis_copyright(PyObject *, PyObject *)
{
    return Py_BuildValue("s", pyacis_copyright_note);
}
    
// version
// $Id: misc.cc,v 1.1.1.1 2006-11-27 00:09:24 aivazis Exp $

// End of file
