#!/bin/sh
# Test WPS processes
DATA="https://rain1.fsv.cvut.cz/data/povodi_iv.zip"
RP="N2,N5,N10,N20,N50,N100"
RL="360"

echo "**************************************************************"
echo "* d-rain-shp"
echo "**************************************************************"

file=`curl \
"https://rain1.fsv.cvut.cz/services/wps?service=wps&version=1.0.0&request=Execute&identifier=d-rain-shp&datainputs=input=${DATA};return_period=${RP};rainlength=${RL}" | \
grep '\<wps:Reference' | cut -d'"' -f2`

wget -q $file
filename=`basename $file`
mkdir -p data
unzip -q -d data $filename
rm -f $filename

echo "RESULT:"
ogrinfo -ro -so data/subdayprecip_output.shp subdayprecip_output | grep 'H_N'

exit 0
