from django.conf import settings
from django.shortcuts import redirect
from profiles.models import Profile
from utils import siteHelpers, profileHelpers
from siteEnums import Species, Notification

class SessionSetup(object):
    
    def process_request(self, request):
        if 'show_greeting' not in request.session:
            
            entry_user = Profile.objects.filter(species=2).order_by('?')[0]
            entry_nav_profile = Profile.objects.filter(species=0).order_by('?')[0]
            
            request_defaults = (
                ('show_greeting', True),
                ('page_background', siteHelpers.bgSelect(666)),
                ('page_banner', siteHelpers.bannerSelect(666)),
                ('session_profile', entry_user.id),
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
    
    def process_request(self, request):
        if siteHelpers.fairPlay(request):
            profile = Profile.objects.get(id=request.session['session_profile'])
            profile.drain()
            if profile.isDead:
                request.session['session_death'] = True


class DeathSentence(object):  

    def process_request(self, request):    
        if request.session['session_death']:
            request.session['session_death'] = False
            request.session['notification'] = Notification.starvation
            deadBody = Profile.objects.get(id=request.session['session_profile'])
            
            #new session as visitor
            profileHelpers.makeAnonymous()
            newP = Profile.objects.filter(species=Species.visitor).order_by('?')[0]
            request.session['session_profile'] = newP.id
            request.session['session_species'] = newP.species
            request.session['session_lock'] = False
            
            return redirect('profiles:profileDeath',  deadBody.id)