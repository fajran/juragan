import urllib
import urllib2

try:
    import json
except ImportError:
    import simplejson as json

from django.http import HttpResponse, Http404
from django.conf import settings

from juragan import provinsi as prov
from juragan.utils import respon_json_ok, respon_json_error, \
                          gmaps_ambil_alamat

def _validasi_posisi(posisi):
    try:
        lat, lng = map(lambda x: float(x), posisi.split(','))
    except ValueError:
        return False
    return True

def _ambil_lokasi(data):

    negara = None
    provinsi = None
    provinsi_nama = None
    kota = None
    alamat = None
    lat = None
    lng = None
    west = None
    east = None
    north = None
    south = None

    try:
        data = gmaps_ambil_alamat(data)
        print data
    
        lng, lat = data['Point']['coordinates'][0:2]
        box = data['ExtendedData']['LatLonBox']
        north = box['north']
        south = box['south']
        east = box['east']
        west = box['west']
    
        area = None
    
        akurasi = data['AddressDetails']['Accuracy']
    
        if akurasi >= 1:
            negara = data['AddressDetails']['Country']['CountryName']
            area = data['AddressDetails']['Country'].get('AdministrativeArea', 
                                                          None)
    
        if akurasi >= 2:
            provinsi_nama = area['AdministrativeAreaName']
            provinsi = prov.get_kode(provinsi_nama)
    
        if akurasi >= 4:
            kota = area['Locality']['LocalityName']
    
        if akurasi >= 6:
            alamat = area['Locality']['DependentLocality'] \
                         ['Thoroughfare']['ThoroughfareName']

    except (ValueError, IndexError, KeyError):
        pass
    
    data = {'lokasi': {'negara': negara,
                       'provinsi': provinsi,
                       'provinsi_nama': provinsi_nama,
                       'kota': kota,
                       'alamat': alamat,
                       'lat': lat,
                       'lng': lng,
                       'north': north,
                       'south': south,
                       'east': east,
                       'west': west}}

    return respon_json_ok(data)

def lokasi(request):
    posisi = request.GET.get('ll', None)
    alamat = request.GET.get('alamat', None)
    kota = request.GET.get('kota', None)
    provinsi = request.GET.get('provinsi', None)

    if posisi is not None:
        if not _validasi_posisi(posisi):
            raise Http404()
        q = posisi
    else:
        provinsi = prov.get_nama(provinsi)
        q = ', '.join(filter(lambda x: x != '',
                        map(lambda x: x.strip(),
                            filter(lambda x: x is not None,
                                [alamat, kota, provinsi, 'Indonesia']))))

    param = {
        'q': q,
        'output': 'json',
        'sensor': 'false',
        'key': settings.GMAPS_API_KEY
    }
    url = "http://maps.google.com/maps/geo?%s" % urllib.urlencode(param)

    try:
        txt = urllib2.urlopen(url).read()
        data = json.loads(txt)
    except (ValueError, urllib2.URLError):
        return HttpResponse(status=502) # Bad Gateway

    if data['Status']['code'] == 200:
        return _ambil_lokasi(data)
    else:
        return respon_json_error(data["Status"])

