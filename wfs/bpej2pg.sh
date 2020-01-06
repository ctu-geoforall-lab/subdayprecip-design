#!/bin/bash -e

# TODO (download automatically)
FILE=bpej_202001029879.zip
URL=https://www.spucr.cz/frontend/webroot/uploads/files/2020/01/$FILE
DIR=/tmp
DB=bpej

# createdb $DB
# psql $DB -c 'create extension postgis'
psql $DB -f epsg5514.sql

cd $DIR
if [ ! -f "$FILE" ]; then
    wget $URL
fi

ogr2ogr -f PostgreSQL -overwrite -nln bpej -a_srs EPSG:5514 -nlt MULTIPOLYGON \
	-lco GEOMETRY_NAME=geom \
        PG:dbname=$DB /vsizip/$DIR/$FILE BPEJ_20200102

exit 0
