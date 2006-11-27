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
#include "journal/firewall.h"
#include <iostream>

int main() {

    journal::firewall_t firewall("test");
    std::cout << firewall.name() << ": state=" << firewall.state() << std::endl;

    firewall << journal::at(__HERE__) << "Hello world!" << journal::endl;

    return 0;
}

// version
// $Id: firewall.cc,v 1.1.1.1 2006-11-27 00:09:40 aivazis Exp $

// End of file 
