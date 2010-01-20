# Daftar provinsi Sumber: Wikipedia
# http://id.wikipedia.org/wiki/Daftar_provinsi_Indonesia

daftar_provinsi = (
    ('ID-AC', 'Aceh'),
    ('ID-SU', 'Sumatera Utara'),
    ('ID-SB', 'Sumatera Barat'),
    ('ID-RI', 'Riau'),
    ('ID-JA', 'Jambi'),
    ('ID-SS', 'Sumatera Selatan'),
    ('ID-BE', 'Bengkulu'),
    ('ID-LA', 'Lampung'),
    ('ID-BB', 'Kepulauan Bangka Belitung'),
    ('ID-KR', 'Kepulauan Riau'),
    ('ID-JK', 'Daerah Khusus Ibukota Jakarta'),
    ('ID-JB', 'Jawa Barat'),
    ('ID-JT', 'Jawa Tengah'),
    ('ID-YO', 'Daerah Khusus Yogyakarta'),
    ('ID-JI', 'Jawa Timur'),
    ('ID-BT', 'Banten'),
    ('ID-BA', 'Bali'),
    ('ID-NB', 'Nusa Tenggara Barat'),
    ('ID-NT', 'Nusa Tenggara Timur'),
    ('ID-KB', 'Kalimantan Barat'),
    ('ID-KT', 'Kalimantan Tengah'),
    ('ID-KS', 'Kalimantan Selatan'),
    ('ID-KI', 'Kalimantan Timur'),
    ('ID-SA', 'Sulawesi Utara'),
    ('ID-ST', 'Sulawesi Tengah'),
    ('ID-SN', 'Sulawesi Selatan'),
    ('ID-SG', 'Sulawesi Tenggara'),
    ('ID-GO', 'Gorontalo'),
    ('ID-SR', 'Sulawesi Barat'),
    ('ID-MA', 'Maluku'),
    ('ID-MU', 'Maluku Utara'),
    ('ID-PB', 'Papua Barat'),
    ('ID-PA', 'Papua'),
)

_map = {}
for k, v in daftar_provinsi:
    _map[k] = v

# Alternatif nama menurut Google Maps
_mapr = {
    'nangro aceh darussalam': 'ID-AC',
    'bangka belitung': 'ID-BB',
    'jakarta': 'ID-JK',
    'yogyakarta': 'ID-YO',
    'irian jaya barat': 'ID-PB',
    'irian jaya timur': 'ID-PA',
    'irian jaya': 'ID-PA',
}
for k, v in daftar_provinsi:
    _map[v.lower()] = k

def get_nama(kode):
    return _map.get(kode, None)

def get_kode(provinsi):
    return _mapr.get(provinsi.lower(), None)

