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

sys.path.insert(0, '..')
from base.subdayprecip import SubDayPrecipProcess
from grass.pygrass.modules import Module

class SubDayPrecipCsv(SubDayPrecipProcess):
     def __init__(self):
          super(SubDayPrecipCsv, self).__init__(
               identifier="subdayprecip-design-csv",
               description=u"Vraci vycislene navrhove srazky jako atributova data ve formatu CSV.",
               input_params=['input', 'keycolumn', 'return_period', 'rainlength'],
               output_params=['output_csv']
          )
          
     def export(self):
          self.output_file = '{}/{}.csv'.format(self.output_dir, self.map_name)

          cols = [self.keycolumn]
          for rp in self.return_period:
               cols.append('H_{}T{}'.format(rp, self.rainlength))

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

          return self.output_file
