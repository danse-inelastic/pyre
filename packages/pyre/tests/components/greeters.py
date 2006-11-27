#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                             Michael A.G. Aivazis
#                               Orthologue, Ltd.
#                      (C) 2004-2006  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


def hello(name=None):

    if name is None:
        name = 'hello'

    from Greeter import Greeter
    greeter = Greeter(name)

    greeter.greeting = "Hello"

    return greeter
    

# version
__id__ = "$Id: greeters.py,v 1.1.1.1 2006-11-27 00:10:13 aivazis Exp $"

# End of file 
