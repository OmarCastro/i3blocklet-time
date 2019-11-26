import sys
import time
import os
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--sort',  help='sort results by offset', action='store_true')
args = parser.parse_args()

now = time.time()

def offsets_in_timezone(timezone_name):
    os.environ["TZ"]=timezone_name
    time.tzset()
    result = time.strftime("%z %z %Z",time.localtime(now)).split()
    result[0] = result[0][:3] + ":" + result[0][3:]
    return result

linesDict = {}
for line in sys.stdin:
    fields = line.split()
    offsets = offsets_in_timezone(fields[0])
    fields += offsets
    if args.sort:
        offset = offsets[1]
        linesDict.setdefault(offset, [])
        linesDict[offset].append(' '.join(fields));
    else:
        print(' '.join(fields))
    

if args.sort:
    keys = sorted(linesDict.keys(), key=int)
    for key in keys:
        print('\n'.join(linesDict[key]))

