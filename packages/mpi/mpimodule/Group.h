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

#if !defined(pympi_Group_h__)
#define pympi_Group_h__

namespace mpi {

    class Group;
    class Communicator;
}


class mpi::Group {

// interface
public:
    int size() const;
    int rank() const;
    MPI_Group handle() const;

    // factories
    static Group * group(const Communicator & comm);

    Group * include(int size, int ranks[]) const;
    Group * exclude(int size, int ranks[]) const;
    
// meta-methods
public:
    Group(MPI_Group handle);
    virtual ~Group();

// hide these
private:
        
    Group(const Group &);
    Group & operator=(const Group &);

// data
protected:

    MPI_Group _group;
};

// version
// $Id: Group.h,v 1.1.1.1 2006-11-27 00:09:44 aivazis Exp $

#endif

//
// End of file
