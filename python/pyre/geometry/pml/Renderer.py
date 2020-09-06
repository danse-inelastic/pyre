#!/usr/bin/env python
#
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2005 All Rights Reserved
# 
#  <LicenseText>
# 
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

from pyre.geometry.Visitor import Visitor
from pyre.weaver.mills.XMLMill import XMLMill


class Renderer(XMLMill, Visitor):


    def render(self, bodies):
        document = self.weave(bodies)
        return document


    # solids bodies
    def onBlock(self, block):
        line = '<block diagonal="({0!s}, {1!s}, {2!s})"/>'.format(block.diagonal)

        self._write(line)
        return


    def onCone(self, cone):
        line = '<cone height="{0!s}" topRadius="{1!s}" bottomRadius="{2!s}"/>'.format(cone.height, cone.top, cone.bottom)

        self._write(line)
        return


    def onCylinder(self, cylinder):
        line = '<cylinder height="{0!s}" radius="{1!s}"/>'.format(cylinder.height, cylinder.radius)

        self._write(line)
        return


    def onPrism(self, prism):
        # NYI
        return self._abstract("onPrism")


    def onPyramid(self, pyramid):
        # NYI
        return self._abstract("onPyramid")


    def onSphere(self, sphere):
        line = '<sphere radius="{0!s}"/>'.format(sphere.radius)

        self._write(line)
        return


    def onTorus(self, torus):
        line = '<torus major="{0!s}" minor="{1!s}"/>'.format(torus.major, torus.minor)

        self._write(line)
        return


    def onGeneralizedCone(self, cone):
        line = '<generalized-cone major="{0!s}" minor="{1!s}" scale="{2!s}" height="{3!s}"/>'.format(cone.major, cone.minor, cone.scale, cone.height)

        self._write(line)
        return


    # Euler operations
    def onDifference(self, difference):
        self._write("<difference>")

        self._indent()
        difference.op1.identify(self)
        difference.op2.identify(self)
        self._outdent()

        self._write("</difference>")

        return


    def onIntersection(self, intersection):
        self._write("<intersection>")

        self._indent()
        intersection.op1.identify(self)
        intersection.op2.identify(self)
        self._outdent()

        self._write("</intersection>")

        return


    def onUnion(self, union):
        self._write("<union>")

        self._indent()
        union.op1.identify(self)
        union.op2.identify(self)
        self._outdent()

        self._write("</union>")

        return


    # transformations
    def onDilation(self, dilation):
        self._write("<dilation>")

        self._indent()
        body = dilation.body.identify(self)
        self._write( "<scale>{0:g}</scale>".format(dilation.scale))
        self._outdent()

        self._write("</dilation>")
        return


    def onReflection(self, reflection):
        self._write("<reflection>")

        self._indent()
        body = reflection.body.identify(self)
        self._write("<vector>({0!s}, {1!s}, {2!s})</vector>".format(reflection.vector))
        self._outdent()

        self._write("</reflection>")
        return


    def onReversal(self, reversal):
        self._write("<reversal>")

        self._indent()
        body = reversal.body.identify(self)
        self._outdent()

        self._write("</reversal>")
        return


    def onRotation(self, rotation):
        self._write("<rotation>")

        self._indent()
        rotation.body.identify(self)
        self._write("<angle>{0:g}</angle>".format(rotation.angle))
        self._write("<vector>({0!s}, {1!s}, {2!s})</vector>".format(rotation.vector))
        self._outdent()

        self._write("</rotation>")
        return


    def onTranslation(self, translation):
        self._write("<translation>")

        self._indent()
        translation.body.identify(self)
        self._write("<vector>({0!s}, {1!s}, {2!s})</vector>".format(translation.vector))
        self._outdent()

        self._write("</translation>")
        return


    def onGeometry(self, body):
        self._indent()
        body.identify(self)
        self._outdent()
        return


    def __init__(self):
        XMLMill.__init__(self)
        return
            

    def _renderDocument(self, body):

        self._rep += ['', '<!DOCTYPE geometry>', '', '<geometry>', '']
        self.onGeometry(body)
        self._rep += ['', '</geometry>']

        return


# version
__id__ = "$Id: Renderer.py,v 1.1.1.1 2006-11-27 00:09:57 aivazis Exp $"

#
# End of file
