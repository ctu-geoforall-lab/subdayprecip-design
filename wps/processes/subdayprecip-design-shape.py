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
import logging

from subdayprecip import SubDayPrecipProcess
import grass.script as gscript # TODO: replace by pyGRASS

class Process(SubDayPrecipProcess):
     def __init__(self):
          SubDayPrecipProcess.__init__(self,
                                       identifier="subdayprecip-design-shapes",
                                       description="Service returns shapes (TODO: explain better)",
                                       skip_input=True)

          self.mapset = 'rl360'
          self.shapetype = [5, 6]
          self.sep = ','

          self.output = self.addComplexOutput(identifier = "output",
                                              title = "Output CSV file",
                                              formats = [ {"mimeType":"application/csv"} ],
                                              asReference = True)

     def execute(self):
          map_name = 'povodi_iii@{}'.format(self.mapset) # TODO: input
          # TODO: self.output_dir already defined in superclass
          self.output_dir = os.path.join('/tmp', '{}_{}'.format(map_name, os.getpid()))
          os.mkdir(self.output_dir)

          rasters = self.raster.getValue().split(',')
          gisenv = gscript.gisenv()

          # query shapes
          sql = 'select min'
          for stype in self.shapetype:
               sql += ',typ{}'.format(stype)
          sql += ' from tvary'
          shapes = gscript.db_select(sql=sql, driver='sqlite',
                                     database=os.path.join(gisenv['GISDBASE'], gisenv['LOCATION_NAME'],
                                                           self.mapset, 'sqlite/sqlite.db'))

          # query map attributes
          columns = map(lambda x: '{}_{}'.format(x.lower(), self.rainlength.getValue()), rasters)
          data = gscript.vector_db_select(map=map_name, columns=','.join(columns))

          self.output_file = '{}/{}.csv'.format(self.output_dir, map_name)
          with open(self.output_file, 'w') as fd:
               self.export(fd, rasters, data, shapes)
          self.output.setValue(self.output_file)

     def export(self, fd, rasters, data, shapes):
          # write header
          fd.write('fid{sep}T'.format(sep=self.sep))
          for stype in self.shapetype:
               for rast in rasters:
                    fd.write('{sep}T_{stype}_{rast}'.format(
                              sep=self.sep, stype=stype, rast=rast[2:]) # skip H_
                    ) 
          fd.write('\r\n')

          # process features
          for fid, attrib in data['values'].iteritems():
               for s in shapes:
                    time = s[0]
                    timeshapes = s[1:]
                    fd.write('{fid}{sep}{time}'.format(fid=fid, time=time, sep=self.sep))
                    for val in attrib:
                         for shape in timeshapes:
                              fd.write('{sep}{val}'.format(sep=self.sep, val=float(val)*float(shape)))
                    fd.write('\r\n')

if __name__ == "__main__":
     process = Process()
     process.execute()
