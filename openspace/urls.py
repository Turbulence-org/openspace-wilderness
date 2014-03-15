from django.conf.urls import patterns, include, url
from django.contrib import admin
from openspace import views
admin.autodiscover()

handler404 = 'views.openspace404'

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),
    url(r'^info/$', views.infoPage, name='infoPage'),
    url(r'^help/$', views.helpPage, name='helpPage'),
    url(r'^credits/$', views.creditsPage, name='creditsPage'),
    url(r'^profiles/', include('apps.profiles.urls', namespace='profiles')),
    url(r'^tags/', include('apps.tags.urls', namespace='tags')),
    url(r'^search/$', views.parkSearch, name='parkSearch'),
    url(r'^topprofiles/$', views.topProfiles, name='topProfiles'),
    url(r'^topposts/$', views.topPosts, name='topPosts'),
    url(r'^changebg/$', views.changeBg, name='changeBg'),
    url(r'^resetsession/$', views.resetSession, name='resetSession'),
)