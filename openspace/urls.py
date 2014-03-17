from django.conf.urls import patterns, include, url
from django.contrib import admin
from openspace import views
from django.views.decorators.cache import cache_page
admin.autodiscover()

handler404 = 'views.openspace404'
#handler500 = 'views.openspace500'

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),
    url(r'^info/$', cache_page(views.dataPage, 60*15), name='dataPage'),
    url(r'^help/$', cache_page(views.helpPage, 6), name='helpPage'),
    url(r'^credits/$', cache_page(views.creditsPage, 6), name='creditsPage'),
    url(r'^profiles/', include('apps.profiles.urls', namespace='profiles')),
    url(r'^tags/', include('apps.tags.urls', namespace='tags')),
    url(r'^search/$', views.parkSearch, name='parkSearch'),
    url(r'^topprofiles/$', cache_page(views.topProfiles, 60*5), name='topProfiles'),
    url(r'^topposts/$', cache_page(views.topPosts, 60*5), name='topPosts'),
    url(r'^changebg/$', views.changeBg, name='changeBg'),
    url(r'^humanentry/(?P<human_key>\d+)$', views.humanEntry, name='humanEntry'),
    url(r'^resetsession/$', views.resetSession, name='resetSession'),
)