# grass -c EPSG:5514 grassdata/soil_gran --exec python3 utils/soil_gran.py ~/Downloads/wps_data

import os
import sys
import glob

from grass.pygrass.modules import Module

input_dir = sys.argv[1]

for tif in glob.glob(input_dir + "/*.tif"):
    tif_path = os.path.abspath(tif)
    map_name = os.path.splitext(os.path.basename(tif))[0]
    Module("r.in.gdal", flags="o", input=tif_path, output=map_name)
