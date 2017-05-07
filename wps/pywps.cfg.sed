[wps]
encoding=utf-8
title=Rain WPS Server
version=1.0.0
abstract=WPS projektu QJ1520265, vice informaci na http://rain.fsv.cvut.cz/webove-sluzby/ogc-wps/
fees=žádné
constraints=žádné
serveraddress=#URL#
keywords=Rain,GRASS,GIS,WPS
lang=cs-CZ

[provider]
providerName=CVUT v Praze, Fakulta stavebni
individualName=Martin Landa
deliveryPoint=Thakurova 7
positionName=Administrator
city=Praha
postalCode=166 29
country=cz
electronicMailAddress=martin.landa@fsv.cvut.cz
providerSite=#URL#
phoneVoice=+420 224 354 644
phoneFacsimile=False
administrativeArea=False
hoursofservice=0:00-24:00
contactinstructions=E-mail preferován
role=Administrator

[server]
maxoperations=4
maxinputparamlength=1024
maxfilesize=200mb
tempPath=/tmp
processesPath=
outputUrl=https://#HOST#.fsv.cvut.cz:4433/wps/outputs
outputPath=#WWWDIR#/wps/outputs
logFile=/var/log/pywps.log
logLevel=INFO
logfile_module_stderr=/var/log/pywps_grass_stderr.log
#debug=True

[grass]
path=/home/landamar/.grass7/addons/scripts:/opt/grass/dist.x86_64-pc-linux-gnu/bin/:/opt/grass/dist.x86_64-pc-linux-gnu/scripts/:/usr/bin
version=7.2.svn
gui=text
gisbase=/opt/grass/dist.x86_64-pc-linux-gnu
ldLibraryPath=/opt/grass/dist.x86_64-pc-linux-gnu/lib
gisdbase=#DATADIR#/grassdata
pythonPath=/opt/grass/dist.x86_64-pc-linux-gnu/etc/python

[mapserver]
mapserveraddress=https://#HOST#.fsv.cvut.cz:4433/cgi-bin/mapserv
projdatapath=/usr/share/proj
projs=epsg:5514,epsg:4326
