#!/bin/bash

# TODO (download automatically)
FILE=bpej_201901028774.zip
URL=https://www.spucr.cz/frontend/webroot/uploads/files/2019/01/$FILE
DIR=/tmp
DB=bpej

cd $DIR

if [ ! -f "$FILE" ]; then
    wget $URL
fi

# createdb $DB
# psql $DB -c 'create extension postgis'
# psql $DB -f epsg5514.sql

ogr2ogr -f PostgreSQL -overwrite -nln bpej -a_srs EPSG:5514 -nlt MULTIPOLYGON \
        PG:dbname=$DB /vsizip/$DIR/$FILE BPEJ_20190102 

exit 0
