from django import forms
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.conf import settings

from juragan import provinsi as prov
from juragan.toko.models import Toko
from juragan.utils import respon_json_ok, respon_json_error
from juragan.toko import utils

class CariForm(forms.Form):
    alamat = forms.CharField(max_length=200, required=False)
    kota = forms.CharField(max_length=100, required=False)
    provinsi = forms.ChoiceField(choices=prov.daftar_provinsi)


INDONESIA = {'lat': -0.7892750,
             'lng': 113.9213270,
             'alamat': 'Indonesia'}

def _cari_posisi(*param):
    param = filter(lambda x: x != '',
                map(lambda x: x.strip(), 
                    filter(lambda x: x is not None, param)))
    
    while len(param) > 0:
        status, hasil = utils.cari_posisi(*param)
        if not status:
            if hasil in [602, 603]:
                param = param[1:]
            else:
                return INDONESIA
        else:
            return hasil

    return INDONESIA

def posisi(request):
    toko = Toko.objects.filter(aktif=True)

    posisi = []
    for t in toko:
        posisi.append({'id': t.id,
                       'lat': t.geo_lintang,
                       'lng': t.geo_bujur,
                       'nama': t.nama,
                       'alamat': t.alamat,
                       'kota': t.kota,
                       'provinsi': t.nama_provinsi(),
                       'website': t.website})

    data = {'posisi': posisi}
    return respon_json_ok(data)

def toko(request, toko_id):
    toko = get_object_or_404(Toko, pk=toko_id, aktif=True)

    produk = toko.produk
    if produk is not None:
        produk = filter(lambda x: x != '',
                    map(lambda x: x.strip(),
                        produk.splitlines()))

    return render_to_response('toko/toko.html', {'toko': toko,
                                                 'produk': produk},
                              context_instance=RequestContext(request))

def cari(request):
    ctx = {}
    
    if request.method == 'POST':
        form = CariForm(request.POST)
        if form.is_valid():
            alamat = form.cleaned_data['alamat']
            kota = form.cleaned_data['kota']
            provinsi = prov.get_nama(form.cleaned_data['provinsi'])

            posisi = _cari_posisi(alamat, kota, provinsi)
            dekat = utils.cari_terdekat(posisi['lat'], posisi['lng'])

            ctx['posisi'] = posisi
            ctx['dekat'] = dekat

    else:
        form = CariForm()

    ctx['key'] = settings.GMAPS_API_KEY
    ctx['form'] = form

    return render_to_response('toko/cari.html', ctx,
                              context_instance=RequestContext(request))

def index(request):
    toko = Toko.objects.filter(aktif=True)

    daftar = {}
    for t in toko:
        p = t.provinsi
        d = daftar.get(p, {'nama': prov.get_nama(p),
                           'toko': []})
        d['toko'].append(t)
        daftar[p] = d

    hasil = []
    for k, v in prov.daftar_provinsi:
        p = daftar.get(k, None)
        if p is not None:
            hasil.append(p)

    return render_to_response('toko/index.html', {'daftar': hasil},
                              context_instance=RequestContext(request))

