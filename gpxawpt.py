#!/usr/bin/env python
"""
Script to add a waypoint to GPX file.

Requires lxml for XML parsing.

Sample call (- for stdin/stdout works, too):
python .\gpxawp --name "My waypoint" --lat 53.72674043005578 --lon 9.663162231445314.py in.gpx > out.gpx
"""

import sys
import argparse
from lxml import etree # https://lxml.de/tutorial.html

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Add/insert a waypoint to GPX file')
    parser.add_argument('name', help="The waypoint name")
    parser.add_argument('lat', help="Latitude, as float number")
    parser.add_argument('lon', help="Longitude, as float number")
    parser.add_argument('--pos', "-p", type=int, default=sys.maxsize, required=False, help="Position to insert at, zero-based, default is to append")
    parser.add_argument('infile', nargs='?', default='-', type=argparse.FileType('r'), help="Input GPX file, default stdin ('-')")
    parser.add_argument('outfile', nargs='?', default='-', type=argparse.FileType('w'), help="Output GPX file, default stdout ('-')")
    args = parser.parse_args()

    gpx = etree.parse(args.infile)
    root = gpx.getroot()

    wpt = etree.Element("wpt", lat=args.lat, lon=args.lon)
    etree.SubElement(wpt, "name").text = args.name

    waypoints = root.findall('.//{*}wpt')
    p = max(0, args.pos)
    if len(waypoints) > p:
        waypoints[p].addprevious(wpt)
    elif len(waypoints):
        waypoints[-1].addnext(wpt)
    else:
        root.append(wpt)
    
    args.outfile.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    args.outfile.write(etree.tostring(root, pretty_print=True).decode())
