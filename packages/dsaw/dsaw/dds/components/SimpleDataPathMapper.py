# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

from pyre.components.Component import Component

class SimpleDataPathMapper(Component):

    def __init__(self, name='simple-obj2path', facility='obj2path'):
        super(SimpleDataPathMapper, self).__init__(name, facility)
        return


    def __call__(self, obj):
        return self.engine(obj)


    def _init(self):
        super(SimpleDataPathMapper, self)._init()
        from dsaw.dds.SimpleDataPathMapper import SimpleDataPathMapper as engine
        self.engine = engine()
        return
    

# version
__id__ = "$Id$"

# End of file 
