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

    subs = {
        'SPEAKER': 'Michael Aivazis',
        'COMPANY': 'California Insitute of Technology',
        'STATE': 'well'
        }

    text = "Hello, this is ${SPEAKER} from ${COMPANY}. I hope you are ${STATE}."

    import pyre.util
    print pyre.util.expandMacros(text, subs)
    
    return


# main
if __name__ == "__main__":
    test()


# version
__id__ = "$Id: expand.py,v 1.1.1.1 2006-11-27 00:10:13 aivazis Exp $"

# End of file 
