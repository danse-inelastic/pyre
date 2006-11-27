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

#include "Entry.h"

using namespace journal;

// helpers

static Entry::meta_t initializeDefaults();

// interface
// meta-methods

Entry::~Entry() {}

// static data

Entry::meta_t Entry::_defaults = initializeDefaults();

// helpers
Entry::meta_t initializeDefaults() {
    Entry::meta_t defaults;

    defaults["severity"] = "<unknown>";
    defaults["facility"] = "<unknown>";
    defaults["filename"] = "<unknown>";
    defaults["function"] = "<unknown>";
    defaults["line"] = "<unknown>";

    return defaults;
}

// version
// $Id: Entry.cc,v 1.1.1.1 2006-11-27 00:09:37 aivazis Exp $

// End of file
