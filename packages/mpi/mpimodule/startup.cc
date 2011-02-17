// -*- C++ -*-
//
//  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
//                              Michael A.G. Aivazis
//                        California Institute of Technology
//                        (C) 1998-2005 All Rights Reserved
//
// <LicenseText>
//
//  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//

#include <portinfo>
#include <Python.h>
#include <mpi.h>

#include "journal/debug.h"

#include "startup.h"


namespace pyrempi{
  
  // wrap MPI_Finalize
  void mpi_finalize()
  {
    MPI_Finalize();
  }
  
}


// initialize
bool pympi_initialize()
{
    // check whether MPI is already intialized
    int isInitialized = 0;
    int status = MPI_Initialized(&isInitialized);

    if (status != MPI_SUCCESS) {
        PyErr_SetString(PyExc_ImportError, "MPI_Initialized failed");
        return false;
    }

    if (!isInitialized) {
      // init mpi
      int *argc = NULL;
      char ***argv = NULL;
      MPI_Init(argc, argv);
      // really initialized?
      status = MPI_Initialized(&isInitialized);
      if (status != MPI_SUCCESS) {
        PyErr_SetString(PyExc_ImportError, "MPI_Initialized failed");
        return false;
      }
      if (!isInitialized) {
        PyErr_SetString(PyExc_ImportError, "Should not reach here.");
        return false;
      }
      // all good, and register mpi_finalize
      atexit(pyrempi::mpi_finalize);
    }

    journal::debug_t info("mpi.init");
    if (info.state()) {
        int rank, size;
        MPI_Comm_rank(MPI_COMM_WORLD, &rank);
        MPI_Comm_size(MPI_COMM_WORLD, &size);

        info
            << journal::at(__HERE__)
            << "[" << rank << ":" << size << "] "
            << "MPI_Init succeeded"
            << journal::endl;
    }

    return true;
}

// version
// $Id: startup.cc,v 1.1.1.1 2006-11-27 00:09:45 aivazis Exp $

// End of file
