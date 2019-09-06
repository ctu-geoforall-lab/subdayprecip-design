#!/bin/bash

envsubst '$NGINX_HOST' < /etc/nginx/conf.d/gisquick.template > /etc/nginx/conf.d/gisquick.conf && nginx -g 'daemon off;' &
gunicorn -b 127.0.0.1:8081  --workers $((2*`nproc --all`)) --log-syslog  --pythonpath /opt/subdayprecip-design/wps pywps_app:application

exit 0
