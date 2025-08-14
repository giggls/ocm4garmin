#!/usr/bin/python
#
# (c) 2023 Sven Geggus <sven-osm@geggus-net>
#
# Generate Garmin POI-files from campsites 
#
# This script will generate gpx-files which can then
# be converted to gpi via gpsbabel
#
#
#
import argparse
import sys
import requests
import xml.etree.ElementTree as ET
import os
import json
from international_address_formatter import AddressFormatter
import re

cscats = ["standard","nudist","backcountry","camping","caravan","group_only"]
private_values = ['private', 'members']

features = {
'en': {
  "tents": {
    "yes": {
      "text": "tents",
    },
    "no": {
      "text": "no tents",
    }
  },
  "caravans": {
    "yes": {
      "text": "caravans",
    },
    "no": {
      "text": "no caravans",
    }
  },
  "static_caravans": {
    "yes": {
      "text": "static caravans",
    }
  },
  "cabins": {
    "yes": {
      "text": "cabins",
    }
  },
  "permanent_camping": {
    "yes": {
      "text": "permanent camping",
    },
    "only": {
      "text": "permanent camping only"
    }
  },
  "toilets": {
    "yes": {
      "text": "toilets",
    },
    "no": {
      "text": "no toilets",
    }
  },
  "shower": {
    "yes": {
      "text": "showers",
    },
    "no": {
      "text": "no showers",
    }
  },
  "drinking_water": {
    "yes": {
      "text": "drinking water",
    },
    "no": {
      "text": "no drinking water",
    }
  },
  "power_supply": {
    "^(?!no).+$": {
      "text": "power supply",
    },
    "no": {
      "text": "no power supply",
    }
  },
  "sanitary_dump_station": {
    "^(?!no).+$": {
      "text": "sanitary dump station",
    }
  },
  "shop": {
    "yes": {
      "text": "shop",
    }
  },
  "laundry": {
    "yes": {
      "text": "laundry",
    }
  },
  "washing_machine": {
    "yes": {
      "text": "washing machine",
    }
  },
  "pub": {
    "yes": {
      "text": "pub",
    }
  },
  "bar": {
    "yes": {
      "text": "bar",
    }
  },
  "restaurant": {
    "yes": {
      "text": "restaurant",
    }
  },
  "fast_food": {
    "yes": {
      "text": "fast food",
    }
  },
  "telephone": {
    "yes": {
      "text": "public telephone",
    }
  },
  "post_box": {
    "yes": {
      "text": "post box",
    }
  },
  "playground": {
    "yes": {
      "text": "playground",
    }
  },
  "internet_access": {
    "yes": {
      "text": "internet",
    },
    "no": {
      "text": "no internet",
    },
    "wifi": {
      "text": "wifi",
    },
    "wlan": {
      "text": "wifi",
    }
  },
  "bbq": {
    "yes": {
      "text": "barbeque",
    }
  },
  "dog": {
    "yes": {
      "text": "dogs allowed"
    },
    "no": {
      "text": "dogs not allowed"
    },
    "leashed": {
      "text": "dogs leashed only"
    }
  },
  "motor_vehicle": {
    "yes": {
      "text": "motor vehicles",
    },
    "no": {
      "text": "no motor vehicles",
    }
  },
  "openfire": {
    "yes": {
      "text": "open fire allowed",
    },
    "no": {
      "text": "open fire prohibited",
    }
  },
  "sauna": {
    "yes": {
      "text": "sauna",
    }
  },
  "miniature_golf": {
    "yes": {
      "text": "miniature golf"
    }
  }
},
'de': {
  "tents": {
    "yes": {
      "text": "Zelte",
    },
    "no": {
      "text": "keine Zelte",
    }
  },
  "caravans": {
    "yes": {
      "text": "Wohnwagen",
    },
    "no": {
      "text": "keine Wohnwagen",
    }
  },
  "static_caravans": {
    "yes": {
      "text": "ortsfeste Wohnwagen",
    }
  },
  "cabins": {
    "yes": {
      "text": "Hütten",
    }
  },
  "permanent_camping": {
    "yes": {
      "text": "Dauercamper",
    },
    "only": {
      "text": "nur Dauercamper"
    }
  },
  "toilets": {
    "yes": {
      "text": "Toiletten",
    },
    "no": {
      "text": "keine Toiletten",
    }
  },
  "shower": {
    "yes": {
      "text": "Duschen",
    },
    "no": {
      "text": "keine Duschen",
    }
  },
  "drinking_water": {
    "yes": {
      "text": "Trinkwasser",
    },
    "no": {
      "text": "kein Trinkwasser",
    }
  },
  "power_supply": {
    "^(?!no).+$": {
      "text": "Stromanschluss",
    },
    "no": {
      "text": "kein Stromanschluss",
    }
  },
  "sanitary_dump_station": {
    "^(?!no).+$": {
      "text": "Sanitäre Entsorgungsstation",
    }
  },
  "shop": {
    "yes": {
      "text": "Laden",
    }
  },
  "laundry": {
    "yes": {
      "text": "Waschsalon",
    }
  },
  "washing_machine": {
    "yes": {
      "text": "Waschmaschine",
    }
  },
  "pub": {
    "yes": {
      "text": "Kneipe",
    }
  },
  "bar": {
    "yes": {
      "text": "Bar",
    }
  },
  "restaurant": {
    "yes": {
      "text": "Restaurant",
    }
  },
  "fast_food": {
    "yes": {
      "text": "Schnellimbiss",
    }
  },
  "telephone": {
    "yes": {
      "text": "Fernsprecher",
    }
  },
  "post_box": {
    "yes": {
      "text": "Briefkasten",
    }
  },
  "playground": {
    "yes": {
      "text": "Spielplatz",
    }
  },
  "internet_access": {
    "yes": {
      "text": "Internetzugang",
    },
    "no": {
      "text": "kein Internetzugang",
    },
    "wifi": {
      "text": "WLAN",
    },
    "wlan": {
      "text": "WLAN",
    }
  },
  "bbq": {
    "yes": {
      "text": "Grill",
    }
  },
  "dog": {
    "yes": {
      "text": "Hunde erlaubt"
    },
    "no": {
      "text": "Hunde verboten"
    },
    "leashed": {
      "text": "Hunde angeleint"
    }
  },
  "motor_vehicle": {
    "yes": {
      "text": "Kfz",
    },
    "no": {
      "text": "keine Kfz",
    }
  },
  "openfire": {
    "yes": {
      "text": "Feuer machen erlaubt",
    },
    "no": {
      "text": "Feuer machen verboten",
    }
  },
  "sauna": {
    "yes": {
      "text": "Sauna",
    }
  },
  "miniature_golf": {
    "yes": {
      "text": "Minigolf"
    }
  }
}
}

sports = {
'de': {
'swimming': 'Schwimmbad',
'golf': 'Golfplatz',
"tennis": "Tennis",
"soccer": "Fußball",
"archery": "Bogensport",
"baseball": "Baseball",
"basketball": "Basketball",
"beachvolleyball": "Beach Volleyball",
"equestrian": "Reitplatz",
"table_tennis": "Tischtennis",
"volleyball": "Volleyball"
},
'en': {
'swimming': 'pool',
'golf': 'golf',
"tennis": "tennis",
"soccer": "soccer",
"archery": "archery",
"baseball": "baseball",
"basketball": "basketball",
"beachvolleyball": "beach volleyball",
"equestrian": "riding arena",
"table_tennis": "table tennis",
"volleyball": "volleyball"
}
}

parser = argparse.ArgumentParser(
    description='Generate OpenCampingMap GARMIN POI file for single or all countries or all')

parser.add_argument('-s', '--sitemap', default='https://opencampingmap.org/sitemap.xml')

parser.add_argument('-u', '--csurl', default='https://opencampingmap.org/getcampsites')

parser.add_argument('-o', '--outdir', default='gpx')

parser.add_argument('-l', '--lang', default='en', choices=['en', 'de'])

exclusive_group = parser.add_mutually_exclusive_group()
exclusive_group.add_argument('-c', '--country', default='all', help='Country to generate data for')
exclusive_group.add_argument('-b', '--bbox', nargs=4, help='Bounding box to generate data for')

args = parser.parse_args()

gpxhead ="""<?xml version="1.0" encoding="UTF-8"?>
<gpx xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.topografix.com/GPX/1/1" creator="gen_garmin_poi" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd " version="1.1">
"""

ccodes = json.load(open('country-names.json'))
addrfm = AddressFormatter()

# try to generate an address string if we have an addres in the data
def genaddr(tags):
  addr = {}
  addrkeys=0
  # count keys starting with "addr:"
  for k in tags.keys():
    if k.startswith('addr:'):
      addrkeys+=1
  if (addrkeys > 2):
    if ('addr:housenumber' in tags):
      addr['house_number'] = tags['addr:housenumber']
    if ('addr:place' in tags):
      addr['road'] = tags['addr:place']
    if ('addr:street' in tags):
      addr['road'] = tags['addr:street']
    if ('addr:city' in tags):
      addr['city'] = tags['addr:city']
    if ('addr:postcode' in tags):
      addr['postcode'] = tags['addr:postcode'];
    if ('addr:country' in tags):
      addr['country'] = ccodes[ tags['addr:country'].upper()].upper()
    res=""
    for l in addrfm.format(addr,'EN').split('\n'):
      if l != '':
        res += l+'\n'
    return res.strip()
  return ''

def gendesc(prop):
  desc=""
  if 'operator' in prop:
    desc+=prop['operator'] +'\n'
    prefix='\n'
  else:
    prefix=''
  # contact Information
  if 'website' in prop:
    desc+=prefix+prop['website'] +'\n'
    prefix=''
  if 'email' in prop:
    desc+=prefix+prop['email'] +'\n'
    prefix=''
  if 'phone' in prop:
    desc+=prefix+prop['phone'] +'\n'
    prefix=''
  # ignore fax as it is usually unavailable outdoors
  
  addr=genaddr(prop)
  if addr != '':
    desc+='\n'+addr+'\n'
    
  facilities = ""
  for f in features[args.lang]:
    if f in prop:
        for v in features[args.lang][f]:
          if re.match(v,prop[f]):
            facilities += features[args.lang][f][v]['text']+ ', '
            break
  
  # Also append sport facilities
  if not 'sport' in prop:
    prop['sport'] = []
  
  if 'swimming_pool' in prop:
    if prop['swimming_pool'] == 'yes':
      prop['sport'].append('swimming')
  
  if 'golf_course' in prop:
    if prop['golf_course'] == 'yes':
      prop['sport'].append('golf')
  
  for s in prop['sport']:
    # ignore 'multi'
    if 's' == 'multi':
      continue
    if s in sports[args.lang]:
      facilities += sports[args.lang][s]+ ', '
    else:
      facilities += s + ', '
  
  facilities = facilities.strip(', ')
  if facilities != "":
    desc+='\n'+facilities+'\n'
  
  return desc.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

def genpoi(country, bbox=None):
  ofopen = {}
  for cscat in cscats:
    ofopen[cscat]=None
    ofopen[cscat+'_private']=None
  
  if bbox is None:
    cspoi=requests.get(args.csurl+'?country='+country)
    prefix=country+'_'
  else:
    bbstr=bbox[0]+','+bbox[1]+','+bbox[2]+','+bbox[3]
    cspoi=requests.get(args.csurl+'?bbox='+bbstr)
    prefix=''
    
  jsondata=cspoi.json()
  for cs in jsondata['features']:
    cscat=cs['properties']['category']
    if 'access' in cs['properties']:
      if cs['properties']['access'] in private_values:
        cscat=cs['properties']['category']+'_private'
    # write data to open file open and initialize
    # if not already done
    if ofopen[cscat] is None:
      ofopen[cscat] = open(os.path.join(args.outdir,prefix+cscat+'.gpx'), "w+")
      ofopen[cscat].write(gpxhead)
    
    if cs['geometry'] is None:
      sys.stderr.write("ignoring invalid object: %s\n" % cs['id'])
      continue
    
    ofopen[cscat].write('  <wpt lat="%s" lon="%s">\n' %(cs['geometry']['coordinates'][1],cs['geometry']['coordinates'][0]))
    if 'name' in cs['properties']:
      ofopen[cscat].write('    <name>%s</name>\n' % cs['properties']['name'].replace('&','&amp;').replace('<','&lt;').replace('>','&gt;'))
    desc=gendesc(cs['properties'])
    if desc != "":
      ofopen[cscat].write('    <desc>%s</desc>\n' % desc)
    ofopen[cscat].write('  </wpt>\n')
  
  for cscat in cscats:
    if ofopen[cscat] is not None:
      ofopen[cscat].write('</gpx>\n')
      ofopen[cscat].close()
      ofopen[cscat]=None
    if ofopen[cscat+'_private'] is not None:
      ofopen[cscat+'_private'].write('</gpx>\n')
      ofopen[cscat+'_private'].close()
      ofopen[cscat+'_private']=None

if not os.path.isdir(args.outdir):
  sys.stderr.write("Output directory >%s< does not exist!\n" % args.outdir)
  sys.exit(1)

if (args.bbox) == None:
  if args.country == 'all':
    # fetch list of available countries via OpenCampingMap sitemap.xml
    # and call genpoi for all of them
    smxml=requests.get(args.sitemap)
    root = ET.fromstring(smxml.text)
    for url in root.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}sitemap'):
      loc = url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text
      genpoi(os.path.splitext(os.path.basename(loc))[0])
  else:
    genpoi(args.country)
else:
  genpoi(None,args.bbox)
  
sys.exit(0)

