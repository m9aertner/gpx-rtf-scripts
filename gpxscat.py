#!/usr/bin/env python
"""
Script to concatenate segments from two or more GPX files.

First file should be a "template", with a <trk> but no <trkseg>.
Subsequent files (one or more) should carry the segments.

Requires lxml for XML parsing. Pretty-print does not work 100%,
pipe through xmllint --format - for pretty-printed result.

Sample call:
python .\gpxscat.py --name "My Tour" template.gpx segment1.gpx segment2.gpx > concatenated.gpx 
"""

import re
import sys
import argparse
from lxml import etree # https://lxml.de/tutorial.html

def add(trk0: etree.Element, segment_file: str):
    segment_xml = etree.parse(segment_file)
    segment_root = segment_xml.getroot()
    namespace = re.match(r'{(.*)}.*', segment_root.tag).group(1) # http://www.topografix.com/GPX/1/1

    for segment in segment_root.iter("{%s}trkseg" % namespace):
        out = etree.SubElement(trk0, "trkseg")
        for trkpt in segment:
            pt = etree.SubElement(trk0, "trkpt", lat=trkpt.get("lat"), lon=trkpt.get("lon"))
            out.append(pt)
        trk0.append(out)

def create_root(gpx_file, name):
    first_gpx = etree.parse(gpx_file)
    first_root = first_gpx.getroot()
    for trk in first_root:
        trk0 = trk
        if name:
            n = etree.SubElement(trk0, "name")
            n.text = name
        break
    return (first_root, trk0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Concatenate GPX file segments')
    parser.add_argument('-n', '--name', type=str, default=None, help='Set track name')
    parser.add_argument('gpx_files', metavar='gpx', type=str, default='', nargs='*', help='GPX file')
    args = parser.parse_args()

    gpx_files = args.gpx_files
    i = 0
    for gpx_file in gpx_files:
        if i == 0:
            (root, trk0) = create_root(gpx_file, args.name)
        else:
            add(trk0, gpx_file)
        i = i + 1

    sys.stdout.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    sys.stdout.write(etree.tostring(root, pretty_print=True).decode())
