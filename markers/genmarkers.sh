#!/bin/bash
#
# (c) 2023 Sven Geggus <sven-git@geggus.net>
#
# Use this script to recreate bmp-files from OpenCampingMap SVG
#
# directory containing markers from OpenCampingMap
# https://github.com/giggls/opencampsitemap/tree/master/markers
DIR=~/osm/campsite-map/map/markers

for bn in standard nudist backcountry camping caravan group_only; do
 inkscape --export-type=png --export-filename=markers/$bn.png --export-area-page --export-overwrite --export-background="rgb(255, 0, 255)" -h 24 $DIR/m_$bn.svg 2>/dev/null
 convert markers/$bn.png -compress none -type palette BMP3:markers/$bn.bmp;
 rm markers/$bn.png
 inkscape --export-type=png --export-filename=markers/${bn}_private.png --export-area-page --export-overwrite --export-background="rgb(255, 0, 255)" -h 24 $DIR/m_private_$bn.svg 2>/dev/null
 convert markers/${bn}_private.png -compress none -type palette BMP3:markers/${bn}_private.bmp;
 rm markers/${bn}_private.png
done

