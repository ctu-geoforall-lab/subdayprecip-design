#!/usr/bin/env python3

import os
from pathlib import Path
from collections import OrderedDict
from subprocess import PIPE

from grass.pygrass.modules import Module
import grass.script.setup as gsetup

### !!! CHANGE START/END DATE !!!
START = '2018-06-09'
END = '2018-06-12'

VALUES = [2, 5, 10, 15, 20, 40, 60, 100]

def process_value(start, end, value, data):
    what = Module(
        't.rast.what', flags='v',
        points='coo', strds='swi',
        where="start_time >= '{}' and start_time <= '{}' and name like '%-SWI-{}%'".format(
            start, end, value),
        layout='row',
        stdout_=PIPE
    )
    
    for line in what.outputs.stdout.splitlines():
        item = line.split('|')
        if item[0] not in data:
            data[item[0]] = OrderedDict()
        if item[3] not in data[item[0]]:
            data[item[0]][item[3]] = []
        try:
            value = float(item[-1])
            if value > 240:
                value = ''
            else:
                value *= 0.5
            data[item[0]][item[3]].append(value)
        except ValueError:
            data[item[0]][item[3]].append('')
    
def write_csv(fd, data):
    for time, values in data.items():
        fd.write('{},{}\n'.format(
            time, ','.join(map(lambda x: str(x), values)))
        )

if __name__ == "__main__":
    gisdbase = Path.home() / Path("grassdata")
    location = 'swi'
    gsetup.init(os.environ['GISBASE'], gisdbase, location, 'PERMANENT')

    # region
    tlist = Module('t.rast.list', input='swi', stdout_=PIPE, flags='u', columns='name')
    Module('g.region', raster=tlist.outputs.stdout.splitlines()[0])

    data = {}
    for val in VALUES:
        process_value(START, END, '{:>03}'.format(val), data)

    for f in data.keys():
        with open('{:>03}.csv'.format(f), 'w') as fd:
            fd.write('time,{}\n'.format(
                ','.join(map(lambda x: 'SWI{:>03}'.format(x), VALUES))
            ))
            write_csv(fd, data[f])

