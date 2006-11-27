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


def main():


    from pyre.applications.Script import Script


    class TimerApp(Script):


        class Inventory(Script.Inventory):

            import pyre.inventory

            count = pyre.inventory.int('count', default=100**2)
            count.meta['tip'] = 'the number of times to execute the loop being timed'


        def main(self, *args, **kwds):
            import pyre.monitors
            t = pyre.monitors.timer("t")
            
            total = 0
            index = 0

            t.start()
            while index <= self.inventory.count:
                total += index**2
                index += 1
            t.stop()

            print "sum of the squares: %d, %f secs" % (total, t.read())

            return


        def __init__(self):
            Script.__init__(self, 'timer')
            return


    app = TimerApp()
    return app.run()


# main
if __name__ == '__main__':
    # invoke the application shell
    main()


# version
__id__ = "$Id: timer.py,v 1.1.1.1 2006-11-27 00:10:13 aivazis Exp $"

# End of file 
