#!/usr/bin/env python

__author__ = "Martin Landa"

from pywps.app.Service import Service

from processes_public.subdayprecip_design_shp import SubDayPrecipShp
from processes_public.subdayprecip_design_csv import SubDayPrecipCsv
from processes_public.subdayprecip_design_point import SubDayPrecipPoint

processes = [
    SubDayPrecipShp(),
    SubDayPrecipCsv(),
    SubDayPrecipPoint(),
]

# Service accepts two parameters:
# 1 - list of process instances
# 2 - list of configuration files
application = Service(
    processes,
    ['/opt/subdayprecip-design/wps/pywps.cfg']
)
