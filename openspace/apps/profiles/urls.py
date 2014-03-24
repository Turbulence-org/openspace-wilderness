from django.conf.urls import patterns, url
from apps.profiles import views

urlpatterns = patterns('',
    #/profiles/
    url(r'^$', views.index, name='index'),
    #/profiles/5/
    url(r'^(?P<profile_id>\d+)/$',
        views.single, name='single'),
    #/profiles/5/friends/
    url(r'^(?P<profile_id>\d+)/friends/$',
        views.friends, name='friends'),
    #/profiles/5/tags/
    url(r'^(?P<profile_id>\d+)/tags/$',
        views.profileTags, name='profileTags'),
    #/profiles/5/death/
    url(r'^(?P<profile_id>\d+)/death/$',
        views.profileDeath, name='profileDeath'),
    #/profiles/5/addtags/
    url(r'^(?P<profile_id>\d+)/addtags/$',
        views.addProfileTags, name='addProfileTags'),
    #/profiles/5/profileinterest/
    url(r'^(?P<profile_id>\d+)/profileinterest/$',
        views.profileInterest, name='profileInterest'),
    #/profiles/5/makefriend/
    url(r'^(?P<profile_id>\d+)/makefriend/$',
        views.makeFriend, name='makeFriend'),
    #/profiles/5/post/5/
    url(r'^(?P<profile_id>\d+)/post/(?P<post_id>\d+)/$',
        views.singlePost, name='singlePost'),
    #/profiles/5/post/5/addtags/
    url(r'^(?P<profile_id>\d+)/post/(?P<post_id>\d+)/addtags/$',
        views.addPostTags, name='addPostTags'),
    #/profiles/post/5/postinterest/
    url(r'^post/(?P<post_id>\d+)/postinterest/$',
        views.postInterest, name='postInterest'),
    #/profiles/5/post/5/addcomment/
    url(r'^(?P<profile_id>\d+)/post/(?P<post_id>\d+)/addcomment/$',
        views.addComment, name='addComment'),
    #/profiles/5/eatprofile/
    url(r'^(?P<profile_id>\d+)/eatprofile/$',
        views.eatProfile, name='eatProfile'),
    #/profiles/5/graze/
    url(r'^(?P<profile_id>\d+)/graze/$',
        views.grazeProfile, name='grazeProfile'),
    #/profiles/5/post/5/graze/
    url(r'^(?P<profile_id>\d+)/post/(?P<post_id>\d+)/graze/$',
        views.grazePost, name='grazePost'),
    #/profiles/createprofile/2/
    url(r'^createprofile/(?P<species_id>\d+)/$',
        views.createProfile, name='createProfile'),
)