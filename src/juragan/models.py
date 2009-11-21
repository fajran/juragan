from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

# Daftar provinsi Sumber: Wikipedia
# http://id.wikipedia.org/wiki/Daftar_provinsi_Indonesia

daftar_provinsi = (
	('ID-AC','Aceh'),
	('ID-SU','Sumatera Utara'),
	('ID-SB','Sumatera Barat'),
	('ID-RI','Riau'),
	('ID-JA','Jambi'),
	('ID-SS','Sumatera Selatan'),
	('ID-BE','Bengkulu'),
	('ID-LA','Lampung'),
	('ID-BB','Kepulauan Bangka Belitung'),
	('ID-KR','Kepulauan Riau'),
	('ID-JK','Daerah Khusus Ibukota Jakarta'),
	('ID-JB','Jawa Barat'),
	('ID-JT','Jawa Tengah'),
	('ID-YO','Daerah Istimewa Yogyakarta'),
	('ID-JI','Jawa Timur'),
	('ID-BT','Banten'),
	('ID-BA','Bali'),
	('ID-NB','Nusa Tenggara Barat'),
	('ID-NT','Nusa Tenggara Timur'),
	('ID-KB','Kalimantan Barat'),
	('ID-KT','Kalimantan Tengah'),
	('ID-KS','Kalimantan Selatan'),
	('ID-KI','Kalimantan Timur'),
	('ID-SA','Sulawesi Utara'),
	('ID-ST','Sulawesi Tengah'),
	('ID-SN','Sulawesi Selatan'),
	('ID-SG','Sulawesi Tenggara'),
	('ID-GO','Gorontalo'),
	('ID-SR','Sulawesi Barat'),
	('ID-MA','Maluku'),
	('ID-MU','Maluku Utara'),
	('ID-PB','Papua Barat'),
	('ID-PA','Papua'),
)

daftar_provinsi_map = {}
for k, v in daftar_provinsi:
    daftar_provinsi_map[k] = v

class Juragan(models.Model):
    user = models.ForeignKey(User, unique=True)
    nama = models.CharField(max_length=200)
    website = models.URLField(null=True, blank=True)
    email = models.EmailField()
    deskripsi = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Daftar Juragan"

    def __unicode__(self):
        return self.nama

class Produk(models.Model):
    nama = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "Daftar Produk"

    def __unicode__(self):
        return self.nama

class Toko(models.Model):
    juragan = models.ForeignKey(Juragan)
    alamat = models.CharField(max_length=200)
    kota = models.CharField(max_length=100)
    provinsi = models.CharField(max_length=5, choices=daftar_provinsi)
    geo_lintang = models.FloatField(null=True, blank=True)
    geo_bujur = models.FloatField(null=True, blank=True)

    produk = models.ManyToManyField(Produk, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Daftar Toko"

    def __unicode__(self):
        return "%s (%s)" % (self.juragan.nama, self.kota)


admin.site.register(Juragan)
admin.site.register(Toko)
admin.site.register(Produk)

