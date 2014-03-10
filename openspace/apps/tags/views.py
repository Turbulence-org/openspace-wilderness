from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from apps.profiles.models import Profile
from apps.tags.models import Tag
from libs import profileHelpers
from libs.siteEnums import Tags, Notification

#/tags/
def tags(request):
    context = {'tags': Tag.objects.exclude(interest=0).order_by('name')}
    return render(request, 'tags/tags.html', context)

#/tags/<tag_id>/
def tag(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    context = {
        'tag': tag,
        'tagscount': Tag.objects.all().count(),
        'profiles': Profile.objects.filter(tags=tag).order_by('-interest')
    }
    return render(request, 'tags/single-tag.html', context)
    
#/tags/<tag_id>/selecttrail/
def selectTrail(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    if request.session['selected_trail'] == tag.name:
        request.session['selected_trail'] = 'no'
        request.session['notification'] = Notification.trail
    else:
        request.session['selected_trail'] = tag.name
        postOut = 'following the [ ' + tag.name + ' ] trail' 
        profileHelpers.makeUserPost(request, postOut, Tags.trails)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

#/tags/deselecttrail/
def deselectTrail(request):
    request.session['selected_trail'] = 'no'
    request.session['notification'] = Notification.trail
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))