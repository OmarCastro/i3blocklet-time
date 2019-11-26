import math
import re
import datetime
from decimal import Decimal

class GeoLocation:

    def __init__(self, lat, long):
        self.latitude=lat
        self.longitude=long

    def _format_coord_iso(self, coord, positive_sign,negative_sign):
        sign = negative_sign if coord.decimal < 0 else positive_sign
        degrees = "" if coord.degrees is None else '{0}º'.format(int(coord.degrees))
        minutes = "" if coord.minutes is 0 else '{0:02d}′'.format(int(coord.minutes))
        seconds = ""if coord.seconds is 0 else '{0:02d}″'.format(int(coord.seconds))
        return degrees+minutes+seconds+sign

    def _format_coord_decimal(self, coord, positive_sign,negative_sign):
        sign = negative_sign if coord.decimal < 0 else positive_sign
        return '{0} {1}'.format(round(coord.decimal, 4),sign)


    def format_latitude_iso(self):
        return self._format_coord_iso(self.latitude, "N", "S")

    def format_longitude_iso(self):
        return self._format_coord_iso(self.longitude, "E", "W")

    def format_latitude_decimal(self):
        return self._format_coord_decimal(self.latitude, "N", "S")

    def format_longitude_decimal(self):
        return self._format_coord_decimal(self.longitude, "E", "W")
class Coordinate:
    def __init__(self, degrees=None, minutes=None, seconds=None, fraction=None, sign="+"):
        if fraction is not None:
            if seconds is not None:
                seconds += fraction
            elif minutes is not None:
                minutes += fraction
            else:
                degrees += fraction
        minutes = Decimal(minutes) if (minutes is not None) else 0
        seconds = Decimal(seconds) if (seconds is not None) else 0
        degrees = Decimal(degrees)
        decimal = degrees + minutes / Decimal('60') + seconds / Decimal('3600')
        decimal = decimal * Decimal(sign + '1')

        self.degrees, self.minutes, self.seconds, self.sign = degrees, minutes, seconds, sign
        self.decimal = decimal



re_coord = r"""
            ^
            (?P<lat_sign>\+|-)
            (?P<lat_degrees>[0,1]?\d{2})
            (?P<lat_minutes>\d{2}?)?
            (?P<lat_seconds>\d{2}?)?
            (?P<lat_fraction>\.\d+)?
            (?P<lng_sign>\+|-)
            (?P<lng_degrees>[0,1]?\d{2})
            (?P<lng_minutes>\d{2}?)?
            (?P<lng_seconds>\d{2}?)?
            (?P<lng_fraction>\.\d+)?
"""
regex = re.compile(re_coord, flags=re.VERBOSE)

def from_ISO_6709(raw_coords):
    """ Convert a string of coordinates to a set of DMSDegree and Decimal Altitude """
    match = regex.match(raw_coords).groupdict()
    results = {}
    for key in ('lat', 'lng'):
        results[key] = {}
        for value in ('sign', 'degrees', 'minutes', 'seconds', 'fraction'):
            results[key][value] = match['{}_{}'.format(key, value)]
    return GeoLocation(Coordinate(**results['lat']), Coordinate(**results['lng']))



