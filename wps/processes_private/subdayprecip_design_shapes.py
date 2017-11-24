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
from base.subdayprecip import SubDayPrecipProcess, LOGGER
import grass.script as gscript # TODO: replace by pyGRASS

class SubDayPrecipShapesBase(object):
     def __init__(self):
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

          if self.identifier == 'd-rain-timedist':
               # query map attributes
               columns = map(lambda x: 'H_{}T{}'.format(x, self.rainlength), self.return_period)
               columns.insert(0, self.keycolumn)
               data = gscript.vector_db_select(map=self.map_name, columns=','.join(columns))
          else:
               data = None

          # export csv
          self.output_file = '{}/{}.csv'.format(self.output_dir, self.identifier)
          with open(self.output_file, 'w') as fd:
               self.export_csv(fd, shapes, data)
          # output_zfile = self.output_file + '.zip'
          # os.chdir(self.output_dir)
          # with ZipFile(output_zfile, 'w') as fzip:
          #      fzip.write('{}'.format(os.path.basename(self.output_file)))
          # self.output_csv.setValue(output_zfile)

          # export png (graph)
          ### TODO

          logging.info("Shapes calculated successfully: {} sec".format(time.time() - start))
          
          return self.output_file
     
class SubDayPrecipShapes(SubDayPrecipShapesBase, SubDayPrecipProcess):
     def __init__(self):
          SubDayPrecipProcess.__init__(self,
               identifier="d-rain-timedist",
               description=u"Vraci tvary navrhovych srazek v tabulkove forme s pevne stanovenou delkou srazky 6 hodin.",
               input_params=['input', 'keycolumn', 'return_period', 'type'],
               output_params=['output_shapes']
          )
          SubDayPrecipShapesBase.__init__(self)

     def _compute_timeshapes_perc(self):
          def type_convert(type_num):
               _types = { '1' : 'F',
                          '2' : 'E',
                          '3' : 'D',
                          '4' : 'C',
                          '5' : 'B',
                          '6' : 'A'
               }
               return _types[type_num]

          # filename syntax: sjtsk_zastoupeni_shluku_cA_100yr_perc
          columns = []
          for stype in self.shapetype:
               type_string = type_convert(stype)
               for rp in self.return_period:
                    n = rp.lstrip('N')
                    columns.append('c{types}_{n}yr_perc'.format(
                         types=type_string, n=n
                    ))
                    map_name = 'sjtsk_zastoupeni_shluku_c{types}_{n}yr_perc@{ms}'.format(
                         types=type_string, n=n, ms=self.mapset
                    )
                    gscript.run_command('v.rast.stats', map=self.map_name, raster=map_name,
                                        method='average', column_prefix=columns[-1]
                    )

          return gscript.vector_db_select(
               map=self.map_name,
               columns=','.join(map(lambda x: '{}_average'.format(x), columns))
          )

     def export_csv(self, fd, shapes, data):
          nl = '\r\n'
          # write header
          fd.write('{key}{sep}CAS_min'.format(key=self.keycolumn, sep=self.sep))
          for stype in self.shapetype:
               for rp in self.return_period:
                    fd.write('{sep}H_{rast}T{rl}TYP{stype}_mm'.format(
                              sep=self.sep, stype=stype, rast=rp, rl=self.rainlength)
                    )
          for stype in self.shapetype:
               for rp in self.return_period:
                    fd.write('{sep}H_{rast}T{rl}TYP{stype}_%'.format(
                         sep=self.sep, stype=stype, rast=rp, rl=self.rainlength)
                    )
          fd.write(nl)

          # compute timeshape percentage
          data_perc = self._compute_timeshapes_perc()

          # process features
          for fid, attrib in data['values'].iteritems():
               fd.write('{fid}{sep}0{seps}'.format(
                    fid=attrib[0], sep=self.sep,
                    seps=self.sep * len(attrib[1:] * len(self.shapetype))
               ))
               for val in data_perc['values'][fid]:
                    fd.write('{sep}{val:.1f}'.format(
                         sep=self.sep, val=float(val)
                    ))
               fd.write(nl)
               for s in shapes:
                    time = s[0]
                    timeshapes = s[1:]
                    fd.write('{fid}{sep}{time}'.format(fid=attrib[0], time=time, sep=self.sep))
                    for val in attrib[1:]:
                         for shape in timeshapes:
                              fd.write('{sep}{val:.2f}'.format(sep=self.sep,
                                                           val=(float(val)*float(shape))/100
                              ))
                    fd.write(nl)

if __name__ == "__main__":
     process = Process()
     process.execute()
