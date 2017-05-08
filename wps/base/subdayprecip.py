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

from pywps import Process, ComplexInput, LiteralInput, Format

class SubDayPrecipProcess(Process):
     def __init__(self, identifier, description, location='/opt/grassdata/subdayprecip', skip=[],
                  inputs=[], outputs=[]):
          if 'input' not in skip:
               inputs.append(ComplexInput(
                    identifier="input",
                    title=u"Vstupni bodová nebo polygonova vektorova data",
                    supported_formats=[Format('application/gml+xml'),
                                       Format('application/zip; charset=binary')])
               )

          inputs.append(LiteralInput(
               identifier="return_period",
               title=u"Doby opakovani",
               data_type='string',
               default="N2,N5,N10,N20,N50,N100")
          )
          if 'rainlength' not in skip:
               inputs.append(LiteralInput(
                    identifier="rainlength",
                    title=u"Delka srazky v minutach",
                    data_type='integer')
               )

          super(SubDayPrecipProcess, self).__init__(
               self._handler,
               identifier=identifier,
               version="0.1",
               title=u"Navrhova srazka pro zvolenou lokalitu. " + description,
               abstract=u"Pocita navrhovou srazku pro zvolenou lokalitu s vyuzitim nastroje GRASS GIS r.subdayprecip.design. Vice informaci na http://rain.fsv.cvut.cz/nastroje/r.subdayprecip.design",
               inputs=inputs,
               outputs=outputs,
               grass_location=location,
               store_supported=True,
               status_supported=True)
          
          self.rainlength_value = None
          self.output = None # to be defined by descendant
          self.output_dir = None
          
          os.environ['GRASS_SKIP_MAPSET_OWNER_CHECK'] = '1'
          os.environ['HOME'] = '/tmp' # needed by G_home()
          
     # def __del__(self):
     #      if self.output_dir:
     #           shutil.rmtree(self.output_dir)

     def _handler(self, request, response):
          if not self.rainlength_value:
               self.rainlength_value = request.inputs['rainlength'][0].data
          # if 'input' in request.inputs.keys():
          #      self.map_name = self.import_data()
          # else:
          #      self.map_name = self.copy()
          self.map_name = self.import_data(request.inputs['input'][0].data)
          
          if 'keycolumn' in request.inputs.keys():
               self.check_keycolumn(request.inputs['keycolumn'][0].data)

          self.rasters = request.inputs['return_period'][0].data.split(',')

          self.output_dir = os.path.join('/tmp', '{}_{}'.format(
               self.map_name, os.getpid())
          )
          os.mkdir(self.output_dir)

          Module('g.region', raster=self.rasters[0])
          logging.debug("Subday computation started")
          start = time.time()
          Module('r.subdayprecip.design',
                 map=self.map_name, return_period=self.rasters,
                 rainlength=self.rainlength_value
          )
          logging.info("Subday computation finished: {} sec".format(time.time() - start))
          logging.info("{}".format(Module(
               'v.info', flags='c', map=self.map_name, stdout_=PIPE).outputs.stdout)
          )
          response.outputs['output'].file = self.export()

          return response
     
     def check_keycolumn(self, keycol):
          # check if key columns exists
          map_cols = Module('db.columns',
                            table=self.map_name, stdout_=PIPE).outputs.stdout.splitlines()
          if keycol not in map_cols:
               raise StandardError(
                    "Key column ({}) not found in input attribute table ({})".format(
                    keycol, ','.join(map_cols))
               )
          
     def import_data(self, input_data, link_only=False):
          map_name = 'subdayprecip_output'

          prefix = '/'
          if input_data.endswith('gzip'):
               prefix += 'vsigzip/' 
          elif input_data.endswith('zip'):
               prefix += 'vsizip/'
          if input_data.startswith('http'):
               prefix += 'vsicurl/'
          input_data = prefix + input_data

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
                      **module_in_args
               )
          except CalledModuleError as e:
               raise Exception("Unable to import input vector data: {}".format(e))
          
          logging.info("Input data imported ({}): {} sec".format(
               module_in, time.time() - start)
          )
          
          return map_name
     
     # def copy(self):
     #      map_name = request.inputs['input'][0].data
     #      Module('g.copy', vector=['{}@PERMANENT'.format(map_name),map_name],
     #             overwrite=True
     #      )

     #      return map_name
     
     def export(self):
          pass
