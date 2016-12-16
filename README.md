# subdayprecip-design

Source code and support files for OGC WMS and WPS developed within
QJ1520265 project, see http://rain.fsv.cvut.cz.

How to set up (Debian stable):

    cd /opt
    su
    ./install.sh

Deploy GIS.lab Web App:

    django-admin.py startproject --template=/opt/gislab-web-dev/webgis/conf/project_template/ rain /opt/subdayprecip-design/webapp
    # create /opt/subdayprecip-design/webapp/rain/settings_custom.py
    cd /opt/subdayprecip-design/webapp
    python3 manage.py migrate
    echo "from webgis.viewer.models import GislabUser;GislabUser.objects.create_superuser('user1', 'user1@gislab.io', 'user1')" | python3 ./manage.py shell

    chgrp www-data webapp/
    chgrp www-data webapp/webgis.sqlite3
    chmod g+w webapp/
    chmod g+w webapp/webgis.sqlite3
	