VNF Install Guide
=================

This walkthrough assumes a fresh Ubuntu install.  However, any part of the guide can be theoretically apply to any unix-based system.  This guide assumes no background whatsoever in unix-based systems.

CACR
-----

To aquire a CACR account first generate a `SSH key <http://www.cacr.caltech.edu/main/?page_id=85>`_.  Then head over to the `CACR Registration Site <http://www.cacr.caltech.edu/main/?page_id=477>`_

Configuring Ubuntu
-------------------

There are several packages that need to be installed prior to actually installing VNF.  

SVN
~~~~

To install SVN onto your system, open terminal and type in this code::

	sudo apt-get install subversion


Downgrading to Python 2.5
~~~~~~~~~~~~~~~~~~~~~~~~~

To install Python 2.5 onto your system, open terminal and type in this code::

	sudo apt-get install python2.5

Edit the /usr/share/python/debian_defaults, changing the default version arg to python2.5.

Open terminal and type this code in::

	sudo mv /usr/bin/python /usr/bin/python25
	sudo ln -s /usr/bin/python2.6 /usr/bin/python
 

Make.mm
~~~~~~~~

Detailed install explanations are located :ref:`here <make-mm>`.

As a shortcut, download this :download:`bash <bash_tools.linux>` file and then move it to root.  Make sure it is named bash_tools.linux.

In terminal, navigate to your root directory and execute this code::

	. .bash_tools.linux

Checking Python and Make.mm Install
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	
	
In terminal, execute this code::

	env
	
After you execute env, you should see a mass of text that describe a variety of enviromental variables.  The variables that you want to look for to check the validity of all you have installed so far are::

	PYTHON_VERSION=2.5
	PYTHONSTARTUP=(whatever your root directory is)/.python
	PYTHON_LIBDIR=/usr/lib/python2.5
	

Pyre Install
-------------

In terminal, navigate to root and type this code in::

	svn co svn+ssh://svn@danse.us/pyre/branches/patches-from-jiao

	cd patches-from-jiao/

	mm

Opal Install
------------

In terminal, navigate to root and type this code in::

	cd patches-from-jiao/

	cd packages/

	cd opal/

	mm

Configuring main.cgi
---------------------

In the folder where you installed Pyre in, navigate to a a document /pythia-0.8/vnf/cgi/main.cgi.  Using a text editor, change the second line of text from::

	VNFINSTALL=/home/jbk/dv

to::

	VNFINSTALL=/home/(your home directory)/(wherever Pyre is installed to)

PostgreSQL Install
------------------

To install postgreSQL open terminal and type::

	sudo apt-get install postgresql-8.3

pgAdmin3 Install
----------------

To install pgAdmin3, open terminal and type::

	sudo apt-get install pgadmin3

Configuring the Database
------------------------

Open terminal and type::

	sudo su postgres -c psql template1

	createdb vnf

If you installed PostgreSQL on the machine where you installed VNF, you can skip this step. If not, modify $VNF_EXPORT/vnf/config/clerk.pml. The default clerk.pml is::

	<inventory>

	  <component name='clerk'>
	     <property name='db'>vnf</property>
	     <property name='dbwrapper'>psycopg2</property>
	  </component>

	</inventory>

where the property "db" tells the vnf applications where to connect to database. The default value "vnf" means that a unix domain socket connection to the local PostgreSQL db server is used, and the database name is "vnf". To connect to a remote db server, the value of "db" should be something like::

	username:password@hostname:port:database

or, to take a specific case::

	vnf:1234567@db.server:5432:vnf

With the db properly functioning, we can initialize three vnf services (a journal daemon, a unique identifier generator daemon, and an authentication daemon) by executing the shell script::

	 cd $VNF_EXPORT/vnf/bin
	 ./startservices.sh

You will probably also want to initialize the vnf database with some tables by executing the python script within $VNF_EXPORT/vnf/bin::

 	./initdb.py

If this fails, it usually means your database connection was not configured correctly. Go reconfigure first. 

psycopg2 Install
-----------------

Download the tarball from a `direct link <http://www.initd.org/pub/software/psycopg/psycopg2-2.0.11.tar.gz>`_, then extract the files inside the tarball into an easily accessible place (preferably root).  Run the setup files.

Apache Server Install and Configuration
-----------------------------------------

Download the Apache install files `here <http://www.gtlib.gatech.edu/pub/apache/httpd/httpd-2.2.11.tar.gz>`_.  Install Apache.

Apache Configuration
~~~~~~~~~~~~~~~~~~~~~

Next, enable CGI.  Through terminal, navigate to the directory `~/etc/apache2/sites-enabled/000-default` and enter this code::

	ScriptAlias /cgi-bin/ /usr/lib/cgi-bin/
	<Directory "/usr/lib/cgi-bin">
		AllowOverride None
		Options +ExecCGI -MultiViews +SymLinksIfOwnerMatch
		Order allow,deny
		Allow from all
	</Directory>

Then, make a directory that serves CGI.  In terminal::

	sudo mkdir /usr/lib/cgi-bin/vnf
	sudo cd /usr/lib/cgi-bin/vnf

Make a simple CGI (main.cgi) that sets up enviromental variables and also calls the VNF application::

	#!/usr/bin/env bash
	releaser=/home/vnf/dv/danse/buildInelast/web-vnf
	EXPORT_ROOT=$releaser/EXPORT
	source $EXPORT_ROOT/bin/envs.sh
	cd $EXPORT_ROOT/vnf/cgi && python main.py $@
	chmod +x main.cgi

HTML content needs to be made available by creating a symbolic link. For example::

	sudo cd /var/www
 	sudo ln -s $VNF_EXPORT/vnf/html vnf

To configure the vnf web application, you will need to put these new paths in $VNF_EXPORT/vnf/config/main.pml. For example::

	<inventory>
	
	  <component name='main'>
	    <property name='home'>http://my.static.ip.address/vnf/</property>
	    <property name='cgi-home'>http://my.static.ip.address/cgi-bin/vnf/main.cgi</property>
	    <property name='imagepath'>/vnf/images</property>
	    <property name='javascriptpath'>/vnf/javascripts</property>
	  </component>
	
	</inventory>





