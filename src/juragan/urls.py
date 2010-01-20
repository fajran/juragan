from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import direct_to_template, redirect_to
from django.contrib.auth import views as auth_views

from django.contrib import admin
admin.autodiscover()

from juragan.lokasi import urls as lokasi_urls
from juragan.toko import urls as toko_urls

urlpatterns = patterns('',
    (r'^\+media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

    (r'^admin/', include(admin.site.urls)),

    (r'^toko/', include(toko_urls)),
    (r'^lokasi/', include(lokasi_urls)),

    (r'^cari/$', 'juragan.toko.views.cari'),

    (r'^bantuan/$', direct_to_template, 
        {'template': 'bantuan.html'}),

    (r'^$', redirect_to, {'url': '/cari/'}),
)

urlpatterns += patterns('',
    (r'^login/',
        auth_views.login,
        {'template_name': 'login.html'}),
    (r'^logout/$',
        auth_views.logout,
        {'template_name': 'logout.html'}),
    (r'^accounts/password/change/$',
        auth_views.password_change,
        {'template_name': 'password_change.html'}),
    (r'^accounts/password/change/done/$',
        auth_views.password_change_done,
        {'template_name': 'password_change_done.html'}),
    (r'^accounts/password/reset/$',
        auth_views.password_reset,
        {'template_name': 'password_reset.html'}),
    (r'^accounts/password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.password_reset_confirm,
        {'template_name': 'password_reset_confirm.html'}),
    (r'^accounts/password/reset/complete/$',
        auth_views.password_reset_complete,
        {'template_name': 'password_reset_complete.html'}),
    (r'^accounts/password/reset/done/$',
        auth_views.password_reset_done,
        {'template_name': 'password_reset_done.html'}),
)
