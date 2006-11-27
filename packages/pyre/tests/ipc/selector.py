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


def test():

    import journal
    journal.debug("pyre.ipc.selector").activate()

    import pyre.ipc
    selector = pyre.ipc.selector()

    selector.notifyWhenIdle(onTimeout)
    
    try:
        selector.watch()
    except:
        import sys
        type, value, tb = sys.exc_info()
        print "got %s: {%s}" % (type, value)
        raise type, value

    return


count = 0
def onTimeout(selector):
    global count
    print "timeout %04d" % count
    count += 1
    return 1


# main
if __name__ == "__main__":
    test()
        

# version
__id__ = "$Id: selector.py,v 1.1.1.1 2006-11-27 00:10:11 aivazis Exp $"

# End of file 
