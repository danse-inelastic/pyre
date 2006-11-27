// -*- C++ -*-
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
//                               Michael A.G. Aivazis
//                        California Institute of Technology
//                       (C) 1998-2005  All Rights Reserved
//
// <LicenseText>
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//

#include <portinfo>
#include <iostream>

#include "pyre/geometry/CanonicalMesh.h"


int main()
{

    typedef pyre::geometry::CanonicalMesh<double> mesh_t;

    mesh_t mesh(1000, 4500);

    std::cout << "mesh@(" << &mesh << "):" << std::endl;
    std::cout << "    nodes = " << mesh.vertices() << std::endl;
    std::cout << "    simplices = " << mesh.simplices() << std::endl;

    return 0;
}

// version
// $Id: canonicalMesh.cc,v 1.1.1.1 2006-11-27 00:10:13 aivazis Exp $

// End of file
