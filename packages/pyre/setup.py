#!/usr/bin/env python
# 
# Michael McKerns
# mmckerns@caltech.edu 
#
#NOTE: this setup.py is for pythia .zip build w/ 'mm zip3' or 'mm zip4'
from setuptools import setup, find_packages
from sys import platform
import os

###############################################################################
# pyre looks for .odb files in $EXPORT_ROOT/etc and $HOME/.pyre (and ".")
# make sure that one of the above are available...

# use defaults for common environment variables
export_root_nux = '/usr/etc'
export_root_mac = '/etc'
export_root_win = 'C:\Program Files\etc' #FIXME: figure out default for windows
# or do a local install
export_root_user = os.path.join(os.path.expanduser('~'), '.pyre')
###############################################################################
local_install = True  #XXX: should be True / False;  or determined by $PREFIX ?

#determine platform
if platform[:3] == 'win':
  myOS = 'win'
  export_root_system = export_root_win
elif platform[:6] == 'darwin':
  myOS = 'mac'
  export_root_system = export_root_mac
else:
  myOS = 'nux'
  export_root_system = export_root_nux

#check if environment variables were set...
try:
    export_root = os.environ['EXPORT_ROOT']
    export_root_found = True
except KeyError:
    if not local_install: export_root = export_root_system
    else: export_root = export_root_user
    export_root_found = False

#build python module...
setup(name='pythia',
      version='0.8',
      description='packages for the pyre component framework (python-only version)',
      author = 'Michael Aivazis',
      author_email = 'aivazis@caltech.edu',
      url = 'http://danse.us/trac/pyre',
      download_url = 'http://dev.danse.us/packages/',
      package_data = {'':['*.*']},
      packages = find_packages(),
     #install_requires("journal>=0.8"),
     #dependency_links = ['http://dev.danse.us/packages/'],
      )

# extract .odb files to EXPORT_ROOT
os.system("unzip pythia-odb.zip -d %s" % export_root)

# print report on environment variables used
if export_root_found:
    pass
else:
    print "\n***********************************************************"
    print "To better enable access to pyre .odb files"
    print "please set $EXPORT_ROOT as indicated in"
    print "    http://danse.us/trac/ctrl/wiki/config"
    print "or copy .odb files from source to $HOME/.pyre"
    print "\n"
    print "WARNING: Using default settings:"
    print "    EXPORT_ROOT %s" % export_root
    print "***********************************************************\n"


# end of file
