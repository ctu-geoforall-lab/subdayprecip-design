# -*- coding: utf-8 -*-

####################################################################
# QJ1520265 project - source code and support files for OGC WMS and
# WPS implementation http://rain.fsv.cvut.cz
#
# Purpose: WPS processes (base class)
# Author: Martin Landa <martin.landa fsv.cvut.cz>
# Licence: see LICENCE file for details
####################################################################

import os
import sys

import time
import types
import shutil
import logging
import magic
from subprocess import PIPE

os.environ['GISBASE'] = '/opt/grass/dist.x86_64-pc-linux-gnu'
sys.path.append(os.path.join(os.environ["GISBASE"], "etc", "python"))
logging.info(sys.path)
from grass.pygrass.modules import Module
from grass.exceptions import CalledModuleError
from pywps.Process import WPSProcess

class SubDayPrecipProcess(WPSProcess):
     def __init__(self, identifier, description, location='subdayprecip', skip=[]):
          WPSProcess.__init__(self,
                              identifier=identifier,
                              version="0.1",
                              title="Návrhová srážka pro zvolenou lokalitu. " + description,
                              abstract="Počítá návrhovou srážku pro zvolenou lokalitu s využitím nástroje GRASS GIS r.subdayprecip.design. "
                              "Více informací na http://rain.fsv.cvut.cz/nastroje/r.subdayprecip.design",
                              grassLocation=location, storeSupported = True, statusSupported = True)

          if 'input' not in skip:
               self.input = self.addComplexInput(identifier = "input",
                                                 title = "Vstupní bodová nebo polygonová vektorová data",
                                                 formats = [ {"mimeType":"text/xml",
                                                              "encoding":"utf-8",
                                                              "schema":"http://schemas.opengis.net/gml/3.2.1/gml.xsd"} ],
                                                 minOccurs=0)
          
          self.return_period = self.addLiteralInput(identifier = "return_period",
                                                    title = "Doby opakování",
                                                    type = types.StringType,
                                                    default = "N2,N5,N10,N20,N50,N100")

          self.rainlength_value = None
          if 'rainlength' not in skip:
               self.rainlength = self.addLiteralInput(identifier = "rainlength",
                                                      title = "Délka srážky v minutách",
                                                      type = types.IntType)

          self.output = None # to be defined by descendant
          self.output_dir = None
          
          os.environ['GRASS_SKIP_MAPSET_OWNER_CHECK'] = '1'
          os.environ['HOME'] = '/tmp' # needed by G_home()
          
     def __del__(self):
          if self.output_dir:
               shutil.rmtree(self.output_dir)

     def execute(self):
          if not self.rainlength_value:
               self.rainlength_value = self.rainlength.getValue()
          if self.input:
               self.map_name = self.import_data()
          else:
               self.map_name = self.copy()

          if hasattr(self, 'keycolumn'):
               self.check_keycolumn(self.keycolumn.getValue())

          self.rasters = self.return_period.getValue().split(',')

          self.output_dir = os.path.join('/tmp', '{}_{}'.format(self.map_name, os.getpid()))
          os.mkdir(self.output_dir)

          Module('g.region', raster=self.rasters[0])
          logging.debug("Subday computation started")
          start = time.time()
          Module('r.subdayprecip.design',
                 map=self.map_name, return_period=self.rasters, rainlength=self.rainlength_value)
          logging.info("Subday computation finished: {} sec".format(time.time() - start))
          
          self.export()
         
     def check_keycolumn(self, keycol):
          # check if key columns exists
          map_cols = Module('db.columns', table=self.map_name, stdout_=PIPE).outputs.stdout.splitlines()
          if keycol not in map_cols:
               raise StandardError("Key column ({}) not found in input attribute table ({})".format(
                         keycol, ','.join(map_cols)
               ))
          
     def import_data(self, link_only=False):
          map_name = 'subdayprecip_output'
          input_data = self.input.getValue()

          # guess mine type
          m = magic.open(magic.MAGIC_MIME)
          m.load()
          mime = m.file(input_data)
          logging.debug('Input ({}) mine type: {}'.format(input_data, mime))
          if 'gzip' in mime:
               input_data = '/vsigzip/' + input_data
          elif 'zip' in mime:
               os.rename(input_data, input_data + '.zip') # GDAL requires zip extension
               input_data = '/vsizip/' + input_data + '.zip'

          # link or import ?
          module_in_args = {}
          if link_only:
               module_in = 'v.external'
               module_in_args['input'] = input_data
               module_in_args['layer'] = 'basin' # TODO: fix it!
          else:
               module_in = 'v.in.ogr'
               module_in_args['input'] = input_data
               # skip projection check
               module_in_args['flags'] = 'o'
          logging.debug("Import started ({})".format(input_data))
          start = time.time()
          try:
               Module(module_in,
                      output=map_name,
                      overwrite=True,
                      **module_in_args)
          except CalledModuleError as e:
               raise Exception("Unable to import input vector data: {}".format(e))
          
          logging.info("Input data imported ({}): {} sec".format(module_in, time.time() - start))
          
          return map_name
     
     def copy(self):
          map_name = self.input.getValue()
          Module('g.copy', vector=['{}@PERMANENT'.format(map_name),map_name],
                 overwrite=True)
          return map_name
     
     def export(self):
          pass
