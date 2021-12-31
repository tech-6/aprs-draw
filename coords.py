#! /usr/bin/env python
# Simple script to convert normal coords to APRS coordinates

import xml.sax
import sys


class CoordHandler(xml.sax.ContentHandler):
    counter = 0
    lats = []
    lons = []

    def __init__(self):

        pass

    def startElement(self, tag, attrs):
        # Handle waypoints
        if tag == 'wpt':
            self.counter += 1
            lat = float(attrs['lat'])
            lon = float(attrs['lon'])

            # format latitude for APRS
            if lat < 0:
                northsouth = 'S'
            else:
                northsouth = 'N'

            lat = abs(lat)
            lat_degrees = str(int(lat))

            if len(lat_degrees) < 2:
                lat_degrees = '0' + lat_degrees

            lat_minutes = ((lat % 1) * 60).__round__(2)

            lat_partial_minutes = str((lat_minutes % 1).__round__(2))[1:]
            lat_minutes = str(int(lat_minutes))

            while len(lat_minutes) < 2:
                lat_minutes = '0' + lat_minutes

            while len(lat_partial_minutes) < 3:
                lat_partial_minutes += '0'

            lat_aprs = lat_degrees + lat_minutes + lat_partial_minutes + northsouth

            # format longitude for APRS
            if lon < 0:
                eastwest = 'W'
            else:
                eastwest = 'E'

            lon = abs(lon)
            lon_degrees = str(int(abs(lon)))

            if len(lon_degrees) < 3:
                lon_degrees = '0' + lon_degrees

            lon_minutes = ((lon % 1) * 60).__round__(2)

            lon_partial_minutes = str((lon_minutes % 1).__round__(2))[1:]
            lon_minutes = str(int(lon_minutes))

            while len(lon_minutes) < 2:
                lon_minutes = '0' + lon_minutes

            while len(lon_partial_minutes) < 3:
                lon_partial_minutes += '0'

            lon_aprs = lon_degrees + lon_minutes + lon_partial_minutes + eastwest

            # Data Verification

            if len(lat_aprs) != 8:
                print('lat: ' + str(len(lat_aprs)), file=sys.stderr)
                print('lat: ' + str(lat_aprs), file=sys.stderr)

                raise

            if len(lon_aprs) != 9:
                print('lon: ' + str(len(lon_aprs)), file=sys.stderr)
                print('lon: ' + str(lon_aprs), file=sys.stderr)

                raise

            self.lats.append(lat_aprs)
            self.lons.append(lon_aprs)



    def endElement(self, tag):
        pass

    def characters(self, content):
        pass


def main():
    # create an XMLReader
    parser = xml.sax.make_parser()
    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    # override the default ContextHandler

    xml.sax.parse("points.gpx", CoordHandler())

    print(CoordHandler.lats)
    print(CoordHandler.lons)

    pass


if __name__ == '__main__':
    main()
