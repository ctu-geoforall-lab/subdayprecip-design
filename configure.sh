#!/bin/sh

####################################################################
# QJ1520265 project - source code and support files for OGC WMS and
# WPS implementation http://rain.fsv.cvut.cz
#
# Purpose: configure MapServer and PyWPS
# Author: Martin Landa <martin.landa fsv.cvut.cz>
# Licence: see LICENCE file for details
####################################################################

host=`hostname`

if [ $host = 'geo102' ] ; then
    # testing server
    wmsurl=http://geo102.fsv.cvut.cz/services/rainwms
    wpsurl=http://geo102.fsv.cvut.cz/services/rainwps
    data=/work/geodata/
    wwwdir=/var/www
else
    # production server
    wmsurl=https://rain1.fsv.cvut.cz:4433/services/wms
    wpsurl=https://rain1.fsv.cvut.cz:4433/services/wps
    data=/opt
    wwwdir=/var/www/html
fi

# WMS
sed "s?#URL#?$wmsurl?g;s?#DATADIR#?$data?g" \
    wms/subdayprecip.map.sed > wms/subdayprecip.map
chown $user:$user wms/subdayprecip.map

# WPS
sed "s?#URL#?$wpsurl?g;s?#DATADIR#?$data?g;s?#HOST#?$host?g;s?#WWWDIR#?$wwwdir?g" \
    wps/pywps.cfg.sed > wps/pywps.cfg
chown $user:$user wps/pywps.cfg

if [ -d /var/www/html/ ] ; then
    cd /var/www/html
else
    cd  /var/www
fi
# output dir for PyWPS
mkdir -p wps/outputs
chown www-data:www-data -R wps
# set up logs for PyWPS
touch /var/log/pywps.log /var/log/pywps_grass_stderr.log
chgrp www-data /var/log/pywps.log /var/log/pywps_grass_stderr.log
chmod g+w /var/log/pywps.log /var/log/pywps_grass_stderr.log

# GRASS database must be writable by www-data user
chgrp www-data /opt/grassdata/subdayprecip
chmod g+w /opt/grassdata/subdayprecip

exit 0
