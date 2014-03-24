from django.conf import settings
from django.shortcuts import redirect
from apps.profiles.models import Profile
from libs import siteHelpers, profileHelpers
from libs.siteEnums import Species

class SessionSpeciesError(object):
    """Sets the new_session flag to true if somehow the user session ends up as an inactive species"""
    
    def process_request(self, request):
        if 'session_species' in request.session:
            if not siteHelpers.isAllowedUserSpecies(request.session['session_species']):
                request.session['new_session'] = True


class SessionSetup(object):
    """Creates and populates a new user session."""
    
    def process_request(self, request):
        if 'new_session' not in request.session or request.session['new_session']:
            is_human = False
            if 'session_anon' in request.session:
                entry_user = Profile.objects.get(id=request.session['session_anon'])
            if 'is_human' in request.session:
                is_human = request.session['is_human']
                if is_human:
                    entry_user = profileHelpers.makeAnonymous()
                    request.session['session_anon'] = entry_user.id
                    
            else:
                entry_user = Profile.objects.filter(species=Species.visitor).order_by('?')[0] #rando to get in the door
            request.session.flush()
            entry_nav_profile = Profile.objects.filter(species=Species.abandoned).order_by('?')[0]
            
            request_defaults = (
                ('new_session', False),
                ('session_anon', entry_user.id),
                ('is_human', is_human),
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
                ('notification', None)
            )
        
            for k, v in request_defaults:
                request.session.setdefault(k, v)
                

class LifeIsHard(object):
    """Drains life of an active type session profile if viewing a page that depletes energy."""
    
    def process_request(self, request):
        if 'session_id' in request.session and request.session['session_id']:
            profile = Profile.objects.get(id=request.session['session_id'])
            if siteHelpers.fairPlay(profile, request):
                profile.drain()
                if profile.isDead:
                    request.session['session_death'] = True


class DeathSentence(object):  
    """Performs a host of operations related to the death of the user's session profile."""

    def process_request(self, request):    
        if 'session_death' in request.session and request.session['session_death']:
            request.session['session_death'] = False
            request.session['notification'] = 'starvation'
            deadBody = request.session['session_id']
            
            # NEW SESSION AS VISITOR
            request.session['session_id'] = request.session['session_anon']
            request.session['session_species'] = Species.visitor
            request.session['is_human'] = True
            request.session['session_lock'] = False
            
            return redirect('profiles:profileDeath',  deadBody)