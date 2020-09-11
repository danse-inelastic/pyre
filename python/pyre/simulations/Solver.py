#!/usr/bin/env python
# 
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2005  All Rights Reserved
# 
#  <LicenseText>
# 
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 

from pyre.components.Component import Component


class Solver(Component):


    def initialize(self, app):
        self._loopInfo.log("initializing solver '{0!s}'".format(self.name))
        return


    def launch(self, app):
        self._loopInfo.log("launching solver '{0!s}'".format(self.name))
        return


    def newStep(self, t, step):
        self.t = t
        self.step = step
        self._loopInfo.log(
            "{0!s}: step {1:d}: starting with t = {2!s}".format(self.name, self.step, self.t))
        return


    def applyBoundaryConditions(self):
        self._loopInfo.log(
            "{0!s}: step {1:d}: applying boundary conditions".format(self.name, self.step))
        return


    def stableTimestep(self, dt):
        self._loopInfo.log(
            "{0!s}: step {1:d}: stable timestep dt = {2!s}".format(self.name, self.step, dt))
        return dt


    def advance(self, dt):
        self._loopInfo.log(
            "{0!s}: step {1:d}: advancing the solution by dt = {2!s}".format(self.name, self.step, dt))
        return


    def publishState(self, directory):
        self._monitorInfo.log(
            "{0!s}: step {1:d}: publishing monitoring information at t = {2!s} in '{3!s}'".format(self.name, self.step, self.t, directory))
        return


    def plotFile(self, directory):
        self._loopInfo.log(
            "{0!s}: step {1:d}: visualization information at t = {2!s} in '{3!s}'".format(self.name, self.step, self.t, directory))
        return


    def checkpoint(self, filename):
        self._loopInfo.log(
            "{0!s}: step {1:d}: checkpoint at t = {2!s} in '{3!s}'".format(self.name, self.step, self.t, filename))
        return


    def endTimestep(self, t):
        self._loopInfo.log(
            "{0!s}: step {1:d}: end of timestep at t = {2!s}".format(self.name, self.step, t))
        return


    def endSimulation(self, steps, t):
        self._loopInfo.log(
            "{0!s}: end of timeloop: {1:d} timesteps, t = {2!s}".format(self.name, steps, t))
        return


    def __init__(self, name, facility=None):
        if facility is None:
            facility = "solver"
            
        Component.__init__(self, name, facility)
        
        self._elc = None
                
        import journal
        self._loopInfo = journal.debug("{0!s}.timeloop".format(name))
        self._monitorInfo = journal.debug("{0!s}.monitoring".format(name))

        from pyre.units.time import second
        self.t = 0.0 * second

        self.step = 0

        return


# version
__id__ = "$Id: Solver.py,v 1.1.1.1 2006-11-27 00:10:06 aivazis Exp $"

#
# End of file
