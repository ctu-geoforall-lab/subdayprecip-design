[server]
encoding=utf-8
language=cs-CZ
parallelprocesses=4
maxrequestsize=1024
outputurl=https://#HOST#.fsv.cvut.cz:4433/wps/outputs
outputpath=#WWWDIR#/wps/outputs

[metadata:main]
identification_title=Rain WPS Server
identification_abstract=WPS projektu QJ1520265, vice informaci na http://rain.fsv.cvut.cz/webove-sluzby/ogc-wps/
identification_keywords=Rain,GRASS,GIS,WPS
provider_url=#URL#
provider_name=CVUT v Praze, Fakulta stavebni
contact_name=Martin Landa
contact_address=Thakurova 7
contact_role=author
contact_city=Praha
contact_postalcode=166 29
contact_country=cz
contact_email=martin.landa@fsv.cvut.cz
contact_phone=+420 224 354 644
contact_hours=0:00-24:00

[logging]
file=/var/log/pywps.log
level=INFO

[grass]
gisbase=/opt/grass/dist.x86_64-pc-linux-gnu
