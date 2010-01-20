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
    data = gmaps_ambil_alamat(data)

    akurasi = data['AddressDetails']['Accuracy']

    area = data['AddressDetails']['Country']['AdministrativeArea']

    provinsi, kota, alamat = None, None, None

    if akurasi >= 2:
        provinsi = area['AdministrativeAreaName']
        provinsi = prov.get_kode(provinsi)

    if akurasi >= 4:
        kota = area['Locality']['LocalityName']

    if akurasi >= 6:
        alamat = area['Locality']['DependentLocality'] \
                     ['Thoroughfare']['ThoroughfareName']

    data = {'lokasi': {'provinsi': provinsi,
                       'kota': kota,
                       'alamat': alamat}}

    return respon_json_ok(data)

def lokasi(request, posisi):
    if not _validasi_posisi(posisi):
        raise Http404()

    param = {
        'q': posisi,
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

