#!/usr/bin/env python
"""
Script to collapse GPX file to a single segment (<trkseg>).
Some Garmin units appear to show only the FIRST segment.

Requires lxml for XML parsing.

Sample call (- for stdin/stdout works, too):
python .\gpx1seg.py in.gpx > out.gpx
"""

import argparse
from lxml import etree # https://lxml.de/tutorial.html

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Collapse GPX file to single segment')
    parser.add_argument('infile', nargs='?', default='-', type=argparse.FileType('r'))
    parser.add_argument('outfile', nargs='?', default='-', type=argparse.FileType('w'))
    args = parser.parse_args()

    gpx = etree.parse(args.infile)
    root = gpx.getroot()
    trkseg0 = None
    for trkseg in root.iter("{*}trkseg"):
        if trkseg0 is None:
            trkseg0 = trkseg
        else:
            trkseg0.extend(trkseg)
            trkseg0.getparent().remove(trkseg)

    args.outfile.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    args.outfile.write(etree.tostring(root, pretty_print=True).decode())
