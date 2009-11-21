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

def daftar(request):
    format = request.GET.get('format', 'html')
    if format == 'json':
        data = {}
        data['juragan'] = []

        juragan = models.Juragan.objects.all()
        for item in juragan:
            d = {
                'nama': item.nama,
                'website': item.website,
                'email': item.email,
                'toko': []
            }

            toko = models.Toko.objects.filter(juragan=item)
            for t in toko:
                dd = {
                    'alamat': t.alamat,
                    'kota': t.kota,
                    'provinsi': models.daftar_provinsi_map[t.provinsi],
                    'x': t.geo_bujur,
                    'y': t.geo_lintang
                }
                d['toko'].append(dd)

            data['juragan'].append(d)

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
            map = {}
            if status == 200:
                map['x'] = data['Placemark'][0]['Point']['coordinates'][0]
                map['y'] = data['Placemark'][0]['Point']['coordinates'][1]
                param['map'] = map

                print map['y'], map['x']

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

