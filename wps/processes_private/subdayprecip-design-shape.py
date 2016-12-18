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

class Process(SubDayPrecipProcess):
     def __init__(self):
          SubDayPrecipProcess.__init__(self,
                                       identifier="subdayprecip-design-shape",
                                       description="Vrací tvary návrhových srážek v tabulkové formě s pevně stanovenou délkou srážky 6 hodin.",
                                       skip = ['rainlength'])

          self.mapset = 'rl360'
          self.shapetype = range(1, 7)
          self.sep = ','
          self.rainlength_value = '360'

          self.keycolumn=self.addLiteralInput(identifier = "column",
                                              title = "Klíčový atribut vstupních dat",
                                              type = types.StringType)

          self.output_csv = self.addComplexOutput(identifier = "output_csv",
                                                  title = "Hodnoty tvaru návrhových srážek ve formátu CSV",
                                                  formats = [ {"mimeType":"application/csv"} ],
                                                  asReference = True)

          # self.output_png = self.addComplexOutput(identifier = "output_png",
          #                                       title = "Tvar návrhových srážek jako graf ve formátu PNG",
          #                                       formats = [ {"mimeType":"image/png"} ],
          #                                       asReference = True)

     def export(self):
          logging.debug("Shapes computation started")
          start = time.time()

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
          columns = map(lambda x: '{}_{}'.format(x.lower(), self.rainlength_value), rasters)
          columns.insert(0, self.keycolumn.getValue())
          data = gscript.vector_db_select(map=self.map_name, columns=','.join(columns))

          # export csv
          self.output_file = '{}/{}.csv'.format(self.output_dir, self.map_name)
          with open(self.output_file, 'w') as fd:
               self.export_csv(fd, rasters, data, shapes)
          # output_zfile = self.output_file + '.zip'
          # os.chdir(self.output_dir)
          # with ZipFile(output_zfile, 'w') as fzip:
          #      fzip.write('{}'.format(os.path.basename(self.output_file)))
          # self.output_csv.setValue(output_zfile)
          self.output_csv.setValue(self.output_file)

          # export png (graph)
          ### TODO

          logging.info("Shapes calculated successfully: {} sec".format(time.time() - start))

     def export_csv(self, fd, rasters, data, shapes):
          keycolumn = self.keycolumn.getValue()
          # write header
          fd.write('{key}{sep}cas_min'.format(key=keycolumn, sep=self.sep))
          for stype in self.shapetype:
               for rast in rasters:
                    fd.write('{sep}typ_{stype}_{rast}_mm'.format(
                              sep=self.sep, stype=stype, rast=rast[2:]) # skip H_
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
