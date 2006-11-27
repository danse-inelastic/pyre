#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                             Michael A.G. Aivazis
#                      California Institute of Technology
#                      (C) 1998-2005  All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


def journald():

    from journal.components.Daemon import Daemon
    app = Daemon()
    app.main()


# main
if __name__ == "__main__":
    import journal
    journal.debug("journald").activate
    
    journald()
    

# version
__id__ = "$Id: journald.py,v 1.1.1.1 2006-11-27 00:09:34 aivazis Exp $"

# End of file 
