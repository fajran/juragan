from django.http import HttpResponse

try:
    import json
except ImportError:
    import simplejson as json

_json_content_type = 'text/plain'

def respon_json_ok(data):
    data['stat'] = 'ok'
    return HttpResponse(json.dumps(data), 
                        content_type=_json_content_type)

def respon_json_error(kode):
    data = json.dumps({'stat': 'error',
                       'kode': kode})

    status = kode
    if kode >= 600:
        status = 500

    return HttpResponse(data, status=status,
                        content_type=_json_content_type)

def gmaps_ambil_alamat(data):
    return data['Placemark'][0]

    # TODO urut berdasar akurasi
    items = []
    for d in data['Placemark']:
        items.append((d['AddressDetails']['Accuracy'], d))
    daftar = sorted(items, cmp_alamat)

    return daftar[0][1]
    
    
