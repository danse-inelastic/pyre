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


def journald(name=None):

    if name is None:
        name = "journald"
        
    import journal
    journal.info("journal").activate()
    journal.debug("journal").activate()
    
    journal.info("journald").activate()
    journal.debug("journald").activate()

    app = journal.daemon(name)
    app.run()


# main
if __name__ == "__main__":
    journald()
    

# version
__id__ = "$Id: journald.py,v 1.1.1.1 2006-11-27 00:09:39 aivazis Exp $"

# End of file 
