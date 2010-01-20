from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import direct_to_template, redirect_to

from django.contrib import admin
admin.autodiscover()

from juragan.lokasi import urls as lokasi_urls
from juragan.toko import urls as toko_urls

urlpatterns = patterns('',
    (r'^\+media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('registration.backends.default.urls')),

    (r'^toko/', include(toko_urls)),
    (r'^lokasi/', include(lokasi_urls)),

    (r'^cari/$', 'juragan.toko.views.cari'),

    (r'^bantuan/$', direct_to_template, 
        {'template': 'bantuan.html'}),

    (r'^$', redirect_to, {'url': '/cari/'}),
)
