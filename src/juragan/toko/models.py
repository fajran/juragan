from django.db import models
from django.contrib.auth.models import User

from juragan import provinsi as prov

class Toko(models.Model):
    user = models.ForeignKey(User)

    nama = models.CharField(max_length=200)
    website = models.URLField(null=True, blank=True)
    email = models.EmailField()
    telepon = models.CharField(max_length=200, null=True, blank=True)

    deskripsi = models.TextField(null=True, blank=True)

    alamat = models.CharField(max_length=200)
    kota = models.CharField(max_length=100)
    provinsi = models.CharField(max_length=5,
                                choices=prov.daftar_provinsi)
    geo_lintang = models.FloatField(null=True, blank=True)
    geo_bujur = models.FloatField(null=True, blank=True)

    produk = models.TextField(null=True, blank=True)
    katalog = models.URLField(null=True, blank=True)

    aktif = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Daftar Toko"

    def __unicode__(self):
        return "%s (%s)" % (self.nama, self.kota)

    def nama_provinsi(self):
        return provinsi.get_nama(self.provinsi)

