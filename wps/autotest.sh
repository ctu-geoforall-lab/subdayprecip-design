#!/bin/sh
# Test WPS processes
URL="http://localhost:8080"
DATA="@xlink:http://rain.fsv.cvut.cz/geodata/test.gml"
KEY="RAD_I"
RP="N2,N5,N100"
RL="360"
COL="RAD_I"
STYP="E,F"
VALUE="25"
LIMIT="10000"

cd /tmp

echo "**************************************************************"
echo "* d-rain-shp"
echo "**************************************************************"

echo "${URL}/services/wps?service=wps&version=1.0.0&request=Execute&identifier=d-rain-shp&datainputs=input=${DATA};return_period=${RP};rainlength=${RL};area_size=${LIMIT}"
file=`curl \
"${URL}/services/wps?service=wps&version=1.0.0&request=Execute&identifier=d-rain-shp&datainputs=input=${DATA};return_period=${RP};rainlength=${RL};area_size=${LIMIT}" | \
grep '\<wps:Reference' | cut -d'"' -f2`

wget -q $file
echo "RESULT:"
ogrinfo -ro -so /vsizip/`basename $file` subdayprecip_output | grep 'H_N'

exit 0

echo "**************************************************************"
echo "* d-rain-csv"
echo "**************************************************************"

file=`curl \
"${URL}/services/wps?service=wps&version=1.0.0&request=Execute&identifier=d-rain-csv&datainputs=input=${DATA};return_period=${RP};rainlength=${RL};keycolumn=$COL;area_size=${LIMIT}" | \
grep '\<wps:Reference' | cut -d'"' -f2`

wget -q $file
echo "RESULT:"
cat `basename $file`

echo "**************************************************************"
echo "* d-rain-point"
echo "**************************************************************"

value=`curl \
"${URL}/services/wps?service=wps&version=1.0.0&request=Execute&identifier=d-rain-point&datainputs=obs_x=15.11784;obs_y=49.88598;return_period=${RP};rainlength=${RL}" | \
grep "\<wps:LiteralData" | cut -d'>' -f 2 | cut -d'<' -f 1`

echo "RESULT:"
echo $value

echo "**************************************************************"
echo "* d-rain6h-timedist (reduction enabled)"
echo "**************************************************************"

file=`curl \
"${URL}/services/wps?service=wps&version=1.0.0&request=Execute&identifier=d-rain6h-timedist&datainputs=input=${DATA};return_period=${RP};keycolumn=${COL};type=${STYP}" | \
grep '\<wps:Reference' | cut -d'"' -f2`

wget -q $file
echo "RESULT:"
cat `basename $file` |  grep -E '[0-9],[05],'

echo "**************************************************************"
echo "* d-rain6h-timedist (reduction disabled)"
echo "**************************************************************"

file=`curl \
"${URL}/services/wps?service=wps&version=1.0.0&request=Execute&identifier=d-rain6h-timedist&datainputs=input=${DATA};return_period=${RP};keycolumn=${COL};type=${STYP};area_red=false" | \
grep '\<wps:Reference' | cut -d'"' -f2`

wget -q $file
echo "RESULT:"
cat `basename $file` |  grep -E '[0-9],[05],'

echo "**************************************************************"
echo "* raintotal6h-timedist"
echo "**************************************************************"

file=`curl \
"${URL}/services/wps?service=wps&version=1.0.0&request=Execute&identifier=raintotal6h-timedist&datainputs=value=${VALUE};type=${STYP}" | \
grep '\<wps:Reference' | cut -d'"' -f2`

wget -q $file
echo "RESULT:"
cat `basename $file` | head -n2

exit 0
