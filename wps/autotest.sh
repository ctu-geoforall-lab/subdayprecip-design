#!/bin/sh
# Test WPS processes
DATA="http://rain1.fsv.cvut.cz/data/povodi_i.zip"
KEY="RAD_I"
RP="N2,N5,N100"
RL="360"
COL="RAD_I"
STYP="1,2"

cd /tmp

echo "**************************************************************"
echo "* subdayprecip-design-shp"
echo "**************************************************************"

file=`curl \
"http://rain1.fsv.cvut.cz/services/wps?service=wps&version=1.0.0&request=Execute&identifier=subdayprecip-design-shp&datainputs=\[input=${DATA};return_period=${RP};rainlength=${RL}\]" | \
grep '\<wps:Reference' | cut -d'"' -f2`

wget -q $file
echo "RESULT:"
ogrinfo -ro -so /vsizip/`basename $file` subdayprecip_output | grep 'H_N'

echo "**************************************************************"
echo "* subdayprecip-design-csv"
echo "**************************************************************"

file=`curl \
"http://rain1.fsv.cvut.cz/services/wps?service=wps&version=1.0.0&request=Execute&identifier=subdayprecip-design-csv&datainputs=\[input=${DATA};return_period=${RP};rainlength=${RL};keycolumn=$COL\]" | \
grep '\<wps:Reference' | cut -d'"' -f2`

wget -q $file
echo "RESULT:"
cat `basename $file` | head -n1

echo "**************************************************************"
echo "* subdayprecip-design-point"
echo "**************************************************************"

value=`curl \
"http://rain1.fsv.cvut.cz/services/wps?service=wps&version=1.0.0&request=Execute&identifier=subdayprecip-design-point&datainputs=\[obs_x=15.11784;obs_y=49.88598;return_period=${RP};rainlength=${RL}\]" | \
grep "\<wps:LiteralData" | cut -d'>' -f 2 | cut -d'<' -f 1`

echo "RESULT:"
echo $value

echo "**************************************************************"
echo "* subdayprecip-design-shapes"
echo "**************************************************************"

file=`curl \
"http://rain1.fsv.cvut.cz/services/wpspriv?service=wps&version=1.0.0&request=Execute&identifier=subdayprecip-design-shapes&datainputs=\[input=${DATA};return_period=${RP};keycolumn=${COL};type=${STYP}\]" | \
grep '\<wps:Reference' | cut -d'"' -f2`

wget -q $file
echo "RESULT:"
cat `basename $file` | head -n1

exit 0
