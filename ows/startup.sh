#!/bin/bash

# WPS
envsubst '$NGINX_HOST $NGINX_PORT' < /opt/pywps/pywps.cfg.template > \
         /opt/pywps/pywps.cfg
# WMS
envsubst '$NGINX_HOST $NGINX_PORT' < /opt/mapserv/wms/subdayprecip.map.template > \
         /opt/mapserv/wms/subdayprecip.map

# WFS
envsubst '$NGINX_HOST $NGINX_PORT' < /opt/mapserv/wfs/subdayprecip.map.template > \
         /opt/mapserv/wfs/subdayprecip.map

envsubst '$NGINX_HOST' < /etc/nginx/conf.d/default.conf.template > \
         /etc/nginx/conf.d/default.conf

/etc/init.d/fcgiwrap start && nginx -g 'daemon off;' &

export LD_LIBRARY_PATH=/usr/lib/grass78/lib

# create log file for MapServer otherwise it fails
touch /var/log/mapserv/mapserv.log
chmod 664 /var/log/mapserv/mapserv.log
chgrp www-data /var/log/mapserv/mapserv.log

gunicorn3 -b 127.0.0.1:8081 --workers $((2*`nproc --all`)) \
          --log-syslog  --pythonpath /opt/pywps pywps_app:application

exit 0
