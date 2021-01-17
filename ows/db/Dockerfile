FROM ubuntu:18.04

# install requirements
RUN apt-get update && apt-get install --yes software-properties-common gettext-base
RUN add-apt-repository --yes ppa:ubuntugis/ubuntugis-unstable
RUN apt-get update
RUN DEBIAN_FRONTEND="noninteractive" apt-get install --yes postgresql-10 postgresql-10-postgis-3

COPY bpej2pg.sh epsg5514.sql /opt/
CMD /opt/bpej2pg.sh
