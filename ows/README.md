# Rain Demo Web Processing Service

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

## Test WPS Requests

GetCapabilities:

http://localhost:8080/services/wps?service=wps&request=getcapabilities
    
DescribeProcess:

http://localhost:8080/services/wps?service=wps&request=describeprocess&version=2.0.0&identifier=d-rain-shp
    
Execute (POST):

```
wget -q --post-file request-d-rain-shp.xml 'http://localhost:8080/services/wps?' -O -
```

## Run tests

```
./autotests.sh
```
