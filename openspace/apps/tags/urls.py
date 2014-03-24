from django.conf.urls import patterns, url
from apps.tags import views

urlpatterns = patterns('',
    #/tags/
    url(r'^$', views.tags, name='tags'),
    #/tags/2/
    url(r'^(?P<tag_id>\d+)/$',
        views.tag, name='tag'),
    #/tags/2/selecttrail
    url(r'^(?P<tag_id>\d+)/selecttrail/$',
        views.selectTrail, name='selectTrail'),
)