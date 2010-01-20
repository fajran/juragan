from django.conf.urls.defaults import *

from juragan.toko import views

urlpatterns = patterns('',
    (r'admin/', include('juragan.toko.tokoadmin.urls')),
    (r'^(?P<toko_id>\d+)/$', views.toko),
    (r'^cari/', views.cari),
    (r'^posisi/', views.posisi),
    (r'^$', views.index),
)

