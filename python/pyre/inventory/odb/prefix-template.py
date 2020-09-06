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

import os

stem = None
try:
    stem = os.environ["PYTHIA_HOME"]
except KeyError:
    try:
        stem = os.environ["EXPORT_ROOT"]
    except KeyError:
        prefix = os.environ.get('DEPLOYMENT_PREFIX', None)
        if prefix is None:
            prefix = os.environ.get('CONDA_PREFIX', None)
        if prefix is None:
            prefix = os.environ['PREFIX']

if stem:
    _SYSTEM_ROOT = os.path.join(stem, "etc")
else:
    _SYSTEM_ROOT = os.path.join(prefix, 'etc', 'pyre')

_USER_ROOT = os.path.join(os.path.expanduser('~'), '.pyre')
_LOCAL_ROOT = ['.']


# version
__id__ = "$Id: prefix-template.py,v 1.1.1.1 2006-11-27 00:10:02 aivazis Exp $"

# End of file 
