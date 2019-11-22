import sys
from datetime import datetime

now = datetime.now()
currentHourUTC = now.hour
currentMinuteUTC = now.minute

def timeinOffset(utcOffset):
    gmt_offset_multi = 1 if utcOffset[0] == "+" else -1
    gmt_offset_hours = int(utcOffset[1:-3])
    gmt_offset_minutes = int(utcOffset[-2:])
    gmt_offset_in_minutes = gmt_offset_multi * (gmt_offset_hours * 60 + gmt_offset_minutes);
    utc_hours = currentHourUTC
    utc_mins = currentMinuteUTC
    utc_in_mins = utc_hours * 60 + utc_mins
    local_time = utc_in_mins + gmt_offset_in_minutes
    local_time = local_time % (24 * 60) if local_time >= 0 else local_time + 24 * 60
    local_hours = local_time / 60
    local_min = local_time % 60
    return '{0:02d}:{1:02d}'.format(local_hours, local_min)


data_format_fromArgs=sys.argv[1].split(",")
mapdict={
    'name': 0,
    'offset': 1,
    'abbreviation': 2,
    'latitude': 3,
    'longitude': 4,
    'sunrise': 5,
    'sunset': 6,
    'time': 7
}
data_format=[ x for x in data_format_fromArgs if x in mapdict ]
data_format_idx=[ mapdict[x] for x in data_format ]
def formatData(fields):
    return [ fields[x] for x in data_format_idx ]

isTimeinData = 'time' in data_format

print ';'.join(data_format)+"; "

for line in sys.stdin:
    fields=line.split()
    if isTimeinData : fields.append( timeinOffset(fields[1] ) )
    print ';'.join(formatData(fields))

