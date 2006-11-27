// -*- C++ -*-
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
//                             Michael A.G. Aivazis
//                      California Institute of Technology
//                      (C) 1998-2005  All Rights Reserved
//
// <LicenseText>
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//

#include <portinfo>
#include "journal/error.h"
#include <iostream>

int main() {

    journal::error_t error("test");
    std::cout << error.name() << ": state=" << error.state() << std::endl;

    error << journal::at(__HERE__) << "Hello world!" << journal::endl;

    return 0;
}

// version
// $Id: error.cc,v 1.1.1.1 2006-11-27 00:09:40 aivazis Exp $

// End of file 
