from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # (r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'index.html'}),
    (r'^\+media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('registration.backends.default.urls')),

    (r'^cari/$', 'juragan.views.cari'),
    (r'^lokasi/(?P<posisi>.+)/$', 'juragan.views.lokasi'),
    (r'^toko/daftar/$', 'juragan.views.daftar'),
    (r'^toko/(?P<toko_id>\d+)/$', 'juragan.views.toko'),
    (r'^distributor/$', 'juragan.views.distributor'),
    (r'^bantuan/$', direct_to_template, 
        {'template': 'bantuan.html'}),
    (r'^$', 'juragan.views.index'),
)
