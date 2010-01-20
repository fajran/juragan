from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # (r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'index.html'}),
    (r'^\+media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('registration.backends.default.urls')),

    (r'^daftar/$', 'juragan.views.daftar'),
    (r'^cari/$', 'juragan.views.cari'),
    (r'^lokasi/(?P<posisi>.+)/$', 'juragan.views.lokasi'),
    (r'^toko/(?P<toko_id>\d+)/$', 'juragan.views.toko'),
    (r'^$', 'juragan.views.index'),
)
