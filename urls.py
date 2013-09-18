from django.conf.urls.defaults import patterns, include, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
#my import
from django.utils.encoding import iri_to_uri

urlpatterns = patterns('',
    url(r'^$', 'goszak.view.start'),
    url(r'^media/([A-Za-z./\d]+)', 'goszak.base.staticFile'),
    # Examples:
    # url(r'^$', 'ec.views.home', name='home'),
    # url(r'^ec/', include('ec.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
)
