from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from profiles.models import Profile, Post, Comment
from tags.models import Tag
from utils import siteHelpers

#404
def openspace404(request):
    return render(request, 'openspace/help.html')

#/
def index(request):
    context = {
        'profiles': Profile.objects.filter(species=0).order_by('-interest')[:10],
        'posts': Post.objects.order_by('-interest')[:10],
        'tags': Tag.objects.exclude(name='prey').exclude(name='graze').order_by('-interest')[:20],
        'recent_comments': Comment.objects.order_by('-date_published')[:15],
        'profile_count': Profile.objects.count(),
        'post_count': Post.objects.count(),
        'greeting' : request.session['show_greeting']
    }
    request.session['show_greeting'] = False
    return render(request, 'openspace/index.html', context)

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
        rawResults = Post.objects.filter(post_content__contains=query).order_by('-interest')
        results = Paginator(rawResults, 25)
        page = request.GET.get('page')
        try:
            pagedResults = results.page(page)
        except PageNotAnInteger:
            pagedResults = results.page(1)
        except EmptyPage:
            pagedResults = results.page(results.num_pages)
    context = {
        'search_query': query,
        'search_results': pagedResults,
        'total_results': rawResults.count(),
        'queries': queriesSubset
    }
    return render(request, 'openspace/search-results.html', context)

#info/
def infoPage(request):
    context = {
        'profile_count': Profile.objects.count(),
        'post_count': Post.objects.count(),
    }
    context.update(siteHelpers.parkDataProcessor())
    return render(request, 'openspace/info.html', context)

#help/
def helpPage(request):
    return render(request, 'openspace/help.html')

#credits/
def creditsPage(request):
    return render(request, 'openspace/credits.html')

#changebg/
def changeBg(request):
    request.session['page_background'] = siteHelpers.bgSelect(request.session['page_background'])
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))