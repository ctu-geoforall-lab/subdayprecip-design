#!/usr/bin/env python3

import os
import sys
import time
from collections import OrderedDict
from subprocess import PIPE
from datetime import timedelta

from grass.pygrass.modules import Module
import grass.script.setup as gsetup

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
    if len(sys.argv) != 3:
        sys.exit("Define start and end date\n"
                 "Example:\n./generate_csv.py 2018-06-09 2018-06-12")

    gisdbase = os.path.join(os.path.dirname(__file__), "grassdata")
    location = 'swi'
    gsetup.init(os.environ['GISBASE'], gisdbase, location, 'PERMANENT')

    start = time.time()

    # region
    tlist = Module('t.rast.list', input='swi', stdout_=PIPE, flags='u', columns='name')
    Module('g.region', raster=tlist.outputs.stdout.splitlines()[0])

    data = {}
    for val in VALUES:
        process_value(sys.argv[1], sys.argv[2], '{:>03}'.format(val), data)

    for f in data.keys():
        with open('{:>03}.csv'.format(f), 'w') as fd:
            fd.write('time,{}\n'.format(
                ','.join(map(lambda x: 'SWI{:>03}'.format(x), VALUES))
            ))
            write_csv(fd, data[f])

    print("Elapsed: {}".format(timedelta(seconds=time.time() - start)))
