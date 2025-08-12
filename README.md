# Scripts for generating Garmin POI files (via gpsbabel) from OpenCampingMap

# Usage

First of all one might need to install the international-address-formatter python
package.

```
pip install international-address-formatter
```

Unfortunately this package seems to be broken.

I was able to fix this using the following command:

```
recode latin1..utf8 $(python -m site --user-site)/international_address_formatter/data/worldwide.yml

```

Afterwards it is possible to call gen_garmin_poi.py. Currently supported output
langages are German and English. Feel free to send patches for others :)

This script has three modes:

* One for generating POI-Output for a single given country,
* one for generating POI-Output for all countries of the world
* and one for generating POI-Output for a given bounding box

The script will generate GPX-Files which can then be converted to Garmin
POI-Format using gpsbabel in a second step.

To do this just call the provided script gpx2poi.

This stuff will likely run on Unix only. Just go for WSL if you are forced to
use Windows.
