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
from subdayprecip_design_shapes import SubDayPrecipShapesBase

import grass.script as gscript # TODO: replace by pyGRASS

class SubDayPrecipShapesTotal(SubDayPrecipShapesBase, SubDayPrecipProcess):
     def __init__(self):
          SubDayPrecipProcess.__init__(self,
               identifier="raintotal-timedist",
               description=u"Vraci tvary navrhovych srazek v tabulkove forme s pevne stanovenou delkou srazky 6 hodin. (TODO: zmenit)",
               input_params=['value', 'type'],
               output_params=['output_shapes']
          )
          SubDayPrecipShapesBase.__init__(self)

     def export_csv(self, fd, shapes, data=None):
          # write header
          fd.write('CAS_min')
          for stype in self.shapetype:
               fd.write('{sep}T{rl}TYP{stype}'.format(
                    sep=self.sep, stype=stype, rl=self.rainlength)
               )
          fd.write('\r\n')

          # process features
          for s in shapes:
               time = s[0]
               timeshapes = s[1:]
               fd.write('{time}'.format(time=time, sep=self.sep))
               for shape in timeshapes:
                    fd.write('{sep}{val}'.format(sep=self.sep,
                                                 val=(float(self.value)*float(shape))/100)
                    )
               fd.write('\r\n')

if __name__ == "__main__":
     process = Process()
     process.execute()
