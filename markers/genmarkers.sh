#!/bin/bash
#
# (c) 2023 Sven Geggus <sven-git@geggus.net>
#
# Use this script to recreate bmp-files from OpenCampingMap SVG
#
# directory containing markers from OpenCampingMap
# https://github.com/giggls/opencampsitemap/tree/master/markers
#
# do not run this resulting files have been manually edited
#

DIR=~/osm/campsite-map/map/markers

for bn in standard nudist backcountry camping caravan group_only; do
 inkscape --export-type=png --export-filename=$bn.png --export-area-page --export-overwrite --export-background="rgb(255, 255, 255)" -h 24 $DIR/m_$bn.svg 2>/dev/null
 convert $bn.png -compress none -type palette BMP3:$bn.bmp;
 inkscape --export-type=png --export-filename=${bn}_private.png --export-area-page --export-overwrite --export-background="rgb(255, 255, 255)" -h 24 $DIR/m_private_$bn.svg 2>/dev/null
 convert ${bn}_private.png -compress none -type palette BMP3:${bn}_private.bmp;
done

