FROM gisquick/nginx

RUN apt update

# Gunicor
RUN apt -y install gunicorn

# GRASS GIS
RUN echo "deb-src http://httpredir.debian.org/debian jessie main" >> /etc/apt/sources.list
RUN apt-get update
RUN apt-get -y build-dep grass
RUN apt-get -y install git python-pip python-pyproj python-sqlalchemy python-lxml python-dateutil python-numpy subversion
RUN cd /tmp && git clone https://github.com/osgeo/grass.git
RUN cd /tmp/grass && git checkout releasebranch_7_6
RUN cd /tmp/grass && ./configure --with-freetype-includes=/usr/include/freetype2/ --without-zstd
RUN cd /tmp/grass && make && make install
RUN rm -rf /tmp/grass
RUN echo "g.extension -s ext=r.subdayprecip.design" > /tmp/ext.sh && chmod +x /tmp/ext.sh
RUN grass76 --tmp-location EPSG:5514 --exec sh /tmp/ext.sh && rm /tmp/ext.sh
RUN echo "/usr/local/grass76/lib" > /etc/ld.so.conf.d/grass.conf
RUN ldconfig

# PyWPS
RUN pip install pywps==4.0.0 python-magic
RUN mkdir -p /var/www/wps/outputs

# Fix EPSG 5514
RUN echo "<5514> +proj=krovak +lat_0=49.5 +lon_0=24.83333333333333 +alpha=30.28813972222222 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +towgs84=570.8,85.7,462.8,4.998,1.587,5.261,3.56 +units=m +no_defs" >> /usr/share/proj/epsg

# Nginx template
COPY gisquick.template /etc/nginx/conf.d/

# Run PyWPS Gunicorn
COPY startup.sh /opt/startup.sh
CMD /opt/startup.sh
# CMD ["gunicorn", "--preload", "-b", "127.0.0.1:8081", "--workers", "4", "--log-syslog",  "--pythonpath", "/opt/subdayprecip-design/wps", "pywps_app:application"]