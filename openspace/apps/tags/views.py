from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from apps.profiles.models import Profile
from apps.tags.models import Tag
from libs import profileHelpers
from libs.siteEnums import Tags

#/tags/
def tags(request):
    context = {'tags': Tag.objects.exclude(interest=0).filter(id__gt=7).order_by('name')}
    return render(request, 'tags/trails.html', context)

#/tags/<tag_id>/
def tag(request, tag_id):
    tag = get_object_or_404(Tag.objects.prefetch_related('profile_set'), pk=tag_id)
    context = {
        'tag': tag,
        'tagscount': Tag.objects.all().count(),
        'profiles': Profile.objects.filter(tags=tag).order_by('-interest')
    }
    return render(request, 'tags/single-tag.html', context)
    
#/tags/<tag_id>/selecttrail/
def selectTrail(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    if tag.interest > 0:
        if request.session['selected_trail'] == tag.name:
            request.session['selected_trail'] = 'no'
            request.session['notification'] = 'trail'
        else:
            request.session['selected_trail'] = tag.name
            postOut = 'following the ' + tag.name + ' trail' 
            profileHelpers.makeUserPost(request, postOut, 'trail')
            request.session['notification'] = 'trail'
    else:
        request.session['notification'] = 'nope'
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

#/tags/deselecttrail/
def deselectTrail(request):
    request.session['selected_trail'] = 'no'
    request.session['notification'] = 'trail'
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))