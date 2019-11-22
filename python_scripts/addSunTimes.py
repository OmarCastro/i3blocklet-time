import sys
from sun import Sun

sun = Sun()

def toTimeInOffset(suntime,utcOffset):
    gmt_offset_multi = 1 if utcOffset[0] == "+" else -1
    gmt_offset_hours = int(utcOffset[1:-2])
    gmt_offset_minutes = int(utcOffset[-2:])
    gmt_offset_in_minutes = gmt_offset_multi * (gmt_offset_hours * 60 + gmt_offset_minutes);
    utc_hours = suntime['hr']
    utc_mins = suntime['min']
    utc_in_mins = utc_hours * 60 + utc_mins
    local_time = utc_in_mins + gmt_offset_in_minutes
    local_time = local_time % (24 * 60) if local_time >= 0 else local_time + 24 * 60
    local_hours = local_time / 60
    local_min = local_time % 60
    return '{0:02d}:{1:02d}'.format(local_hours, local_min)



for line in sys.stdin:
  fields=line.split()
  utcOffset=fields[1]
  lat=float(fields[3])
  lon=float(fields[4])
  coords = {'longitude' : lon, 'latitude' : lat }
  sunrise = sun.getSunriseTime( coords )
  if sunrise['status']:
    sunset = sun.getSunsetTime( coords )
    leftToken = toTimeInOffset(sunrise, utcOffset)
    rightToken = toTimeInOffset(sunset, utcOffset)
  else:
    leftToken = "allDay" if sunrise['alwaysDay'] else "allNight"
    rightToken = leftToken
  print '{0} {1} {2}'.format(line.rstrip("\n\r"), leftToken, rightToken)

