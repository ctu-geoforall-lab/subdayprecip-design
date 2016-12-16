#!/bin/sh

if test -z $1 ; then
    echo "specify user"
    exit 1
fi
user="$1"
if test -z $2 ; then
    echo "specify host"
    exit 1
fi
host="$2"
dest=/opt/subdayprecip-design/webapp/publish/rain/
if test -n "$3" ; then
    dest="$3"
fi
host="$2"

basename="webapp"

cd ../qgis
rsync -av --delete data.sqlite webapp.qgs $user@$host:$dest
for f in `ls -t ${basename}_[0-9]* | head -2`; do
    #scp $f $user@$host:$dest
    ext=`echo $f | cut -d'.' -f2`
    cp $f webapp_published.${ext}
done
