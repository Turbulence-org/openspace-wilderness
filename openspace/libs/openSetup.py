from django.utils import timezone
from apps.profiles.models import Profile
from apps.tags.models import Tag
from libs.profileHelpers import makeProfile, makeBirthPost, makeFriends, assignImages, makeTaggedPost
from libs.siteEnums import Species, Gender, Tags
import data_path

def populate(pop):
    for i in range(pop):
        makeProfile(Species.abandoned)

def initialPreyProfiles():
    profileBank = [
        {'fname':'Angela', 'lname':'Lyman', 'gender':Gender.male, 'age':30, 'location':'Albuquerque, New Mexico'},
        {'fname':'Mark', 'lname':'Gunk', 'gender':Gender.male, 'age':33, 'location':'Raleigh, North Carolina'},
        {'fname':'Forch', 'lname':'Cholak', 'gender':Gender.male, 'age':30, 'location':'Eerie, Pennsylvania'},
        {'fname':'Yesh', 'lname':'Bash', 'gender':Gender.male, 'age':32, 'location':'Orono, Maine'},
        {'fname':'Katherine', 'lname':'Woods', 'gender':Gender.female, 'age':28, 'location':'Baton Rouge, Lousiana'},
        {'fname':'Marya', 'lname':'Jackson', 'gender':Gender.female, 'age':43, 'location':'Ames, Iowa'},
        {'fname':'Cosmo', 'lname':'Toto', 'gender':Gender.male, 'age':29, 'location':'Youngstown, Ohio'},
        {'fname':'Jennifer', 'lname':'Margaret', 'gender':Gender.female, 'age':30, 'location':'Portland, Oregon'},
        {'fname':'Raymond', 'lname':'Elanor', 'gender':Gender.female, 'age':29, 'location':'Tulsa, Okalahoma'},
        {'fname':'Ian', 'lname':'LePage', 'gender':Gender.male, 'age':35, 'location':'Gorham, Maine'},
        {'fname':'Taffy', 'lname':'Virgo', 'gender':Gender.female, 'age':48, 'location':'Carmel, Indiana'},
        {'fname':'Kate', 'lname':'Digby', 'gender':Gender.female, 'age':29, 'location':'West Stockbridge, Massachusetts'},
    ]
    return profileBank
    
def initialTags():
     return [
        'protected', 'birth', 'death', 'starvation', 'predation', 'grazing',
        'friends', 'comment', 'interest', 'tag', 'trail',  # 11 System Reserved Tags
        'sports', 'depression', 'boys', 'girls', 'sex', 'school', 'internet',
        'apology', 'gibberish', 'pets', 'music', 'work', 'politics', 'stupid',
        'video games', 'anger', 'romance'
        ]

def setupOpen(pop):

    #SETUP ABANDONED PROFILES
    if pop > 1:
        populate(pop)
    #profiles = Profile.objects.all()
    #for p in profiles:
    #    makeFriends(p)
    
    #SETUP TAGS
    for t in initialTags():
        d = Tag(name=t)
        d.save()
        
    #MAKE RANGER
    ranger = Profile(
        fname='Ranger',
        lname='Lyman',
        gender=Gender.female,
        age=30,
        location='Indianapolis, Indiana',
        last_login=timezone.now(),
        species=Species.system,
        profile_url='ranger@openspacewilderness.com',
        img_number=1,
        energy=1983,
        visible=True
    )
    ranger.save()
    rangerPost = "Thank you for visiting the openspace wilderness. I am here to assist you as well as post occasional updates and additional info about the park. Have fun exploring, and be careful out there in the wilds."
    makeTaggedPost(ranger, rangerPost, 'protected')
    
    #SEED PREY PROFILES
    for p in initialPreyProfiles():
        newProfile = Profile(
            fname=p['fname'],
            lname=p['lname'],
            gender=p['gender'],
            age=p['age'],
            location=p['location'],
            last_login=timezone.now(),
            species=Species.forager,
            energy=80,
            visible=False
        )
        newProfile.save()
        assignImages(newProfile)
        makeBirthPost(newProfile)
