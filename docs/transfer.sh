#!/usr/bin/env sh

#this script can be altered for whoever is transfering files to the server

svn up
scp -r _build/html/ jbrkeith@login.cacr.caltech.edu:pyre
