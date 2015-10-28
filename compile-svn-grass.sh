#!/bin/sh

####################################################################
# QJ1520265 project - source code and support files for OGC WMS and
# WPS implementation http://rain.fsv.cvut.cz
#
# Purpose: compile GRASS from SVN
# Author: Martin Landa <martin.landa fsv.cvut.cz>
# Licence: see LICENCE file for details
####################################################################

cd /opt/grass
svn up 
if [ "$1" = "f" ] ; then
    make distclean
fi
if [ ! -f include/Make/Platform.make ] ; then
    ./configure \
	--prefix=/usr/local \
	--with-gdal --with-proj --with-proj-share=/usr/share \
	--with-nls \
	--with-cxx --enable-largefile \
	--with-freetype --with-freetype-includes=/usr/include/freetype2 \
	--with-sqlite \
	--with-cairo --with-python \
	--with-geos --with-pthread --with-lapack --with-blas
fi

set -e
make

export GRASS_BATCH_JOB=/opt/subdayprecip-design/grass/extension.sh
export GRASS_SKIP_MAPSET_OWNER_CHECK=1
/opt/grass/bin.x86_64-unknown-linux-gnu/grass70 --text /opt/grassdata/subdayprecip/PERMANENT
unset GRASS_BATCH_JOB

exit 0
