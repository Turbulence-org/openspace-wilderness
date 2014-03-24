from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from apps.profiles.models import Profile, Post, Comment
from apps.tags.models import Tag
from libs import siteHelpers
from libs.siteEnums import System, Species
import urllib

#404
def openspace404(request):
    return render(request, 'help.html')

#500
def openspace500(request):
    return HttpResponseRedirect('https://s3.amazonaws.com/openspacemedia/error/os500.html')

#/
def index(request):
    context = {
        'profiles': Profile.objects.filter(species=Species.abandoned).order_by('-interest')[:10],
        'posts': Post.objects.order_by('-interest')[:10],
        'tags': Tag.objects.filter(id__gt=System.reservedTags).order_by('-interest')[:20],
        'recent_comments': Comment.objects.order_by('-date_published')[:5],
        'profile_count': Profile.objects.count(),
        'post_count': Post.objects.count(),
    }
    context.update(siteHelpers.parkDataProcessor())
    return render(request, 'index.html', context)

#search/
def parkSearch(request):
    """Queries post_content of Post objects only. Returns paginated set.
    
    Retrieves a string via GET for a contains query.
    """
    queriesSubset = request.GET.copy()
    if queriesSubset.has_key('page'):
        del queriesSubset['page']
    results = None
    posts = None
    if 'query' in request.GET and request.GET['query']:
        query = request.GET['query']
        unpagedResults = Post.objects.filter(post_content__contains=query).order_by('-interest').prefetch_related('post_profile')
        pagedResults = siteHelpers.paginatorMaker(unpagedResults, request.GET.get('page'), 25)
        heading = '[ ' + str(unpagedResults.count()) +' ] result for [ ' + query + ' ]'
    context = {
        'heading': heading,
        'paged_results': pagedResults,
        'search_query': query,
        'query': urllib.urlencode(queriesSubset) + '&'    
    }
    return render(request, 'search-results.html', context)

#info/
def dataPage(request):
    context = {
        'profile_count': Profile.objects.count(),
        'post_count': Post.objects.count(),
    }
    context.update(siteHelpers.parkDataProcessor())
    return render(request, 'data.html', context)

#help/
def helpPage(request):
    ranger = Profile.objects.filter(species=Species.system)[0]
    context = {
        'ranger_id': ranger.id,
        'ranger_icon': ranger.prettyPic
    }
    return render(request, 'help.html', context)

#credits/
def creditsPage(request):
    return render(request, 'credits.html')

#changebg/
def changeBg(request):
    request.session['page_background'] = siteHelpers.bgSelect(request.session['page_background'])
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

#humanentry/3432452
def humanEntry(request, human_key):
    """Verifies that the user is human and not a bot creating multiple thousand new profiles."""
    secret_key = System.humanKey
    if int(human_key) == secret_key:
        request.session['is_human'] = True
        request.session['new_session'] = True
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

#nonewsession
def noNewSession(request):
    """Bypass creating a new profile but register as human."""
    request.session['is_human'] = True
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

#resetsession/
def resetSession(request):
    """Clears the whole user session and starts fresh."""
    request.session['new_session'] = True
    return redirect('index')
    
#topprofiles/
def topProfiles(request):
    unpagedProfiles = Profile.objects.exclude(visible=False).order_by('-interest')[:200]
    pagedResults = siteHelpers.paginatorMaker(unpagedProfiles, request.GET.get('page'), 50)
    context = {
        'heading': 'top [ 200 profiles ]',
        'paged_results': pagedResults
    }
    return render(request, 'profile-results.html', context)

#topposts/
def topPosts(request):
    unpagedPosts = Post.objects.order_by('-interest')[:100]
    pagedResults = siteHelpers.paginatorMaker(unpagedPosts, request.GET.get('page'), 25)
    context = {
        'heading': 'top [ 100 posts ]',
        'paged_results': pagedResults
    }
    return render(request, 'post-results.html', context)