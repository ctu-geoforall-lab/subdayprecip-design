# FROM mundialis/grass-py3-pdal:stable-ubuntu
FROM ubuntu:18.04

# install requirements
COPY requirements.txt /tmp/requirements.txt
RUN apt-get update && apt-get install --yes software-properties-common gettext-base
RUN add-apt-repository --yes ppa:ubuntugis/ubuntugis-unstable
RUN apt-get update && apt-get install --yes python3-pip python3-pyproj gunicorn3 nginx grass-core grass-doc grass-dev
RUN python3 -m pip install -r /tmp/requirements.txt

# set up pyWPS
RUN mkdir -p /var/www/wps/output
RUN mkdir -p /var/log/pypws
RUN rm /etc/nginx/sites-enabled/default

# install GRASS extensions
RUN grass --tmp-location EPSG:5514 --exec g.extension -s r.subdayprecip.design

# run pyWPS Gunicorn
COPY startup.sh /opt/startup.sh
CMD /opt/startup.sh
