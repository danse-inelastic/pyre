FROM ubuntu:14.04

MAINTAINER "Jiao Lin <jiao.lin@gmail.com>"

RUN apt-get update
RUN apt-get install -y git build-essential
RUN apt-get install -y cmake
RUN apt-get install -y python python-dev

# danse deps
# establish repo
RUN apt-get install curl
RUN curl -s https://packagecloud.io/install/repositories/${PKGCLOUD_USERNAME}/${PKGCLOUD_REPO}/script.deb.sh | bash
# install
RUN apt-get install ${DEP_DANSE_PKGS}

