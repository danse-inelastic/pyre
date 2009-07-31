VNF Install Guide
=================

This walkthrough assumes a fresh Ubuntu or Fedora install.  However, any part of the guide can be theoretically apply to any unix-based system.  This guide assumes no background whatsoever in unix-based systems.

CACR
-----

To aquire a CACR account first generate a `SSH key <http://www.cacr.caltech.edu/main/?page_id=85>`_.  Then head over to the `CACR Registration Site <http://www.cacr.caltech.edu/main/?page_id=477>`_

Configuring Your Environment
----------------------------

There are several packages that need to be installed prior to actually installing VNF.  

Install Dependencies
~~~~~~~~~~~~~~~~~~~~

For Ubuntu, open a terminal and type 'sudo apt-get install' and each of the packages names in the following list. For Fedora, log in to root, and the equivalent is 'yum install'.

- subversion
- postgresql-8.3
- pgadmin3 (Optional)
- wxPython
- numpy
- matplotlib
- hdf5

Test wxPython, numpy, and matplotlib by making sure there are no errors when you type, in terminal::

	python
	>>> import wx
	>>> import numpy
	>>> import matplotlib

Downgrading to Python 2.5
~~~~~~~~~~~~~~~~~~~~~~~~~

Note: Pyre and vnf have been known to work with Python2.6 on Fedora 11, so try continuing with installation without downgrading from Python2.6 first. 

For Ubuntu, to install Python 2.5 onto your system, open terminal and type in this code::

	sudo apt-get install python2.5

Edit the /usr/share/python/debian_defaults, changing the default version arg to python2.5.

Open terminal and type this code in::

	sudo mv /usr/bin/python /usr/bin/python2.5
	sudo ln -s /usr/bin/python2.6 /usr/bin/python
 

Make.mm
~~~~~~~~

Follow the instructions :ref:`here <make-mm>`.

As mentioned in the detailed instructions for Make.mm, a shortcut is to download this :download:`bash <bash_tools.linux>` file and then move it to root.  Make sure it is named bash_tools.linux.

In terminal, navigate to your root directory and execute this code::

	. .bash_tools.linux

On Fedora, this is::

	source bash_tools.linux
	./bash_tools.linux

Checking Python and Make.mm Install
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	
	
If you downgraded to Python2.5, try the following:
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

Check to make sure Pyre and Make.mm is properly installed by following the directions on testing them (e.g. typing app.py in terminal should produce the message "creating application 'Simple' in 'simple.py'").

Downloading VNF
---------------

In terminal, go to where you would like to install VNF and type::

	svn co svn://danse.us/VNET/vnf/releases/alpha
	cd alpha
	mm

Throughout these instructions, it will be assumed that everything is installed in /home/username, for example's sake.

Configuring the Database
------------------------

For Ubuntu, open a terminal and type::

	sudo su postgres -c psql template1

	createdb vnf

In Fedora, logged in as root, type in a terminal::

        service postgresql start
	su -- postgres
	psql template1
	CREATE USER username WITH PASSWORD 'password';
	\q
	su -- username
	createdb vnf

Where username is one that matches the apache httpd.conf file (in Apache Configuration, below).

Remote DB Servers
-----------------

If you installed PostgreSQL on the machine where you installed VNF, you can skip this step. If not, modify $VNF_EXPORT/config/clerk.pml (where $VNF_EXPORT is where VNF is installed. For example, /home/username/alpha). The default clerk.pml is::

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

psycopg2 Install
-----------------

Download the tarball from a `direct link <http://www.initd.org/pub/software/psycopg/psycopg2-2.0.11.tar.gz>`_, then extract the files inside the tarball into an easily accessible place (preferably root).  Run the setup files.

If there are error messages, it may be necessary to download header files for postgresql.

Apache Server Install and Configuration
-----------------------------------------

Download the Apache install files `here <http://www.gtlib.gatech.edu/pub/apache/httpd/httpd-2.2.11.tar.gz>`_.  Install Apache. 

In terminal, log in to root and type::

	apachectl start

Apache Configuration
~~~~~~~~~~~~~~~~~~~~~

Next, enable CGI.  For Ubuntu, through terminal, navigate to the directory `~/etc/apache2/sites-enabled/000-default` and enter this code::

	ScriptAlias /cgi-bin/ /usr/lib/cgi-bin/
	<Directory "/usr/lib/cgi-bin">
		AllowOverride None
		Options +ExecCGI -MultiViews +SymLinksIfOwnerMatch
		Order allow,deny
		Allow from all
	</Directory>

For Fedora, open the file /etc/httpd/conf/httpd.conf and enter this::

	ScriptAlias /cgi-bin/ /var/www/cgi-bin/
	<Directory "/var/www/cgi-bin">
		AllowOverride None
		Options +ExecCGI -MultiViews +SymLinksIfOwnerMatch
		Order allow,deny
		Allow from all
	</Directory>

Also, you may need to find where it says::

	User apache
	Group apache 

and change apache to your username (which matches your database username). 

It may also be necessary to disable SELinux (System > Administration > SELinux Management).

After making changes to httpd.conf, restart the server by logging in to root and type::

	apachectl restart

Then, make a directory that serves CGI.  For Ubuntu, in terminal::

	sudo mkdir /usr/lib/cgi-bin/vnf
	sudo cd /usr/lib/cgi-bin/vnf

For Fedora, in terminal::

	mkdir /var/www/cgi-bin/vnf
        cd /var/www/cgi-bin/vnf

Make a simple CGI (main.cgi) that sets up enviromental variables and also calls the VNF application. Assuming vnf was downloaded in /home/username (replace username with your actual username) and Pyre was installed following the Make.mm instructions in /home/username/dv/tools/pythia-0.8, main.cgi should contain::

	#!/usr/bin/env bash

        VNFINSTALL=/home/username/alpha
        PYREINSTALL=/home/username/dv/tools/pythia-0.8
	export PATH=$VNFINSTALL/bin:$PATH
	export PYTHONPATH=$PYREINSTALL/packages/histogram:$PYTHONPATH
	export PYTHONPATH=$VNFINSTALL:$PYTHONPATH
	export LD_LIBRARY_PATH=$PYREINSTALL/lib:$LD_LIBRARY_PATH
	export PYRE_DIR=$PYREINSTALL/packages:$PYRE_DIR
	cd $VNFINSTALL/cgi && python main.py $@

Adjust the above code as needed and make sure main.cgi is executable::

        chmod +x main.cgi

HTML content needs to be made available by creating a symbolic link. For example::

	sudo cd /var/www
 	sudo ln -s /home/username/dv/tools/pythia-0.8/vnf/html vnf

To configure the vnf web application, you will need to put these new paths in /home/username/alpha/config/main.pml. For example::

	<inventory>
	
	  <component name='main'>
	    <property name='home'>http://localhost/vnf/</property>
	    <property name='cgi-home'>http://localhost/cgi-bin/vnf/main.cgi</property>
	    <property name='imagepath'>/vnf/images</property>
	    <property name='javascriptpath'>/vnf/javascripts</property>
	  </component>
	
	</inventory>

Start Daemons
-------------

With the db properly functioning, we can initialize three vnf services (a journal daemon, a unique identifier generator daemon, and an authentication daemon) by executing the shell script::

	 cd $VNF_EXPORT/bin
	 ./startservices.sh

or::

        cd $VNF_EXPORT/bin
        ./journald.py
        ./idd.py
        ./ipad.py

where $VNF_EXPORT is the directory where vnf is installed (example: /home/username/alpha).

You will also want to initialize the vnf database with some tables by executing the python script within $VNF_EXPORT/bin::

 	./initdb.py

If this fails, it usually means your database connection was not configured correctly. Go reconfigure first.

Test Your VNF Installation
--------------------------

Open your browser and go to http://localhost/cgi-bin/vnf/main.cgi.

Troubleshooting
---------------

Try http://localhost/cgi-bin/vnf/main.cgi?actor=login for the test url.

Error log locations:

- For apache: /var/log/httpd
- For vnf: $VNF_EXPORT/log

You could also try running VNF out of </home/username>/dv/tools/pythia-0.8/vnf instead of </home/username>/alpha. In this case, main.cgi should read::

	#!/usr/bin/env bash

        VNFINSTALL=/home/username/dv
        EXPORT_ROOT=$VNFINSTALL/tools/pythia-0.8
        export PATH=$EXPORT_ROOT/bin:$PATH
        export PYTHONPATH=$EXPORT_ROOT/packages/histogram:$PYTHONPATH
        export PYTHONPATH=$EXPORT_ROOT/modules:$PYTHONPATH
        export PYTHONPATH=$EXPORT_ROOT/packages:$PYTHONPATH
        export LD_LIBRARY_PATH=$EXPORT_ROOT/lib:$LD_LIBRARY_PATH
        export PYRE_DIR=$EXPORT_ROOT/packages:$PYRE_DIR
        cd $EXPORT_ROOT/vnf/cgi && python main.py $@

and $VNF_EXPORT in the instructions above would refer to /home/username/dv/tools/pythia-0.8/vnf, for example.

