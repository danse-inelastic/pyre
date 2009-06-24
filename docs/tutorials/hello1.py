#!/usr/bin/env python

from pyre.applications.Script import Script as base

class HelloApp(base):

    def main(self):
        print "Hello World!"
        return
    
    def __init__(self):
        super(HelloApp, self).__init__("hello1")
        return
    
# main
if __name__ == "__main__":
    app = HelloApp()
    app.run()
    
# End of file
