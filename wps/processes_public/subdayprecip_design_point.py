# -*- coding: utf-8 -*-

####################################################################
# QJ1520265 project - source code and support files for OGC WMS and
# WPS implementation http://rain.fsv.cvut.cz
#
# Purpose: WPS processes (Shapefile)
# Author: Martin Landa <martin.landa fsv.cvut.cz>
# Licence: see LICENCE file for details
####################################################################

import sys
from subprocess import PIPE

sys.path.insert(0, '..')
from base.subdayprecip import SubDayPrecipProcess, LOGGER
from grass.pygrass.modules import Module

class SubDayPrecipPoint(SubDayPrecipProcess):
     def __init__(self):

          super(SubDayPrecipPoint, self).__init__(
               identifier="d-rain-point",
               description=u"Vraci vycislenou navrhovou srazku pro zvoleny bod ve WGS-84.",
               input_params=['obs', 'return_period', 'rainlength'],
               output_params=['output_value']
          )

     def _handler(self, request, response):
          self.rasters = request.inputs['return_period'][0].data.split(',')
          Module('g.region', raster=self.rasters[0])

          map_name = 'obs'
          p = Module('m.proj',
                     coordinates=[request.inputs['obs_x'][0].data,
                                  request.inputs['obs_y'][0].data],
                     proj_in='+init=epsg:4326', proj_out='+init=epsg:5514', stdout_=PIPE)
          x, y, z = p.outputs.stdout.split('|')
          vector_input="1|{}|{}".format(x, y)
          LOGGER.info(vector_input)
          Module('v.in.ascii', input='-', output=map_name,
                 cat=1, x=2, y=3, stdin_=vector_input)
          Module('v.db.addtable', map=map_name)
          LOGGER.debug("Subday computation started")
          Module('r.subdayprecip.design',
                 map=map_name, return_period=self.rasters,
                 rainlength=request.inputs['rainlength'][0].data)
          LOGGER.debug("Subday computation finished")

          p = Module('v.db.select', map=map_name, flags='c', stdout_=PIPE)
          LOGGER.info(p.outputs.stdout)
          response.outputs['output'].data = p.outputs.stdout.split('|')[1].rstrip()

          return response
