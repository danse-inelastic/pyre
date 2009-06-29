##############################################################################
#
# Rules for building and publishing epydoc documentation.
#
# Targets:
#
# all       -- build epydoc documents in HTML format [default]
# clean     -- remove all generated files
# publish   -- publish the HTML documents online, the user must have ssh
#              access to the WEBDOCDIR server
#
##############################################################################


PKGNAME = pyre
OUTPUT = html
WEBDOCDIR = login.cacr.caltech.edu:/cacr/home/proj/danse/docs.danse.us/docroot/$(PKGNAME)


all:
	epydoc --config=epydoc.cfg --output=$(OUTPUT) \
	       --name=$(PKGNAME) $(PKGNAME)


clean:
	/bin/rm -rf $(OUTPUT)


publish:
	rsync -e /usr/bin/ssh -va --chmod=a+rwx,o-w,Dg+s,Fa-x \
	    $(OUTPUT)/ $(WEBDOCDIR)/api
