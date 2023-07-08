# Some ad-hoc tools to tweak GPX files

I prefer to __construct__ our ([road cycling event](https://www.rg-wedel.de/rtf-2022-tracks-und-ausschilderung/)) tracks from re-usable "segment files". Some stretches of road are part of multiple tracks, so editing the respective segment file __once__ followed by automated re-construction of the resulting tracks via scripting keeps all tracks in sync and accurate.

This is more exact than using interactive tools to work on each track in turn. And it is much easier and faster to use the command line than using interactive tools (e.g. online) to concatenate the tracks from segment GPXs manually.

These scripts use Python and expect [lxml](https://lxml.de/) to be installed.

## Build GPX from Segments

    # Concatenate a number of segment files to a basic template:
	python .\gpxscat.py --name "My Tour" template.gpx segment1.gpx segment2.gpx > concatenated.gpx 

## Reduce to single Track Segment

    # Some Garmin units appear to show only the FIRST segment.
    python .\gpx1segt.py concatenated.gpx > single-segment.gpx
