from django.contrib.staticfiles.templatetags.staticfiles import static
from django.db.models import Count
from apps.profiles.models import Profile, Post
from apps.tags.models import Tag
from libs.siteEnums import Species
from libs.auxHelpers import returnCount
from random import randint
from sys import path
import os, fnmatch, re

def fairPlay(request):
    """Returns True if current session_profile is active and page should drain energy."""
    path = request.get_full_path()
    tprof = Profile.objects.get(id=request.session['session_id'])
    fairUrls = ['changebg', 'addtags', 'postinterest',
        'profileinterest', 'addcomment', 'admin', 'tags', 'friends']
    if not tprof.isActive:
        return False
    if 'profiles' not in path:
        return False
    for url in fairUrls:
        if url in path:
            return False
    return True

def excludeUrls(path):
    """Returns True if current location is in the list of excluded urls."""
    if 'profiles' not in path:
        return True
    exclude = ['help', 'info', 'credits', 'tags', 'friends']
    for e in exclude:
        if e in path:
            return True
    return False

def isPost(request):
    """Returns True if location is a single post for profileHelpers.grazePost()."""
    if 'post' in request.get_full_path():
        return True

def isSelf(request):
    """Returns True is current nav_id is same as session."""
    if int(request.session['nav_id']) == int(request.session['session_id']):
        return True
    return False

def isKosher(request):
    """Returns True if current Profile is grazable by Forager type Profile."""
    if not isSelf(request) and request.session['session_species'] == Species.forager:
        if not Profile.objects.get(id=request.session['nav_id']).isActive and not excludeUrls(request.get_full_path()):
            return True
    return False

def isPrey(request):
    """Returns True if current Profile is edible by Predator type Profile."""
    if not isSelf(request) and request.session['session_species'] == Species.predator:
        if Profile.objects.get(id=request.session['nav_id']).isActive and not excludeUrls(request.get_full_path()):
            return True
    return False

def isFriend(request):
    """Returns True if Profile checkId is a current friend of the session_profile."""
    if isSelf(request):
        return True
    tprof = Profile.objects.get(id=request.session['session_id'])
    navProf = Profile.objects.get(id=request.session['nav_id'])
    if navProf.isDead:
        return True
    if navProf in tprof.friends.all():
        return True
    return False

def isPredatorPrey(species):
    """Returns True is Profile is species type forager or predator."""
    if int(species) == Species.forager or int(species) == Species.predator:
        return True
    return False

def isAllowedUserSpecies(species):
    """Returns True is species is in the allowed list."""
    allowed = [Species.visitor, Species.predator, Species.forager]
    if species in allowed:
        return True
    return False

def upInterest(obj):
    """Increases the interest of supplied object of type Profile or Post. Returns nothing."""
    if hasattr(obj, 'interest'):
        obj.interest += 1
        obj.save()

def addTags(obj, tags):
    """Adds tags from a supplied list to an object of type Profile or Post. Returns nothing.
    
    Creates a new Tag object if tag is new to the system. Will not create duplicates but will
    add to interest rating of pre-existing Tag objects.
    """
    for tag in tags:
        if tag.isalpha():
            if Tag.objects.filter(name=tag).count():
                t = Tag.objects.filter(name=tag.lower()).order_by('?')[0]
                t.interest += 1
                t.save()
            else:
                t = Tag(name=tag.lower(), interest=1)
                t.save()
            if isinstance(obj, Post):
                obj.post_profile.tags.add(t)  
                obj.post_profile.save()  
            obj.tags.add(t)
    obj.save()

def bannerSelect(current):
    """Returns a randomly selected banner image from collection of banners. Used in bruce_banner block."""
    bannerCount = returnCount('banners')
    selection = randint(1, bannerCount)
    while selection == current:
        selection = randint(1, bannerCount)
    return selection

def bgSelect(current):
    """Returns next background image from collection of backgrounds. Used in background-style.html."""
    bgCount = returnCount('backgrounds')
    if current > bgCount:
        return randint(1, bgCount)
    selection = current + 1
    if selection > bgCount:
        selection = 1
    return selection
    
def getTheMessage(request, i):
    """Returns message from collection of site messages for display in message tag."""
    navName = Profile.objects.get(id=request.session['nav_id']).fullName
    siteMessages = [
        'Null',
        'you made friends with [' + navName + ']',
        'you died from starvation',
        'you ate [' + navName + '] to sustain life',
        'you grazed to sustain life',
        'welcome to the [openspace] wilderness',
        'you commented on a post',
        'you liked something',
        'you tagged [' + navName + ']',
        'you tagged a post',
        'following [' + request.session['selected_trail'] + '] trail'
        ]
    if i < len(siteMessages):
        return siteMessages[i]
    return "something has happened"

def parkDataProcessor():
    """Returns a dictionary containing data about the site."""
    profileCount = Profile.objects.all().count()
    postCount = Post.objects.all().count()
    activeCount = Profile.objects.exclude(species=Species.abandoned).count()
    data = {}
    (data['tagged_profile_count'],
        data['tagged_post_count'],
        data['tagged_percent']) = taggedData(profileCount + postCount)
    data['dead_count'], data['dead_percent'] = deadData(activeCount)
    return data

def taggedProcessor(total):
    """Figures a percentage of total Park Objects tagged and returns counts and percentage."""
    taggedProfiles = Profile.objects.annotate(num_tags=Count('tags')).filter(num_tags__gt=0).count()
    taggedPosts = Post.objects.annotate(num_tags=Count('tags')).filter(num_tags__gt=0).count()
    return quickIntPercent(total, (taggedProfiles + taggedPosts))

def deadProcessor(profileCount):
    """Figures a percentage of total Profiles dead and returns count and percentage."""
    deadProfiles = Profile.objects.filter(species=Species.dead).count()
    return deadProfiles, quickIntPercent(profileCount, deadProfiles)
    
def quickIntPercent(total, subset):
    """Figures and returns a percentage given a total and a subset."""
    return int(float(subset) / total * 100)