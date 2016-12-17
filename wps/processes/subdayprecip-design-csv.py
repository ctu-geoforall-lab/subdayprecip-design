# -*- coding: utf-8 -*-

####################################################################
# QJ1520265 project - source code and support files for OGC WMS and
# WPS implementation http://rain.fsv.cvut.cz
#
# Purpose: WPS processes (CSV)
# Author: Martin Landa <martin.landa fsv.cvut.cz>
# Licence: see LICENCE file for details
####################################################################

import types

from subprocess import PIPE
from subdayprecip import SubDayPrecipProcess
from grass.pygrass.modules import Module

class Process(SubDayPrecipProcess):
     def __init__(self):
          SubDayPrecipProcess.__init__(self,
                                       identifier="subdayprecip-design-csv",
                                       description="Vrací vyčíslené návrhové srážky jako atributová data ve formátu CSV.")
          
          self.keycolumn=self.addLiteralInput(identifier = "column",
                                              title = "Klíčový atribut vstupních dat",
                                              type = types.StringType)

          self.output = self.addComplexOutput(identifier = "output",
                                              title = "Výsledek ve formátu CSV",
                                              formats = [ {"mimeType":"application/csv"} ],
                                              asReference = True)
          
     def export(self):
          self.output_file = '{}/{}.csv'.format(self.output_dir, self.map_name)

          cols = [self.keycolumn.getValue()]

          # check if key columns exists
          map_cols = Module('db.columns', table=self.map_name, stdout_=PIPE).outputs.stdout.splitlines()
          if cols[0] not in map_cols:
               raise StandardError("Key column ({}) not found in input attribute table ({})".format(
                         cols[0], ','.join(map_cols)
               ))

          rasters = self.raster.getValue().split(',')
          rainlength = self.rainlength.getValue()
          for rast in rasters:
               cols.append('{}_{}'.format(rast, rainlength))

          Module('v.db.select',
                 map=self.map_name,
                 separator='comma',
                 columns=cols,
                 file=self.output_file)
          # Module('v.out.ogr',
          #        flags='sm',
          #        input=self.map_name,
          #        output=self.output_file,
          #        overwrite=True, format='CSV')
          
          self.output.setValue(self.output_file)
          
if __name__ == "__main__":
     process = Process()
     process.execute()
