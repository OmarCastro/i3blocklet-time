import sys
import time
import os
from utils.geo_location import from_ISO_6709

now = time.time()

def time_in_timezone(timezone_name):
    os.environ["TZ"]=timezone_name
    time.tzset()
    result = time.strftime("%H:%M",time.localtime(now)).split()
    return result


data_format_fromArgs=sys.argv[1].split(",")
mapdict={
    'name': 0,
    'geolocation': 1,
    'sunrise': 2,
    'sunset': 3,
    'offset': 4,          'offset:hh:mm': 4,
    'offset:hhmm': 5,  
    'abbreviation': 6,
    'time': 7,      
    'latitude': 8,       'latitude:iso': 8,
    'longitude': 9,      'longitude:iso': 9,
    'latitude:decimal': 10,
    'longitude:decimal': 11
}
data_format=[ x for x in data_format_fromArgs if x in mapdict ]
headers=[ x.split(':')[0] for x in data_format]
data_format_idx=[ mapdict[x] for x in data_format ]

def format_data(fields):
    return [ fields[x] for x in data_format_idx ]

is_time_in_data = 'time' in data_format
is_formattedGeoLocation_in_data = any([x.startswith('latitude') or x.startswith('longitude') for x in data_format])

print(';'.join(headers)+"; ")


for line in sys.stdin:
    fields = line.split()
    fields += time_in_timezone(fields[mapdict['name']] ) if is_time_in_data else ['']
    if is_formattedGeoLocation_in_data:
        coordinates = from_ISO_6709(fields[mapdict['geolocation']])
        fields += [coordinates.format_latitude_iso(), coordinates.format_longitude_iso(),coordinates.format_latitude_decimal(), coordinates.format_longitude_decimal()]
    else:
        fields += [''] * 4

    print(';'.join(format_data(fields)));