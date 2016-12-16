# -*- coding: utf-8 -*-

####################################################################
# QJ1520265 project - source code and support files for OGC WMS and
# WPS implementation http://rain.fsv.cvut.cz
#
# Purpose: WPS processes (Shapefile)
# Author: Martin Landa <martin.landa fsv.cvut.cz>
# Licence: see LICENCE file for details
####################################################################

import os
from zipfile import ZipFile
import logging

from subdayprecip import SubDayPrecipProcess
from grass.pygrass.modules import Module

class Process(SubDayPrecipProcess):
     def __init__(self):
          SubDayPrecipProcess.__init__(self,
                                       identifier="subdayprecip-design-shp",
                                       description="Vrací vyčíslené návrhové srážky jako Esri Shapefile.")
          
          self.output = self.addComplexOutput(identifier = "output",
                                              title = "Výsledný soubor ve formátu Esri Shapefile",
                                              formats = [ {"mimeType":"application/x-zipped-shp"} ],
                                              asReference = True)
          
     def export(self):
          self.output_file = '{}/{}.zip'.format(self.output_dir, self.map_name)
          
          logging.debug("Export started")          
          Module('v.out.ogr',
                 input=self.map_name,
                 flags='sm',
                 output='{}/{}.shp'.format(self.output_dir, self.map_name),
                 overwrite=True)
          
          os.chdir(self.output_dir)
          with ZipFile(self.output_file, 'w') as shpzip:
               shpzip.write('{}.dbf'.format(self.map_name))
               shpzip.write('{}.shp'.format(self.map_name))
               shpzip.write('{}.shx'.format(self.map_name))
               shpzip.write('{}.prj'.format(self.map_name))
          logging.debug("Export finished")
          
          self.output.setValue(self.output_file)
          
if __name__ == "__main__":
     process = Process()
     process.execute()
