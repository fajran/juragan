from django.conf.urls.defaults import *
from juragan.lokasi import views

urlpatterns = patterns('',
    (r'^(?P<posisi>.+)/$', views.lokasi)
)

