// -*- C++ -*-
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
//                             Michael A.G. Aivazis
//                      California Institute of Technology
//                      (C) 1998-2005  All Rights Reserved
//
// {LicenseText}
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//

#define WITHOUT_JOURNAL_DEBUG
#include <journal/debug.h>

int main() {

    journal::debug_t debug("null");

    debug
        << "Hello world!"
        << journal::newline
        << journal::endl;

    return 0;
}

// version
// $Id: null.cc,v 1.1.1.1 2006-11-27 00:09:40 aivazis Exp $

// End of file 
