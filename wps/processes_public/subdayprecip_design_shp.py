# -*- coding: utf-8 -*-

####################################################################
# QJ1520265 project - source code and support files for OGC WMS and
# WPS implementation http://rain.fsv.cvut.cz
#
# Purpose: WPS processes (Shapefile)
# Author: Martin Landa <martin.landa fsv.cvut.cz>
# Licence: see LICENCE file for details
####################################################################

__author__ = "Martin Landa"

import os
import sys
import logging
from zipfile import ZipFile

sys.path.insert(0, '..')
from base.subdayprecip import SubDayPrecipProcess
from grass.pygrass.modules import Module

class SubDayPrecipShp(SubDayPrecipProcess):
     def __init__(self):
          super(SubDayPrecipShp, self).__init__(
               identifier="subdayprecip-design-shp",
               description="Vraci vycislene navrhove srazky jako vektorova data ve formatu Esri Shapefile.",
               input_params=['input', 'return_period', 'rainlength'],
               output_params=['output_shp']
          )
          
     def export(self):
          self.output_file = '{}/{}.zip'.format(self.output_dir, self.map_name)
          
          logging.debug("Export started")          
          Module('v.out.ogr',
                 input=self.map_name,
                 flags='sme',
                 output='{}/{}.shp'.format(self.output_dir, self.map_name),
                 overwrite=True)
          
          os.chdir(self.output_dir)
          with ZipFile(self.output_file, 'w') as shpzip:
               shpzip.write('{}.dbf'.format(self.map_name))
               shpzip.write('{}.shp'.format(self.map_name))
               shpzip.write('{}.shx'.format(self.map_name))
               shpzip.write('{}.prj'.format(self.map_name))
          logging.debug("Export finished")

          return self.output_file
