from django.conf import settings
from django.shortcuts import redirect
from apps.profiles.models import Profile
from libs import siteHelpers, profileHelpers
from libs.siteEnums import Species, Notification

class SessionSpeciesError(object):
    """Sets the new_session flag to true if somehow the user session ends up as an inactive species"""
    
    def process_request(self, request):
        if 'session_species' not in request.session:
            request.session['session_species'] = Species.visitor
        if not siteHelpers.isAllowedUserSpecies(request.session['session_species']):
            request.session['new_session'] = True


class SessionSetup(object):
    """Creates and populates a new user session."""
    
    def process_request(self, request):
        if 'new_session' not in request.session or request.session['new_session'] is True:
            
            request.session.flush()
            entry_user = profileHelpers.makeAnonymous()
            entry_nav_profile = Profile.objects.filter(species=0).order_by('?')[0]
            
            request_defaults = (
                ('new_session', False),
                ('show_greeting', True),
                ('page_background', siteHelpers.bgSelect(666)),
                ('page_banner', siteHelpers.bannerSelect(666)),
                ('session_id', entry_user.id),
                ('session_species', entry_user.species),
                ('session_death', False),
                ('selected_trail', 'no'),
                ('nav_id', entry_nav_profile.id),
                ('nav_position', entry_nav_profile.position),
                ('session_lock', False),
                ('profile_interest_collection', str(entry_user.id)),
                ('post_interest_collection', ''),
                ('notification', 0)
            )
        
            for k, v in request_defaults:
                request.session.setdefault(k, v)
                

class LifeIsHard(object):
    """Drains life of an active type session profile if viewing a page that depletes energy."""
    
    def process_request(self, request):
        profile = Profile.objects.get(id=request.session['session_id'])
        if siteHelpers.fairPlay(profile, request):
            profile.drain()
            if profile.isDead:
                request.session['session_death'] = True


class DeathSentence(object):  
    """Performs a host of operations related to the death of the user's session profile."""

    def process_request(self, request):    
        if request.session['session_death']:
            request.session['session_death'] = False
            request.session['notification'] = Notification.starvation
            deadBody = Profile.objects.get(id=request.session['session_id'])
            
            #new session as visitor
            profileHelpers.makeAnonymous()
            newP = Profile.objects.filter(species=Species.visitor).order_by('?')[0]
            request.session['session_id'] = newP.id
            request.session['session_species'] = newP.species
            request.session['session_lock'] = False
            
            return redirect('profiles:profileDeath',  deadBody.id)