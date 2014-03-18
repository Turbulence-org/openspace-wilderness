from django.conf.urls import patterns, include, url
from django.views.decorators.cache import cache_page
from django.contrib.sitemaps import FlatPageSitemap, GenericSitemap
from django.contrib import admin
from apps.profiles.models import Profile
from openspace import views
from sitemap import *

admin.autodiscover()

handler404 = 'views.openspace404'

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),
    url(r'^data/$', cache_page(views.dataPage, 0), name='dataPage'),
    url(r'^help/$', cache_page(views.helpPage, 0), name='helpPage'),
    url(r'^credits/$', cache_page(views.creditsPage, 0), name='creditsPage'),
    url(r'^profiles/', include('apps.profiles.urls', namespace='profiles')),
    url(r'^tags/', include('apps.tags.urls', namespace='tags')),
    url(r'^search/$', views.parkSearch, name='parkSearch'),
    url(r'^topprofiles/$', cache_page(views.topProfiles, 60*5), name='topProfiles'),
    url(r'^topposts/$', cache_page(views.topPosts, 60*5), name='topPosts'),
    url(r'^changebg/$', views.changeBg, name='changeBg'),
    url(r'^humanentry/(?P<human_key>\d+)$', views.humanEntry, name='humanEntry'),
    url(r'^resetsession/$', views.resetSession, name='resetSession'),
)


# here be monsters ... and sitemap garbage
info_dict = {
    'queryset': Profile.objects.all(),
    'date_field': 'date_published'
}

sitemaps = {
    'flatpages': FlatPageSitemap,
    'profiles': GenericSitemap(info_dict, priority=0.6),
}

urlpatterns += patterns('',
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
)