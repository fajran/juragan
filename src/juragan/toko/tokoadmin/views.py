from django import forms
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response, redirect

from juragan import provinsi as prov

from juragan.toko.models import Toko

daftar_provinsi = (('', '-- pilih provinsi --'),) + prov.daftar_provinsi

class TokoForm(forms.Form):
    nama = forms.CharField(max_length=200)
    email = forms.EmailField()
    website = forms.URLField(required=False)
    telepon = forms.CharField(required=False)

    deskripsi = forms.CharField(widget=forms.Textarea,
                                required=False,
                                help_text="Informasi mengenai toko Anda. " \
                                          "Tulisan diformat dengan MarkDown.")


    alamat = forms.CharField(max_length=200)
    kota = forms.CharField(max_length=100)
    provinsi = forms.ChoiceField(choices=daftar_provinsi)

    geo_lintang = forms.FloatField(label="Lintang",
                                   required=False,
                                   help_text="Koordinat lintang (latitude).")
    geo_bujur = forms.FloatField(label="Bujur",
                                 required=False,
                                 help_text="Koordinat bujur (longitude).")

    produk = forms.CharField(widget=forms.Textarea,
                             required=False,
                             help_text="Tuliskan daftar produk yang Anda " \
                                            "sediakan. " \
                                       "Satu baris berisi satu produk.")

    katalog = forms.URLField(required=False,
                             help_text="URL menuju katalog online (jika ada).")


@login_required
def ubah(request, toko_id):
    toko = get_object_or_404(Toko, pk=toko_id, user=request.user)
    if request.method == 'POST':
        form = TokoForm(request.POST)
        if form.is_valid():
            for key in form.cleaned_data:
                toko.__dict__[key] = form.cleaned_data[key]
            toko.save()

            return redirect('/toko/%d/' % toko.id)

    else:
        form = TokoForm(toko.__dict__)

    ctx = {'form': form,
           'tipe': 'edit'}
    return render_to_response('toko/admin/tambah.html', ctx,
                              context_instance=RequestContext(request))

@login_required
def hapus(request):
    pass


@login_required
def tambah(request):
    ctx = {}

    if request.method == 'POST':
        form = TokoForm(request.POST)
        if form.is_valid():
            toko = Toko(**form.cleaned_data)
            toko.user = request.user
            toko.aktif = True
            toko.save()

            return redirect('/toko/%d/' % toko.id)
            
        ctx['form'] = form

    else:
        form = TokoForm()
        ctx['form'] = form

    return render_to_response('toko/admin/tambah.html', ctx,
                              context_instance=RequestContext(request))

@login_required
def index(request):
    toko = Toko.objects.filter(user=request.user)
    ctx = {'toko': toko}
    return render_to_response('toko/admin/index.html', ctx,
                              context_instance=RequestContext(request))
    
