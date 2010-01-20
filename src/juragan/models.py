from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

# Daftar provinsi Sumber: Wikipedia
# http://id.wikipedia.org/wiki/Daftar_provinsi_Indonesia

daftar_provinsi = (
	('ID-AC','Nangro Aceh Darussalam'),
	('ID-SU','Sumatera Utara'),
	('ID-SB','Sumatera Barat'),
	('ID-RI','Riau'),
	('ID-JA','Jambi'),
	('ID-SS','Sumatera Selatan'),
	('ID-BE','Bengkulu'),
	('ID-LA','Lampung'),
	('ID-BB','Bangka Belitung'),
	('ID-KR','Kepulauan Riau'),
	('ID-JK','Jakarta'),
	('ID-JB','Jawa Barat'),
	('ID-JT','Jawa Tengah'),
	('ID-YO','Yogyakarta'),
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
	('ID-PB','Papua Barat'), # Irian Jaya Barat
	('ID-PA','Papua'), # Irian Jaya Timur, Irian Jaya
)

daftar_provinsi_map_reverse = {
    "irian jaya barat": "ID-PB",
    "irian jaya timur": "ID-PA",
    "irian jaya": "ID-PA",
}
for k, v in daftar_provinsi:
    daftar_provinsi_map_reverse[v.lower()] = k

daftar_provinsi_map = {}
for k, v in daftar_provinsi:
    daftar_provinsi_map[k] = v

# Alternatif nama menurut Google Maps

class Toko(models.Model):
    user = models.ForeignKey(User)

    nama = models.CharField(max_length=200)
    website = models.URLField(null=True, blank=True)
    email = models.EmailField()
    telepon = models.CharField(max_length=200, null=True, blank=True)

    deskripsi = models.TextField(null=True, blank=True)

    alamat = models.CharField(max_length=200)
    kota = models.CharField(max_length=100)
    provinsi = models.CharField(max_length=5, choices=daftar_provinsi)
    geo_lintang = models.FloatField(null=True, blank=True)
    geo_bujur = models.FloatField(null=True, blank=True)

    produk = models.TextField(null=True, blank=True)
    katalog = models.URLField(null=True, blank=True)

    aktif = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Daftar Toko"

    def __unicode__(self):
        return "%s (%s)" % (self.nama, self.kota)


admin.site.register(Toko)

