# -*- coding: utf-8 -*-

####################################################################
# QJ1520265 project - source code and support files for OGC WMS and
# WPS implementation http://rain.fsv.cvut.cz
#
# Purpose: WPS processes (DBF)
# Author: Martin Landa <martin.landa fsv.cvut.cz>
# Licence: see LICENCE file for details
####################################################################

from subdayprecip import SubDayPrecipProcess
from grass.pygrass.modules import Module

class Process(SubDayPrecipProcess):
     def __init__(self):
          SubDayPrecipProcess.__init__(self,
                                       identifier="subdayprecip-design-dbf",
                                       description="Service returns DBF file.")
          
          self.output = self.addComplexOutput(identifier = "output",
                                              title = "Output DBF file",
                                              formats = [ {"mimeType":"application/dbase"} ],
                                              asReference = True)
          
     def export(self):
          self.output_file = '{}/{}.dbf'.format(self.output_dir, self.map_name)
          
          Module('v.out.ogr',
                 flags='sm',
                 input=self.map_name,
                 output='{}/{}.shp'.format(self.output_dir, self.map_name),
                 overwrite=True)
          
          self.output.setValue(self.output_file)
          
if __name__ == "__main__":
     process = Process()
     process.execute()
