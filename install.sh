#!/bin/sh

####################################################################
# QJ1520265 project - source code and support files for OGC WMS and
# WPS implementation http://rain.fsv.cvut.cz
#
# Purpose: install software requirements
# Author: Martin Landa <martin.landa fsv.cvut.cz>
# Licence: see LICENCE file for details
####################################################################

apt-get install --yes flex bison libproj-dev libtiff-dev \
	mesa-common-dev libglu1-mesa-dev libfftw3-dev libblas-dev \
	liblapack-dev libcairo-dev proj-bin libgdal1-dev libwxbase3.0-dev \
	gettext subversion emacs24-nox g++ python-numpy cgi-mapserver \
	mapserver-bin apache2 python-lxml gdal-bin make htop python-wxgtk3.0

a2enmod cgi
service apache2 restart

# Proj.4 (5514)
EPSG=/usr/share/proj/epsg
if [ `grep 5514 $EPSG | wc -l` = 1 ] ; then
    cat proj4/epsg >> $EPSG
fi

if [ ! -d /opt/grass ] ; then
    svn checkout https://svn.osgeo.org/grass/grass/branches/releasebranch_7_2 /opt/grass
    ./compile-svn-grass.sh
    git clone https://github.com/geopython/PyWPS.git /opt/pywps
    cp wps/pywps.cgi /usr/lib/cgi-bin
    chgrp www-data /opt/pywps/pywps/Templates/ -R
    chmod g+w /opt/pywps/pywps/Templates/ -R
fi
./configure.sh

exit 0
