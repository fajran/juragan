from django.conf.urls.defaults import *

from juragan.toko.tokoadmin import views

urlpatterns = patterns('',
    (r'^(?P<toko_id>\d+)/$', views.toko),
    (r'^tambah/$', views.tambah),
    (r'^hapus/$', views.hapus),
    (r'^$', views.index),
)

