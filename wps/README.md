# Rain Web Processing Service

## Deploy Rain WPS server using Docker

### Build image

    docker-compose build
    
### Run container

    docker-compose up
    
### Call WPS

GetCapabilities:

http://localhost:8080/services/wps?service=wps&request=getcapabilities
    
DescribeProcess:

http://localhost:8080/services/wps?service=wps&request=describeprocess&version=2.0.0&identifier=d-rain-shp
    
Execute (POST):

    wget --post-file request.xml 'http://localhost:8080/services/wps?' -O /tmp/response.xml
