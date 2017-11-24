#!/usr/bin/python

import os
import sys
import glob
import subprocess
import tempfile

SAMPLE = False

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
    run_command('r.grow', input=map_name, out='{}_f'.format(map_name), radius=9)

    # run_command('r.colors', map=map_name, raster='chmi_1d')
    # # fill gaps
    # run_command('r.fill.gaps', input=map_name, output=map_name + '_f_tmp',
    #              flags='p',
    #              uncertainty=map_name + '_f_unc')
    # # r.fill.gaps - avoid extrapolation
    # run_command('r.mapcalc',
    #             expression='{m}_f = if(isnull({m}),if({m}_f_unc < 0.25,{m}_f_tmp,null()),{m})'.format(m=map_name)
    # )
    run_command('r.colors', map='{}_f'.format(map_name), raster='chmi_1d')
    run_command('r.out.gdal', input='{}_f'.format(map_name),
                output=os.path.join(outdir, 'sjtsk_{}.tiff'.format(map_name)))

def compute_utm(datadir, outdir):
    location = 'location-32633'
    init(gisbase=os.environ['GISBASE'], dbase=datadir, location=location)
    if not os.path.exists(os.path.join(datadir, location)):
        create_location(dbase=datadir, location=location, epsg=32633)

    # os.chdir(datadir)
    # for f in glob.glob('*.vrt'):
    #     mapname = os.path.splitext(os.path.basename(f))[0]
    #     if not find_file(mapname, element='vector')['fullname']:
    #         run_command('v.import', input=f, output=mapname + '_imp')
    #         run_command('v.transform', input=mapname + '_imp', out=mapname, xshift=-2000, yshift=2000)

    #     run_command('v.out.ogr', input=mapname, output=os.path.join(outdir, 'utm_{}.gpkg'.format(mapname)),
    #                 flags='se', format='GPKG')
    if not find_file(mapname, element='vector')['fullname']:
        run_command('v.proj', location='location-5514', input=mapname)
    run_command('v.out.ogr', input=mapname, output=os.path.join(outdir, 'utm_{}.gpkg'.format(mapname)),
                flags='se', format='GPKG')

def compute_wgs84(datadir, outdir):
    location = 'location-4326'
    init(gisbase=os.environ['GISBASE'], dbase=datadir, location=location)
    print os.path.join(datadir, location)
    if not os.path.exists(os.path.join(datadir, location)):
        create_location(dbase=datadir, location=location, epsg=4326)
    
    os.chdir(datadir)
    for f in glob.glob('*.vrt'):
        mapname = os.path.splitext(os.path.basename(f))[0]
        #     if not find_file(mapname, element='vector')['fullname']:
        #         run_command('v.import', input=f, output=mapname)
        if not find_file(mapname, element='vector')['fullname']:
            run_command('v.proj', location='location-5514', input=mapname)
        run_command('v.out.ogr', input=mapname, output=os.path.join(outdir, 'wgs84_{}.gpkg'.format(mapname)),
                    flags='se', format='GPKG')
    
def compute_sjtsk(datadir, outdir):
    location = 'location-5514'
    init(gisbase=os.environ['GISBASE'], dbase=datadir, location=location)
    print os.path.join(datadir, location)
    if not os.path.exists(os.path.join(datadir, location)):
        create_location(dbase=datadir, location=location, epsg=5514, datum_trans=2)
    
    os.chdir(datadir)
    for f in glob.glob('*.vrt'):
        mapname = os.path.splitext(os.path.basename(f))[0]
        if not find_file(mapname, element='vector')['fullname']:
            run_command('v.import', input=f, output=mapname + '_imp')
            run_command('v.transform', input=mapname + '_imp', out=mapname, xshift=-1000, yshift=1000)            
        run_command('v.out.ogr', input=mapname, output=os.path.join(outdir, 'sjtsk_{}.gpkg'.format(mapname)),
                    flags='se', format='GPKG')

    # import CHMI
    run_command('r.in.gdal', input=os.path.join(datadir, 'chmi100_jtsk', 'w001001.adf'),
                output='chmi_1d', flags='o')
    run_command('r.colors', map='chmi_1d', rules='myblues.txt')

    # install dependencies
    # for prog in ('r.vect.stats', 'r.fill.gaps'):
    #     if find_program(prog):
    #         continue
    #     run_command('g.extension', extension=prog)

    # set region
    run_command('g.region', raster='chmi_1d')
    if not find_file('stat', element='vector')['fullname']:
        run_command('v.import', input=os.path.join(datadir, 'stat.gpkg'), output='stat')
    run_command('r.mask', vector='stat')

    for map_name in list_grouped('vector', exclude='^stat')['PERMANENT']:
        for col in vector_columns(map_name).keys():
            if col in ('cat', 'Pixel', 'Lat', 'Lon', 'Alt'):
                continue
            message("Processing <{}> column '{}' writing to '{}'...".format(
                map_name, col, outdir
            ))
            create_raster(map_name, col, outdir)
            if SAMPLE == True:
                return


if __name__ == "__main__":
    # add GRASS libraries to path
    sys.path.append(os.path.join(find_grass(), 'etc', 'python'))
    
    # import GRASS libraries
    from grass.script.core import create_location, run_command, gisenv, list_grouped, \
        find_program, message, find_file
    from grass.script.vector import vector_columns
    from grass.script.setup import init

    # fix for G72
    os.environ['PATH'] += os.pathsep + os.path.join(os.environ['HOME'], '.grass7', 'addons', 'bin')
    
    os.environ['GRASS_OVERWRITE'] = '1'

    # datadir = tempfile.mkdtemp()
    datadir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'datadir')
    if not os.path.exists(datadir):
        sys.exit("Input dir not found")
    
    # outdir = tempfile.mkdtemp()
    outdir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'outdir')
    if os.path.exists(outdir):
        import shutil
        shutil.rmtree(outdir)
    os.makedirs(outdir)
        
    # compute_utm(datadir, outdir)

    compute_sjtsk(datadir, outdir)

    compute_wgs84(datadir, outdir)

    print('DATADIR: {}'.format(datadir))
    print('OUTDIR: {}'.format(outdir))
