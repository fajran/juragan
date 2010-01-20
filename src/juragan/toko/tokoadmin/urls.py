from django.conf.urls.defaults import *

from juragan.toko.tokoadmin import views

urlpatterns = patterns('',
    (r'^(?P<toko_id>\d+)/$', views.ubah),
    (r'^tambah/$', views.tambah),
    (r'^hapus/(?P<toko_id>\d+)/$', views.hapus),
    (r'^$', views.index),
)

