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


from pyre.applications.Script import Script


class CGI(Script):


    class Inventory(Script.Inventory):

        import pyre.inventory

        stream = pyre.inventory.outputFile("stream")
        stream.meta['tip'] = "where to place the generated text"

        content = pyre.inventory.str(
            name="content", default="html",
            validator=pyre.inventory.choice(["raw", "html", "attachment"]))
        content.meta['tip'] = "the target browser behaviour"

        debug = pyre.inventory.bool(name="debug", default=False)
        debug.meta['tip'] = "suppress some html output for debugging purposes"
    
    
    stdin_size_limit = 1024*1024*16

    

    def collectUserInput(self, registry):

        # first extract standard commandline arguments
        help, argv = self.processCommandline(registry)

        # argv now contains the left over, unprocessed arguments
        # look through them for GET input
        argv = self.collectCGIInput(registry, argv)

        return help, argv


    def collectCGIInput(self, registry, argv):
        # get access to the environment variables
        import os

        # remember the cgi inputs so that we can output them when necessary (debug)
        self._cgi_inputs = os.environ.copy()
        
        # create a parser for query strings
        parser = self._createCGIParser()

        # figure out the request method
        try:
            method = os.environ['REQUEST_METHOD'].upper()
        except KeyError:
            method = 'GET'

        # extract the headers
        headers = {}
        headers['content-type'] = os.environ.get(
            'CONTENT_TYPE', 'application/x-www-form-urlencoded')
        try:
            headers['content-length'] = os.environ['CONTENT_LENGTH']
        except KeyError:
            pass
        
        # process arguments from query string
        if method == 'GET' or method == 'HEAD':
            try:
                query = os.environ['QUERY_STRING']
            except KeyError:
                pass
            else:
                parser.parse(registry, query, 'query string')
                
        elif method == 'POST':
            
            try:
                query = os.environ['QUERY_STRING']
            except KeyError:
                pass
            else:
                parser.parse(registry, query, 'query string')

            content_type = headers['content-type']
            
            normalform = 'application/x-www-form-urlencoded'
            if content_type[:len(normalform)] == normalform:
                import sys
                inlines = []
                for line in sys.stdin:
                    inlines.append(line)
                    parser.parse(registry, line, 'form')
                self._cgi_inputs['sys.stdin'] = inlines
                    
            elif content_type.find( 'multipart/form-data' ) != -1:
                self._handle_upload(headers, registry, parser)
                
            else:
                import journal
                firewall = journal.firewall('opal')
                firewall.log("NYI: unsupported content-type '%s'" % content_type)
        else:
            import journal
            journal.firewall('opal').log("unknown method '%s'" % method)

        # if we got commandline arguments, parse them as well
        for arg in argv:
            if arg and arg[0] == '?':
                arg = arg[1:]
            parser.parse(registry, arg, 'command line')
            
        return


    def printHeaders(self):
        if self.content == "html":
            print 'Content-type: text/html'
            print ''
        elif self.content == "attachment":
            # header output to be done by the process at a later time
            pass

        # just in case further output is done by a subprocess
        import sys
        sys.stdout.flush()

        return


    def printAttachmentHeaders(self, attachment):
        print 'Content-Type: application/force-download'
        print 'Content-Disposition: attachment; filename="%s"' % attachment
        print ''

        # just in case further output is done by a subprocess
        import sys
        sys.stdout.flush()

        return


    def initializeTraceback(self):
        # pipe stderr to stdout
        import sys
        sys.stderr = sys.stdout
        
        # decorate exceptions
        import cgitb
        cgitb.enable()
        return


    def initializeJournal(self):
        import journal
        renderer = journal.journal().device.renderer
        renderer.header = '<pre>' + renderer.header
        renderer.footer = renderer.footer + '</pre>'
        return


    def getUploads(self):
        return self._uploads

    def _handle_upload(self, headers, registry, parser):
        # file upload handling

        # mime parser
        from email.FeedParser import FeedParser
        fp = FeedParser()

        # need header
        content_type = headers['content-type']
        fp.feed( 'CONTENT-TYPE: %s\n' % content_type )

        # size limit
        size_limit = self.stdin_size_limit

        # read in chunks
        chunk_size = 8192

        # number of chunks
        n = size_limit/chunk_size
        
        # feed contents from stdin to parser
        import sys
        i=0; succeeded = False
        while i<n:
            data = sys.stdin.read( chunk_size )
            if not data: succeeded = True; break
            fp.feed( data )
            continue
        if not succeeded:
            raise RuntimeError, "stdin too large"
        
        # parsed is a mime instance
        parsed = fp.close()

        #
        header = 'Content-Disposition'

        if self.inventory.debug: 
            self._cgi_inputs['uploaded mime'] = parsed.as_string()

        args = []
        uploads = {}
        for part in parsed.walk():

            if part.get_content_maintype() == 'multipart':
                # this part is the parent message it self, skip
                continue

            filename = part.get_param( 'filename', header = header )
            if filename:
                # this means we are dealing with a real file
                # save them to a dictionary so that later actors can handle them
                content = part.get_payload(decode=True)
                uploads[filename] = content
            else:
                # just a key,value pair
                key = part.get_param( 'name', header = header )
                value = part.get_payload()
                args.append( (key,value) )

            # pass key,value pairs to pyre option registry
            arg = '&'.join( [ '%s=%s' % (k,v) for k,v in args] )
            if arg: parser.parse( registry, arg, 'form' )

        self._uploads = uploads
        return

    
    def __init__(self, name):
        Script.__init__(self, name)
        self.stream = None
        self.content = "html"

        # debugging mode
        self.debug = False

        return


    def _configure(self):
        Script._configure(self)

        self.stream = self.inventory.stream
        self.content = self.inventory.content
        self.debug = self.inventory.debug
        return

    def _init(self):
        Script._init(self)

        if self.content == "html":
            # get the headers out asap
            self.printHeaders()

            # take care of exception output
            self.initializeTraceback()

            # format journal output
            # self.initializeJournal()

        return


    def _createCGIParser(self):
        import opal.applications
        return opal.applications.cgiParser()
        

# version
__id__ = "$Id: CGI.py,v 1.6 2008-04-21 07:51:08 aivazis Exp $"

# End of file 
