#!/usr/bin/env python3

import os
import re
import tempfile
import shutil
from zipfile import ZipFile

from grass.pygrass.modules import Module

DIR="/home/martin/geodata/k143/SWI 2018 GeoTIFF Clip OrLiRi/"

def filter_files(dirname, filter_='.zip'):
    pattern = re.compile(r'.*{}$'.format(filter_))
    files = []
    for rec in os.walk(dirname):
        if not rec[-1]:
            continue
        
        match = filter(pattern.match, rec[-1])
        if match is None:
            continue

        for f in match:
            files.append(os.path.join(rec[0], f))
            
    return files

def process_zip(zip_file):
    print ("Processing {}...".format(zip_file))
    dir_path = tempfile.mkdtemp()
    with ZipFile(zip_file) as fd:
        fd.extractall(dir_path)

    os.environ['GRASS_OVERWRITE'] = '1'
    for tf in filter_files(dir_path, 'tiff'):
        map_name = os.path.splitext(os.path.basename(tf))[0]
        Module('r.import', input=tf, output=map_name)

    shutil.rmtree(dir_path)
    
def main(directory):
    for zip_file in filter_files(directory):
        process_zip(zip_file)

if __name__ == "__main__":
    main(DIR)
