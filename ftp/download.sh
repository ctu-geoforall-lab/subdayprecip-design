#!/bin/bash -e

# ./download.sh username password target

if test -z "$1"; then
    echo "username missing"
    echo "./download.sh username password target"
    exit 1
fi
if test -z "$2"; then
    echo "password missing"
    echo "./download.sh username password target"
    exit 1
fi
if test -z "$3"; then
    echo "target missing"
    echo "./download.sh username password target"
    exit 1
fi

mkdir -p "$3"
cd "$3"

wget --mirror --continue --no-host-directories \
     --user=$1 --password=$2 ftp://rain.fsv.cvut.cz 2>"$3/download.log"

exit 0
