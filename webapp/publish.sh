#!/bin/sh

if test -z $1 ; then
    echo "specify user"
    exit 1
fi
user="$1"
if test -z $2 ; then
    echo "specify user"
    exit 1
fi
host="$2"

basename="webapp"

for f in `ls -t ${basename}_* | head -2`; do
    scp $f $user@$host:/opt/subdayprecip-design/webapp/publish/rain/
done
