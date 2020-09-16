from future.standard_library import install_aliases
install_aliases()

import sys
if sys.version_info < (3,0):
    strtype = basestring
else:
    strtype = str
def isstr(s):
    return isinstance(s, strtype)
