import sys
import time
import os
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--sort',  help='sort results by offset', action='store_true')
parser.add_argument('-f','--tz-field',  type=int, help='field with timezone', required=True)
parser.add_argument('-s','--separator',  help='input field separator', default=None)
parser.add_argument('-o','--output-separator',  help='output field separator', default=" ")
args = parser.parse_args()
if args.tz_field < 1:
    parser.error("timezone field must be a positive number")

now = time.time()

def offsets_in_timezone(timezone_name):
    os.environ["TZ"]=timezone_name
    time.tzset()
    result = time.strftime("%z %z %Z",time.localtime(now)).split()
    result[0] = result[0][:3] + ":" + result[0][3:]
    return result

linesDict = {}
for line in sys.stdin:
    fields = line.split(args.separator)
    offsets = offsets_in_timezone(fields[args.tz_field - 1])
    fields += offsets
    if args.sort:
        offset = offsets[1]
        linesDict.setdefault(offset, [])
        linesDict[offset].append(args.output_separator.join(fields));
    else:
        print(args.output_separator.join(fields))
    

if args.sort:
    keys = sorted(linesDict.keys(), key=int)
    for key in keys:
        print('\n'.join(linesDict[key]))

