[server]
encoding=utf-8
language=cs-CZ
parallelprocesses=4
maxrequestsize=10mb
maxsingleinputsize=10mb
outputurl=https://#HOST#.fsv.cvut.cz/wps/outputs/
outputpath=#WWWDIR#/wps/outputs
url=#URL#

[metadata:main]
identification_title=Rain WPS Server
identification_abstract=WPS projektu QJ1520265, vice informaci na http://rain.fsv.cvut.cz/webove-sluzby/ogc-wps/
identification_keywords=Rain,GRASS,GIS,WPS
provider_url=http://rain.fsv.cvut.cz
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
contact_instructions=Preferovan e-mail

[logging]
file=/var/log/pywps.log
level=INFO

[grass]
gisbase=/usr/local/grass76
