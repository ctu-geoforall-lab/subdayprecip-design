[wps]
encoding=utf-8
title=Rain WPS Server
version=1.0.0
abstract=WPS projektu QJ1520265, vice informaci na http://rain.fsv.cvut.cz/webove-sluzby/wfs
fees=none
constraints=none
serveraddress=#URL#
keywords=GRASS,GIS,WPS
lang=cs-CZ

[provider]
providerName=CVUT v Praze, Fakulta stavebni
individualName=Martin Landa
positionName=GIS Lecturer
deliveryPoint=Thakurova 7
city=Praha
postalCode=166 29
country=cz
electronicMailAddress=martin.landa@fsv.cvut.cz
providerSite=#URL#
phoneVoice=+420 224 354 644
phoneFacsimile=False
administrativeArea=False
hoursofservice=0:00-24:00
contactinstructions=none

[server]
maxoperations=5
maxinputparamlength=1024
maxfilesize=200mb
tempPath=/tmp
processesPath=
outputUrl=http://#HOST#.fsv.cvut.cz/wps/outputs
outputPath=#WWWDIR#/wps/outputs
logFile=/var/log/pywps.log
logLevel=INFO
logfile_module_stderr=/var/log/pywps_grass_stderr.log
#debug=True

[grass]
path=/home/landamar/.grass7/addons/scripts:/opt/grass/dist.x86_64-pc-linux-gnu/bin/:/opt/grass/dist.x86_64-pc-linux-gnu/scripts/:/usr/bin
version=7.1.svn
gui=text
gisbase=/opt/grass/dist.x86_64-pc-linux-gnu
ldLibraryPath=/opt/grass/dist.x86_64-pc-linux-gnu/lib
gisdbase=#DATADIR#/grassdata
pythonPath=/opt/grass/dist.x86_64-pc-linux-gnu/etc/python

[mapserver]
mapserveraddress=http://#HOST#.fsv.cvut.cz/cgi-bin/mapserv
projdatapath=/usr/share/proj
projs=epsg:5514,epsg:4326
