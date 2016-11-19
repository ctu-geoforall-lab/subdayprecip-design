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
from mimetypes import MimeTypes
import magic

os.environ['GISBASE'] = '/opt/grass/dist.x86_64-pc-linux-gnu'
sys.path.append(os.path.join(os.environ["GISBASE"], "etc", "python"))
logging.info(sys.path)
from grass.pygrass.modules import Module
from grass.exceptions import CalledModuleError
from pywps.Process import WPSProcess

class SubDayPrecipProcess(WPSProcess):
     def __init__(self, identifier, description, location='subdayprecip', skip_input=False):
          WPSProcess.__init__(self,
                              identifier=identifier,
                              version="0.1",
                              title="Subday design precipitation. " + description,
                              abstract="Computes subday design precipitation series using GRASS GIS. "
                              "See http://grass.osgeo.org/grass70/manuals/addons/r.subdayprecip.design.html for details.",
                              grassLocation=location, storeSupported = True, statusSupported = True)

          if not skip_input:
               self.input = self.addComplexInput(identifier = "input",
                                                 title = "Input vector data",
                                                 formats = [ {"mimeType":"text/xml",
                                                              "encoding":"utf-8",
                                                              "schema":"http://schemas.opengis.net/gml/3.2.1/gml.xsd"} ],
                                                 minOccurs=0)
          
          self.raster = self.addLiteralInput(identifier = "raster",
                                             title = "Name of repetition periods raster map(s)",
                                             type = types.StringType,
                                             default = "H_002,H_005,H_010,H_020,H_050,H_100")
          
          self.rainlength = self.addLiteralInput(identifier = "rainlength",
                                                 title = "Rain length value in minutes",
                                                 type = types.IntType)
          
          self.output = None # to be defined by descendant
          self.output_dir = None
          
          os.environ['GRASS_SKIP_MAPSET_OWNER_CHECK'] = '1'
          os.environ['HOME'] = '/tmp' # needed by G_home()
          
     def __del__(self):
          if self.output_dir:
               shutil.rmtree(self.output_dir)
     
     def execute(self):
          if self.input:
               self.map_name = self.import_data()
          else:
               self.map_name = self.copy()
          
          self.output_dir = os.path.join('/tmp', '{}_{}'.format(self.map_name, os.getpid()))
          os.mkdir(self.output_dir)
          
          rasters = self.raster.getValue().split(',')
          Module('g.region', raster=rasters[0])
          logging.debug("Subday computation started")
          start = time.time()
          Module('r.subdayprecip.design',
                 map=self.map_name, raster=rasters, rainlength=self.rainlength.getValue())
          logging.info("Subday computation finished: {} sec".format(time.time() - start))
          
          self.export()

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
