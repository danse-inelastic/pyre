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


def actor(name):
    from GenericActor import GenericActor
    return GenericActor(name)


def authenticatingActor(name):
    from AuthenticatingActor import AuthenticatingActor
    return AuthenticatingActor(name)


def sentry(*args):
    from Sentry import Sentry
    return Sentry(*args)


# version
__id__ = "$Id: __init__.py,v 1.1.1.1 2006-11-27 00:09:47 aivazis Exp $"

# End of file 
