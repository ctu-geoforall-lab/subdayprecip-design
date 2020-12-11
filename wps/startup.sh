#!/bin/bash

envsubst '$NGINX_HOST $NGINX_PORT' < /opt/pywps/pywps.cfg.template > \
         /opt/pywps/pywps.cfg

envsubst '$NGINX_HOST' < /etc/nginx/conf.d/default.conf.template > \
         /etc/nginx/conf.d/default.conf

nginx -g 'daemon off;' &

export LD_LIBRARY_PATH=/usr/lib/grass78/lib
export PATH=/usr/lib/grass78/bin:/usr/lib/grass78/scripts:$PATH

gunicorn3 -b 127.0.0.1:8081 --workers $((2*`nproc --all`)) \
          --log-syslog  --pythonpath /opt/pywps pywps_app:application

exit 0
