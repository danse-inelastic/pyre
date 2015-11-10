FROM fedora:21

MAINTAINER "Jiao Lin <jiao.lin@gmail.com>"

RUN yum install -y deltarpm
RUN yum install -y git cmake make gcc-c++ python python-devel rpm-build

RUN curl -s https://packagecloud.io/install/repositories/${PKGCLOUD_USERNAME}/${PKGCLOUD_REPO}/script.rpm.sh | bash
RUN yum install -y ${DEP_DANSE_PKGS}
