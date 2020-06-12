#!/usr/bin/env python3

import os
import re
import tempfile
import shutil
from zipfile import ZipFile
from datetime import datetime
from pathlib import Path

from grass.pygrass.modules import Module
import grass.script as gs
import grass.script.setup as gsetup

# !!! CHANGE INPUT DIRECTORY FOLDER !!!
DIR = r"Z:\k143"

POINTS = os.path.join(DIR, "coo.txt")
INPUT = os.path.join(DIR, "SWI 2018 GeoTIFF Clip OrLiRi")

def import_points(points):
    Module('v.in.ascii',
           points,
           x=3, y=2, separator='tab',
           output='coo')

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

    date = datetime.strptime(
        os.path.basename(zip_file).split('_')[3], '%Y%m%d%H%M'
    )
    tlist = []
    for tf in filter_files(dir_path, 'tiff'):
        map_name = os.path.splitext(os.path.basename(tf))[0]
        tlist.append((map_name, date.strftime('%Y-%m-%d %H:%M')))
        Module('r.import', input=tf, output=map_name)

    tlist_file = gs.tempfile()
    with open(tlist_file, 'w') as fd:
        for item in tlist:
            fd.write('{}|{}\n'.format(item[0], item[1]))
    Module('t.register', input='swi', file=tlist_file)

    shutil.rmtree(dir_path)
    
def main(directory, points):
    os.environ['GRASS_OVERWRITE'] = '1'
    os.environ['GRASS_VERBOSE'] = '-1'

    gisdbase = Path.home() / Path("grassdata")
    location = 'swi'
    gsetup.init(os.environ['GISBASE'], gisdbase, location, 'PERMANENT')
    gs.create_location(gisdbase, location, epsg=4326)
    
    Module('t.create', output='swi', title='swi', description='swi')

    import_points(points)
    for zip_file in filter_files(directory):
        process_zip(zip_file)

if __name__ == "__main__":
    main(INPUT, POINTS)
