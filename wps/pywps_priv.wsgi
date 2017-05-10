#!/usr/bin/env python

__author__ = "Martin Landa"

from pywps.app.Service import Service

from processes_private.subdayprecip_design_shapes import SubDayPrecipShapes

processes = [
    SubDayPrecipShapes(),
]

# Service accepts two parameters:
# 1 - list of process instances
# 2 - list of configuration files
application = Service(
    processes,
    ['/opt/subdayprecip-design/wps/pywps.cfg']
)
