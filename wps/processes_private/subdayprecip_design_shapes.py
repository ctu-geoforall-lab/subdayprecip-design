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
import sys
import logging
import types
import time
from zipfile import ZipFile

sys.path.insert(0, '..')
from base.subdayprecip import SubDayPrecipProcess
import grass.script as gscript # TODO: replace by pyGRASS

class SubDayPrecipShapes(SubDayPrecipProcess):
     def __init__(self):
          super(SubDayPrecipShapes, self).__init__(
               identifier="d-rain-timedist",
               description=u"Vraci tvary navrhovych srazek v tabulkove forme s pevne stanovenou delkou srazky 6 hodin.",
               input_params=['input', 'keycolumn', 'return_period', 'type'],
               output_params=['output_shapes']
          )

          self.mapset = 'rl360'
          self.sep = ','
          self.rainlength = '360'

     def export(self):
          logging.debug("Shapes computation started")
          start = time.time()

          gisenv = gscript.gisenv()

          # query shapes
          sql = 'select min'
          for stype in self.shapetype:
               sql += ',typ{}'.format(stype)
          sql += ' from tvary'
          shapes = gscript.db_select(sql=sql, driver='sqlite',
                                     database=os.path.join(
                                          gisenv['GISDBASE'], gisenv['LOCATION_NAME'],
                                          self.mapset, 'sqlite/sqlite.db')
          )

          # query map attributes
          columns = map(lambda x: 'H_{}T{}'.format(x, self.rainlength), self.return_period)
          columns.insert(0, self.keycolumn)
          data = gscript.vector_db_select(map=self.map_name, columns=','.join(columns))

          # export csv
          self.output_file = '{}/{}.csv'.format(self.output_dir, self.map_name)
          with open(self.output_file, 'w') as fd:
               self.export_csv(fd, data, shapes)
          # output_zfile = self.output_file + '.zip'
          # os.chdir(self.output_dir)
          # with ZipFile(output_zfile, 'w') as fzip:
          #      fzip.write('{}'.format(os.path.basename(self.output_file)))
          # self.output_csv.setValue(output_zfile)

          # export png (graph)
          ### TODO

          logging.info("Shapes calculated successfully: {} sec".format(time.time() - start))
          
          return self.output_file
     
     def export_csv(self, fd, data, shapes):
          # write header
          fd.write('{key}{sep}CAS_min'.format(key=self.keycolumn, sep=self.sep))
          for stype in self.shapetype:
               for rp in self.return_period:
                    fd.write('{sep}H_{rast}T{rl}TYP{stype}'.format(
                              sep=self.sep, stype=stype, rast=rp, rl=self.rainlength)
                    ) 
          fd.write('\r\n')

          # process features
          for fid, attrib in data['values'].iteritems():
               for s in shapes:
                    time = s[0]
                    timeshapes = s[1:]
                    fd.write('{fid}{sep}{time}'.format(fid=attrib[0], time=time, sep=self.sep))
                    for val in attrib[1:]:
                         for shape in timeshapes:
                              fd.write('{sep}{val}'.format(sep=self.sep,
                                                           val=(float(val)*float(shape))/100
                              ))
                    fd.write('\r\n')

if __name__ == "__main__":
     process = Process()
     process.execute()
