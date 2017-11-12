#!/usr/bin/python

import os
import sys
import glob
import subprocess
import tempfile

def find_grass():
    """Find GRASS installation.
    """
    ins = subprocess.Popen(['grass', '--config', 'path'],
                           stdout=subprocess.PIPE)
    out, err = ins.communicate()

    os.environ['GISBASE'] = out.rstrip(os.linesep)

    return os.environ['GISBASE']

def create_raster(input_map, column, outdir):
    map_name = '{}_{}'.format(input_map, column)
    run_command('r.vect.stats', input=input_map, column=column,
                 output=map_name)
    run_command('r.colors', map=map_name, raster='chmi_1d')
    # vyplneni der
    run_command('r.fill.gaps', input=map_name, output=map_name + '_f_tmp',
                 flags='p',
                 uncertainty=map_name + '_f_unc')
    # r.fill.gaps provadi extrapolaci, to chceme zamezit
    run_command('r.mapcalc',
                expression='{m}_f = if(isnull({m}),if({m}_f_unc < 0.25,{m}_f_tmp,null()),{m})'.format(m=map_name)
    )
    run_command('r.colors', map='{}_f'.format(map_name), raster='chmi_1d')
    run_command('r.out.gdal', input='{}_f'.format(map_name),
                output=os.path.join(outdir, '{}.tiff'.format(map_name)))

def compute_utm():
    # GRASS lokace v S-JTSK
    # datadir = tempfile.mkdtemp()
    datadir = '/opt/grassdata'
    location = 'location-32633'
    init(gisbase=os.environ['GISBASE'], dbase=datadir, location=location)
    if not os.path.exists(os.path.join(datadir, location)):
        create_location(dbase=datadir, location=location, epsg=32633) #, datum_trans=2)

    # vytvoreni bodovych vrstev v S-JTSK (SHP)
    for f in glob.glob('*.vrt'):
        mapname = os.path.splitext(os.path.basename(f))[0]
        run_command('v.import', input=f, output=mapname)
        #run_command('v.out.ogr', input=mapname, output=os.path.join(outdir, mapname + '.gpkg'),
        #            flags='se', format='GPKG')

    # import CHMI
    run_command('r.in.gdal', input='p100_1d1/w001001.adf', output='chmi_1d', flags='o')
    run_command('r.colors', map='chmi_1d', rules='myblues.txt')

    # install dependencies
    for prog in ('r.vect.stats', 'r.fill.gaps'):
        if find_program(prog):
            continue
        run_command('g.extension', extension=prog)

    # set region
    run_command('g.region', raster='chmi_1d')
    run_command('v.proj', location='gismentors', mapset='ruian', input='staty', output='stat')
    run_command('r.mask', vector='stat')

    for map_name in list_grouped('vector', exclude='^stat')['PERMANENT']:
        for col in vector_columns(map_name).keys():
            if col in ('cat', 'Pixel', 'Lat', 'Lon', 'Alt'):
                continue
            create_raster(map_name, col, outdir)

if __name__ == "__main__":
    # add GRASS libraries to path
    sys.path.append(os.path.join(find_grass(), 'etc', 'python'))
    
    # import GRASS libraries
    from grass.script.core import create_location, run_command, gisenv, list_grouped, find_program
    from grass.script.vector import vector_columns
    from grass.script.setup import init

    # fix for G72
    os.environ['PATH'] += os.pathsep + os.path.join(os.environ['HOME'], '.grass7', 'addons', 'bin')
    
    os.environ['GRASS_OVERWRITE'] = '1'
    
    # outdir = tempfile.mkdtemp()
    outdir = '/tmp/data'
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    compute_utm()

print('grass --text {}'.format(os.path.join(datadir, location, 'PERMANENT')))
print('OUTDIR: {}'.format(outdir))
