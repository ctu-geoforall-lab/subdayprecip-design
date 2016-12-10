# -*- coding: utf-8 -*-

####################################################################
# QJ1520265 project - source code and support files for OGC WMS and
# WPS implementation http://rain.fsv.cvut.cz
#
# Purpose: WPS processes (CSV)
# Author: Martin Landa <martin.landa fsv.cvut.cz>
# Licence: see LICENCE file for details
####################################################################

from subdayprecip import SubDayPrecipProcess
from grass.pygrass.modules import Module

class Process(SubDayPrecipProcess):
     def __init__(self):
          SubDayPrecipProcess.__init__(self,
                                       identifier="subdayprecip-design-csv",
                                       description="Service returns CSV file.")
          
          self.output = self.addComplexOutput(identifier = "output",
                                              title = "Output CSV file",
                                              formats = [ {"mimeType":"application/csv"} ],
                                              asReference = True)
          
     def export(self):
          self.output_file = '{}/{}.csv'.format(self.output_dir, self.map_name)
          
          Module('v.out.ogr',
                 input=self.map_name,
                 output=self.output_file,
                 overwrite=True, format='CSV')
          
          self.output.setValue(self.output_file)
          
if __name__ == "__main__":
     process = Process()
     process.execute()
