from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django import forms
from django.conf import settings

from juragan import models

import urllib2
import urllib

try:
    import json
except ImportError:
    import simplejson as json

def get_content(url):
    return urllib2.urlopen(url).read()

class Cari(forms.Form):
    produk = forms.CharField(max_length=200, required=False)
    alamat = forms.CharField(max_length=200)
    kota = forms.CharField(max_length=100)
    provinsi = forms.ChoiceField(choices=models.daftar_provinsi)

def cmp(a, b):
    if a[1] < b[1]:
        return -1
    elif a[1] > b[1]:
        return 1
    return 0

def cari_terdekat(x, y, max=5):
    daftar = []

    items = models.Toko.objects.all()
    for toko in items:
        tx = toko.geo_bujur
        ty = toko.geo_lintang
        dx = tx-x
        dy = ty-y
        jarak = dx*dx + dy*dy

        daftar.append((toko, jarak))

    return map(lambda x: x[0], sorted(daftar, cmp)[0:max])

def tambah_nama_provinsi(toko):
    toko.provinsi_nama = models.daftar_provinsi_map[toko.provinsi]
    return toko

def cmp_alamat(a, b):
    if a[0] < b[0]:
        return 1
    elif a[0] > b[0]:
        return -1
    else:
        return 0

def ambil_alamat(data):
    return data['Placemark'][0]
    items = []
    for d in data['Placemark']:
        items.append((d['AddressDetails']['Accuracy'], d))
    daftar = sorted(items, cmp_alamat)

    return daftar[0][1]

def daftar(request):
    format = request.GET.get('format', 'html')
    if format == 'json':
        data = {}
        data['toko'] = []

        toko = models.Toko.objects.all()
        for t in toko:
            dd = {
                'id': t.id,

                'email': t.email,
                'website': t.website,
                'nama': t.nama,

                'alamat': t.alamat,
                'kota': t.kota,
                'provinsi': models.daftar_provinsi_map[t.provinsi],

                'x': t.geo_bujur,
                'y': t.geo_lintang,
            }
            data['toko'].append(dd)

        data = json.dumps(data)
        return HttpResponse(data, content_type="text/plain")
    else:
        return HttpResponse('<h1>Daftar Juragan</h1>')

def cari(request):
    param = {}
    if request.method == 'POST':
        form = Cari(request.POST)
        if form.is_valid():
            kota = form.cleaned_data['kota']
            provinsi = form.cleaned_data['provinsi']
            alamat = form.cleaned_data['alamat']
            provinsi_nama = models.daftar_provinsi_map[provinsi]
            q = "%s, %s, %s, id" % (alamat, kota, provinsi_nama)
            param = {
                'q': q,
                'output': 'json',
                'sensor': 'false',
                'key': settings.GMAPS_API_KEY
            }
            url = "http://maps.google.com/maps/geo?%s" % urllib.urlencode(param)
            txt = get_content(url)
            data = json.loads(txt)
            status = data['Status']['code']
            peta = {}
            if status == 200:
                data = ambil_alamat(data)
                x = data['Point']['coordinates'][0]
                y = data['Point']['coordinates'][1]
                peta['x'] = x
                peta['y'] = y
                peta['alamat'] = data['address']
                peta['dekat'] = map(tambah_nama_provinsi, cari_terdekat(x, y))

                param['peta'] = peta

    else:
        form = Cari()
        
    param['key'] = settings.GMAPS_API_KEY
    param['form'] = form

    return render_to_response('cari.html', param,
        context_instance=RequestContext(request))

def index(request):
    form = Cari()
    return render_to_response('index.html', {
            'form': form
        }, context_instance=RequestContext(request))

def toko(request, toko_id):
    toko = get_object_or_404(models.Toko, pk=toko_id)

    produk = toko.produk
    if produk is not None:
        produk = filter(lambda x: x != '',
                    map(lambda x: x.strip(),
                        produk.splitlines()))

    toko.provinsi_nama = models.daftar_provinsi_map[toko.provinsi]

    return render_to_response('toko.html', {
            'toko': toko,
            'produk': produk,
        }, context_instance=RequestContext(request))

def lokasi(request, posisi):
    (y, x) = posisi.split(',')
    param = {
        'q': posisi,
        'output': 'json',
        'sensor': 'false',
        'key': settings.GMAPS_API_KEY
    }
    url = "http://maps.google.com/maps/geo?%s" % urllib.urlencode(param)
    txt = get_content(url)
    data = json.loads(txt)

    data = ambil_alamat(data)
    akurasi = data['AddressDetails']['Accuracy']

    aa = data['AddressDetails']['Country']['AdministrativeArea']

    provinsi, kota, alamat = None, None, None

    if akurasi >= 2:
        provinsi = aa['AdministrativeAreaName']
    if akurasi >= 4:
        kota = aa['Locality']['LocalityName']
    if akurasi >= 6:
        alamat = aa['Locality']['DependentLocality']['Thoroughfare']['ThoroughfareName']

    kota = None
    hasil = {'provinsi': provinsi, 'kota': kota, 'alamat': alamat}
    lokasi = json.dumps(hasil)

    return HttpResponse(lokasi, content_type="text/plain")


