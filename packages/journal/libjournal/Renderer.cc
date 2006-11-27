// -*- C++ -*-
//
//--------------------------------------------------------------------------------
//
//                              Michael A.G. Aivazis
//                       California Institute of Technology
//                       (C) 1998-2005  All Rights Reserved
//
// <LicenseText>
//
//--------------------------------------------------------------------------------
//

#include <portinfo>
#include <map>
#include <vector>
#include <string>

#include "Renderer.h"
#include "Entry.h"

using namespace journal;

// interface
Renderer::string_t Renderer::render(const Entry & entry) {
    string_t text = header(entry) + body(entry) + footer(entry);
    return text;
}

// meta-methods
Renderer::~Renderer() {}

// version
// $Id: Renderer.cc,v 1.1.1.1 2006-11-27 00:09:38 aivazis Exp $

// End of file
