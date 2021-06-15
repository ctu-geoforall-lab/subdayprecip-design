#!/usr/bin/env python3

__author__ = "Martin Landa"

import os
import sys
from pywps.app.Service import Service

os.environ['GISBASE'] = '/usr/lib/grass78' 
sys.path.append(os.path.join(os.environ["GISBASE"], "etc", "python"))

from processes.subdayprecip_design_shp import SubDayPrecipShp
from processes.subdayprecip_design_csv import SubDayPrecipCsv
from processes.subdayprecip_design_point import SubDayPrecipPoint
from processes.subdayprecip_design_shapes import SubDayPrecipShapes
from processes.subdayprecip_design_shapes_total import SubDayPrecipShapesTotal
from processes.granularity import GranularityProcess

processes = [
    SubDayPrecipShp(),
    SubDayPrecipCsv(),
    SubDayPrecipPoint(),
    SubDayPrecipShapes(),
    SubDayPrecipShapesTotal(),
    GranularityProcess()
]

application = Service(
    processes,
    ['/opt/pywps/pywps.cfg']
)
