FROM postgis/postgis:10-3.1

ADD bpej2pg.sh /docker-entrypoint-initdb.d/
ADD epsg5514.sql /docker-entrypoint-initdb.d/

RUN apt-get update && apt-get install --yes wget gdal-bin
