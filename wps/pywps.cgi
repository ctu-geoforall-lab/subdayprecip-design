#!/bin/sh

SRC_SUBD=/opt/subdayprecip-design
export PYWPS_CFG=${SRC_SUBD}/wps/pywps.cfg
export PYWPS_PROCESSES=${SRC_SUBD}/wps/processes

/opt/pywps/wps.py
