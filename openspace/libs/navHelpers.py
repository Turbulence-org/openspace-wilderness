from apps.profiles.models import Profile
from libs.siteEnums import Species

def randomEncounter():
    """Selects a random Profile object and if Profile.isActive returns it as random encounter."""
    encounter = Profile.objects.all().order_by('?')[0]
    if encounter.isActive:
        return encounter.id
    return None

def randomProfile(currentId, profile, trail):
    """Selects and returns a random Profile id for navigation based on selected Trail."""
    selectedProfile = Profile.objects.get(id=currentId)
    if profile.isPredator:
        prey = randomEncounter()
        if prey:
            return prey
    if trail:
        if Profile.objects.filter(tags=trail).count() > 1:
            while selectedProfile.id == currentId:
                selectedProfile = Profile.objects.exclude(visible=False).filter(tags=trail).order_by('?')[0]
    else:
        if Profile.objects.count() > 1:
            while selectedProfile.id == currentId:
                selectedProfile = Profile.objects.exclude(visible=False).order_by('?')[0]
    return selectedProfile.id

def nextProfile(currentId, profile, trail):
    """Gets and returns the next Profile id based on selected Trail."""
    if profile.isPredator:
        prey = randomEncounter()
        if prey:
            return prey
    if trail:
        next = Profile.objects.filter(tags=trail).filter(position__gt=currentId).order_by('position')[0:1]
        if not next:
            next = Profile.objects.filter(tags=trail).order_by('position')[0:1]
    else:
        next = Profile.objects.filter(position__gt=currentId).filter(visible=True).order_by('position')[0:1]
        if not next:
            next = Profile.objects.filter(visible=True).order_by('position')[0:1]
    return next[0].id

def previousProfile(currentId, profile, trail):
    """Gets and returns the previous Profile id based on selected Trail."""
    if profile.isPredator:
        prey = randomEncounter()
        if prey:
            return prey
    if trail:
        prev = Profile.objects.filter(tags=trail).filter(position__lt=currentId).order_by('-position')[0:1]
        if not prev:
            end = Profile.objects.filter(tags=trail).order_by('position').count()
            prev = [Profile.objects.filter(tags=trail).order_by('position')[end-1]]
    else:
        prev = Profile.objects.filter(position__lt=currentId).filter(visible=True).order_by('-position')[0:1]
        if not prev:
            end = Profile.objects.filter(visible=True).order_by('position').count()
            prev = [Profile.objects.filter(visible=True).order_by('position')[end-1]]
    return prev[0].id