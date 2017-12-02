#!/usr/bin/env python

__author__ = "Martin Landa"

from pywps.app.Service import Service

from processes_public.subdayprecip_design_shp import SubDayPrecipShp
from processes_public.subdayprecip_design_csv import SubDayPrecipCsv
from processes_public.subdayprecip_design_point import SubDayPrecipPoint

from processes_private.subdayprecip_design_shapes import SubDayPrecipShapes
from processes_private.subdayprecip_design_shapes_total import SubDayPrecipShapesTotal

processes = [
    SubDayPrecipShp(),
    SubDayPrecipCsv(),
    SubDayPrecipPoint(),
    SubDayPrecipShapes(),
    SubDayPrecipShapesTotal(),
]

# Service accepts two parameters:
# 1 - list of process instances
# 2 - list of configuration files
application = Service(
    processes,
    ['/opt/subdayprecip-design/wps/pywps.cfg']
)
