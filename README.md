# QJ1520265 project (GIS part)

Source code and support files for OGC WMS and WPS developed within
QJ1520265 project, see http://rain.fsv.cvut.cz.

## Deploy Rain WPS server using Docker

### Build image

```
docker-compose build
```

### Run container

Download [BPEJ
data](https://www.spucr.cz/bpej/celostatni-databaze-bpej) from SPU
website. Place a downloaded zip file into `db/data` directory.

```
docker-compose up
```

## Quick test

### Test DB connection

```
PGPASSWD=20rain20 docker-compose exec rain_db psql -U mapserv -d bpej -c 'select count(*) from bpej'
```

# WMS

GetCapabilities:

http://localhost:8080/services/wms?service=wms&request=getcapabilities

GetMap:

http://localhost:8080/services/wms?service=wms&request=getmap&layers=H_N2_24h&version=1.3.0&crs=EPSG:5514&bbox=-907000,-1230000,-429000,-933000&format=image/png&width=1280&height=920

### WFS

GetCapabilities:

http://localhost:8080/services/wfs?service=wfs&request=getcapabilities

GetFeature:

http://localhost:8080/services/wfs?service=wfs&request=getfeature&typename=bpej&maxfeatures=10&version=2.0.0

### WPS

GetCapabilities:

http://localhost:8080/services/wps?service=wps&request=getcapabilities
    
DescribeProcess:

http://localhost:8080/services/wps?service=wps&request=describeprocess&version=2.0.0&identifier=d-rain-shp
    
Execute (POST):

```
wget -q --post-file ./ows/wps/tests/request-d-rain-shp.xml 'http://localhost:8080/services/wps?' -O -
```

### Run tests

```
./ows/wps/tests/autotest.sh
```
