# -*- coding: utf-8 -*-

####################################################################
# QJ1520265 project - source code and support files for OGC WMS and
# WPS implementation http://rain.fsv.cvut.cz
#
# Purpose: WPS processes (CSV)
# Author: Martin Landa <martin.landa fsv.cvut.cz>
# Licence: see LICENCE file for details
####################################################################

import sys
import types

sys.path.insert(0, '..')
from base.subdayprecip import SubDayPrecipProcess
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
          rainlength = self.rainlength.getValue()
          for rp in self.return_period.getValue().split(','):
               cols.append('H_{}_T{}_mm'.format(rp, rainlength))

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
