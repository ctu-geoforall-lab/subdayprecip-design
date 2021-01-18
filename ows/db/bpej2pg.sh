#!/bin/bash -e

# TODO (download automatically)
FILE=bpej_2021010410908.zip
URL=https://www.spucr.cz/frontend/webroot/uploads/files/2021/01/$FILE
DIR=/data
DB=bpej

createdb $DB
psql $DB -c 'create extension postgis'

cd $DIR
if [ ! -f "$FILE" ]; then
    wget $URL
fi

ogr2ogr -f PostgreSQL -overwrite -nln bpej -a_srs EPSG:5514 -nlt MULTIPOLYGON \
	-lco GEOMETRY_NAME=geom \
        PG:dbname=$DB /vsizip/$DIR/$FILE

exit 0
