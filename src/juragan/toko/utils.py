import urllib
import urllib2

try:
    import json
except ImportError:
    import simplejson as json

from django.conf import settings

from juragan.utils import gmaps_ambil_alamat
from juragan.toko.models import Toko

def cari_posisi(*param):
    query = ', '.join(param + ('Indonesia',))

    args = {'q': query,
            'output': 'json',
            'sensor': False,
            'key': settings.GMAPS_API_KEY}

    args = urllib.urlencode(args)
    url = "http://maps.google.com/maps/geo?%s" % args

    res = urllib2.urlopen(url).read()
    data = json.loads(res)

    status = data['Status']['code']

    if status != 200:
        return False, status

    alamat = gmaps_ambil_alamat(data)
    lng, lat = alamat['Point']['coordinates'][0:2]

    return True, {'lat': lat,
                  'lng': lng,
                  'alamat': alamat['address']}

def _bandingkan_jarak(a, b):
    if a[1] < b[1]:
        return -1
    elif a[1] > b[1]:
        return 1
    return 0

def cari_terdekat(lat, lng, max=5):
    daftar = []

    toko = Toko.objects.filter(aktif=True) \
            .exclude(geo_lintang=None) \
            .exclude(geo_bujur=None)

    for t in toko:
        tlat = t.geo_lintang
        tlng = t.geo_bujur
        dlat = tlat-lat
        dlng = tlng-lng
        jarak = dlat*dlat + dlng*dlng

        daftar.append((t, jarak))

    return map(lambda x: x[0], 
               sorted(daftar, _bandingkan_jarak)[0:max])


