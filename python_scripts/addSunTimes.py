import sys
import time
import os
from utils.sun import Sun
from utils.geo_location import from_ISO_6709

sun = Sun()

def to_time_in_timezone(suntime,timezone_name):
    os.environ["TZ"]=timezone_name
    time.tzset()
    timezone_offset=time.timezone;
    utc_hours = suntime['hr']
    utc_mins = suntime['min']
    utc_time = (utc_hours * 60 + utc_mins) * 60
    local_time = utc_time - timezone_offset;
    local_hours = (int(local_time / 3600) + 24) % 24
    local_min = int((local_time % 3600) / 60)
    return '{0:02d}:{1:02d}'.format(local_hours, local_min)



for line in sys.stdin:
  fields=line.split()
  timezone=fields[0]
  coordinates = from_ISO_6709(fields[1])
  coords = {'longitude' : float(coordinates.longitude.decimal), 'latitude' : float(coordinates.latitude.decimal) }
  sunrise = sun.getSunriseTime( coords )
  if sunrise['status']:
    sunset = sun.getSunsetTime( coords )
    leftToken = to_time_in_timezone(sunrise, timezone)
    rightToken = to_time_in_timezone(sunset, timezone)
  else:
    leftToken = "allDay" if sunrise['alwaysDay'] else "allNight"
    rightToken = leftToken
  print('{0} {1} {2}'.format(line.rstrip("\n\r"), leftToken, rightToken))

