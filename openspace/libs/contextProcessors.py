from apps.profiles.models import Profile
from apps.tags.models import Tag
from libs import navHelpers, siteHelpers
from libs.siteEnums import Notification, Species, Tags
from os.path import join
from settings.common import DJANGO_ROOT

def siteProcessor(request):
    background = 'bg-' + str(request.session['page_background']) + '.jpg'
    request.session['page_banner'] = siteHelpers.bannerSelect(request.session['page_banner'])
    #banner_src = join(DJANGO_ROOT, 'assets/media/banners/banner-' + str(request.session['page_banner']) + '.jpg')
    banner_src = 'media/banners/banner-' + str(request.session['page_banner']) + '.jpg'
    site_context = {
        'background': background,
        'banner_src': banner_src,
        'path': request.get_full_path()
    }
    return site_context

def sessionProcessor(request):
    session_context = {}
    
    # CONSTANTS
    session_context['predator'] = Species.predator
    session_context['forager'] = Species.forager
    
    # SESSION KEYS
    tprof = Profile.objects.get(id=request.session['session_profile'])
    session_context['session_object'] = tprof
    session_context['session_profile'] = tprof.id
    session_context['session_name'] = tprof.fullName
    session_context['session_icon'] = tprof.prettyIcon
    session_context['session_species'] = tprof.species
    session_context['session_energy'] = tprof.energy
    session_context['species_posts'] = 0
    if tprof.isPredator:
        session_context['species_posts'] = tprof.post_set.filter(tags=Tags.predator).count()
    if tprof.isForager:
        session_context['species_posts'] = tprof.post_set.filter(tags=Tags.graze).count()
    session_context['session_lock'] = request.session['session_lock']
    
    # HANDLING FOOD
    session_context['is_pred_prey'] = siteHelpers.isPredatorPrey(tprof.species)
    session_context['prey'] = siteHelpers.isPrey(request)
    session_context['kosher'] = siteHelpers.isKosher(request)
    session_context['is_post'] = siteHelpers.isPost(request)
    
    # HANDLING FRIENDS
    session_context['is_friend'] = siteHelpers.isFriend(request)

    return session_context

def navigationProcessor(request):
    nav_context = {}
    tprof = Profile.objects.get(id=request.session['session_profile'])
    currentPosition = request.session['nav_position']
    nav_context['nav_position'] = currentPosition
    nav_context['selected_trail'] = request.session['selected_trail']
    if nav_context['selected_trail'] != 'no':
        trail = Tag.objects.get(name=nav_context['selected_trail'])
        nav_context['selected_trail_id'] = trail.id
    else:
        trail = None
    
    # NAVIGATION KEYS
    nav_context['rand_profile'] = navHelpers.randomProfile(currentPosition, tprof, trail)
    nav_context['prev_profile'] = navHelpers.previousProfile(currentPosition, tprof, trail)
    nav_context['next_profile'] = navHelpers.nextProfile(currentPosition, tprof, trail)
    
    return nav_context

def messageProcessor(request):
    message_context = {}
    message_context['message_flag'] = False
    current_notice = request.session['notification']
    if current_notice != Notification.no_notification:
        message_context['message_flag'] = True
        message_context['message'] = siteHelpers.getTheMessage(request, current_notice)
    request.session['notification'] = Notification.no_notification
    
    return message_context