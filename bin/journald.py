#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                             Michael A.G. Aivazis
#                      California Institute of Technology
#                      (C) 1998-2005  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


def run():
    import journal

    app = journal.daemon()
    return app.run(spawn=True)
    

if __name__ == "__main__":
    run()


# version
__id__ = "$Id: journald.py,v 1.1.1.1 2006-11-27 00:09:51 aivazis Exp $"

# End of file 
