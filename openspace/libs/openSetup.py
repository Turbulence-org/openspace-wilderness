from django.utils import timezone
from apps.profiles.models import Profile
from apps.tags.models import Tag
from libs.profileHelpers import makeProfile, makeBirthPost, makeFriends
from libs.siteEnums import Species
import data_path

def populate(pop):
    for i in range(pop):
        makeProfile(Species.abandoned)

# 0-ABANDONED/1-SYSTEM/2-VISITOR/3-PREDATOR/4-FORRAGER
def initialProfiles():
    profileBank = [
        {'fname':'Park', 'lname':'Ranger', 'gender':0, 'age':'45', 'location':'Topeka, Kansas', 'imgnumber':1, 'species':1,},
        {'fname':'Anonymous', 'lname':'Visitor', 'gender':1, 'age':'58', 'location':'Albuquerque, New Mexico', 'imgnumber':1, 'species':2,},
        {'fname':'Anonymous', 'lname':'Visitor', 'gender':0, 'age':'18', 'location':'Indianapolis, Indiana', 'imgnumber':2, 'species':2,},
        {'fname':'Anonymous', 'lname':'Visitor', 'gender':1, 'age':'32', 'location':'Savannah, Georgia', 'imgnumber':3, 'species':2,},
        {'fname':'Anonymous', 'lname':'Visitor', 'gender':0, 'age':'22', 'location':'Portland, Maine', 'imgnumber':4, 'species':2,},
        {'fname':'Anonymous', 'lname':'Visitor', 'gender':1, 'age':'14', 'location':'Chicago, Illinois', 'imgnumber':1, 'species':2,},
        {'fname':'Anonymous', 'lname':'Visitor', 'gender':0, 'age':'29', 'location':'San Francisco, California', 'imgnumber':2, 'species':2,},
        {'fname':'Anonymous', 'lname':'Visitor', 'gender':1, 'age':'19', 'location':'West Lafyette, Indiana', 'imgnumber':3, 'species':2,},
        {'fname':'Anonymous', 'lname':'Visitor', 'gender':0, 'age':'36', 'location':'Franklin, Indiana', 'imgnumber':4, 'species':2,},
        {'fname':'Mark', 'lname':'Gunk', 'gender':1, 'age':'33', 'location':'Raleigh, North Carolina', 'imgnumber':1, 'species':4, 'energy':80,},
        {'fname':'Forch', 'lname':'Cholak', 'gender':0, 'age':'30', 'location':'Eerie, Pennsylvania', 'imgnumber':2, 'species':4, 'energy':80,},
        {'fname':'Yeshe', 'lname':'Bash', 'gender':1, 'age':'32', 'location':'Orono, Maine', 'imgnumber':3, 'species':4, 'energy':80,},
        {'fname':'Kate', 'lname':'Woods', 'gender':0, 'age':'28', 'location':'Baton Rouge, Lousiana', 'imgnumber':4, 'species':4, 'energy':80,},
        {'fname':'Marya', 'lname':'Zinner', 'gender':0, 'age':'43', 'location':'Ames, Iowa', 'imgnumber':5, 'species':4, 'energy':80,},
        {'fname':'Cosmo', 'lname':'Toto', 'gender':1, 'age':'29', 'location':'Youngstown, Ohio', 'imgnumber':6, 'species':4, 'energy':80,},
        {'fname':'Jennifer', 'lname':'Margaret', 'gender':0, 'age':'30', 'location':'Portland, Oregon', 'imgnumber':7, 'species':4, 'energy':80,},
        {'fname':'Ray', 'lname':'Elanor', 'gender':0, 'age':'29', 'location':'Tulsa, Okalahoma', 'imgnumber':8, 'species':4, 'energy':80,},
        {'fname':'Ian', 'lname':'LePage', 'gender':1, 'age':'35', 'location':'Gorham, Maine', 'imgnumber':9, 'species':4, 'energy':80,},
        {'fname':'Taffy', 'lname':'Virgo', 'gender':0, 'age':'48', 'location':'Carmel, Indiana', 'imgnumber':10, 'species':4, 'energy':80,},
        {'fname':'Kay', 'lname':'Skinner', 'gender':0, 'age':'29', 'location':'West Stockbridge, Massachusetts', 'imgnumber':10, 'species':4, 'energy':80,},
    ]
    return profileBank
    
def initialTags():
     return [
        'protected', 'birth', 'death', 'starvation', 'predation', 'grazing', 'friends',
        'comment', 'interest', 'tagged profile', 'tagged post', 'trail',
        'sports', 'depression', 'boys', 'girls', 'sex', 'school', 'internet',
        'apology', 'gibberish', 'pets', 'music', 'work', 'politics', 'journal',
        ]

def setupOpen():
    #SETUP ABANDONED PROFILES
    populate(75)
    profiles = Profile.objects.all()
    #for p in profiles:
        #makeFriends(p)
    
    #SETUP TAGS
    for t in initialTags():
        d = Tag(name=t)
        d.save()
    
    #SETUP ACTION PROFILES
    for p in initialProfiles():
        d = Profile(fname=p['fname'], lname=p['lname'], gender=p['gender'], age=p['age'], location=p['location'], last_login=timezone.now(), img_number=p['imgnumber'], species=p['species'], visible=False,)
        d.save()
        makeBirthPost(d)
    
    #INITIAL FORAGER POPULATION
    for i in range(4):
        makeProfile(Species.forager)
