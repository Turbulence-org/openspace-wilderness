from apps.profiles.models import Profile, Post
from apps.tags.models import Tag
from libs import navHelpers, siteHelpers
from libs.siteEnums import Species, Tags, System

def siteProcessor(request):
    background = 'media/backgrounds/bg-' + str(request.session['page_background']) + '.jpg'
    request.session['page_banner'] = siteHelpers.bannerSelect(request.session['page_banner'])
    banner_src = 'media/banners/banner-' + str(request.session['page_banner']) + '.jpg'
    site_context = {
        'human_key': 84990210,
        'is_human': request.session['is_human'],
        'background': background,
        'banner_src': banner_src,
        'path': request.get_full_path(),
        'mb_size': System.mb
    }
    return site_context

def sessionProcessor(request):
    session_context = {}
    
    # CONSTANTS
    session_context['predator'] = Species.predator
    session_context['forager'] = Species.forager
    
    # SESSION KEYS
    tprof = Profile.objects.select_related('post_set').get(id=request.session['session_id'])
    session_context['session_object'] = tprof
    session_context['session_id'] = tprof.id
    session_context['session_name'] = tprof.fullName
    session_context['session_icon'] = tprof.prettyIcon
    session_context['session_species'] = tprof.species
    session_context['session_energy'] = tprof.energy
    session_context['species_meals'] = tprof.meals
    session_context['session_lock'] = request.session['session_lock']
    session_context['session_activity'] = tprof.recentActivity
    
    # HANDLING FOOD
    session_context['is_pred_prey'] = siteHelpers.isPredatorPrey(tprof.species)
    session_context['prey'] = siteHelpers.isPrey(request)
    session_context['kosher'] = siteHelpers.isKosher(request)
    session_context['is_post'] = siteHelpers.isPost(request)
    
    # HANDLING FRIENDS
    session_context['is_friend'] = siteHelpers.isFriend(request)

    #navigation
    nav_context = {}
    currentPosition = request.session['nav_position']
    nav_context['nav_position'] = currentPosition
    nav_context['selected_trail'] = request.session['selected_trail']
    if nav_context['selected_trail'] != 'no':
        trail = Tag.objects.get(name=nav_context['selected_trail'])
        nav_context['selected_trail_id'] = trail.id
    else:
        trail = None
    
    # NAVIGATION KEYS
    nav_context['rand_profile'] = navHelpers.randomProfile(tprof, trail)
    nav_context['prev_profile'] = navHelpers.previousProfile(currentPosition, tprof, trail)
    nav_context['next_profile'] = navHelpers.nextProfile(currentPosition, tprof, trail)
    
    return dict(session_context.items() + nav_context.items())

def messageProcessor(request):
    message_context = {}
    message_context['message_flag'] = False
    current_notice = request.session['notification']
    if current_notice:
        message_context['message_flag'] = True
        message_context['message'] = siteHelpers.getTheMessage(request, current_notice)
    request.session['notification'] = None
    
    return message_context