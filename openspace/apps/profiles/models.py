from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from apps.tags.models import Tag
from libs.siteEnums import Gender, Species, System
from libs.auxHelpers import returnCount
from random import randint
import os, fnmatch
from os.path import join
from settings.common import STATIC_URL


class Profile(models.Model):
    """Profile objects are the primary object employed in the openspace wilderness.
    
    Profiles may have a profile image, an icon, and related data
    + may have sets of friends containing Profile objects
    + may have sets of tags containing Tag objects
    + have a one-to-one relationship with Post objects
    
    Required assignments:
    fname, lname, age
    
    Optional assignments:
    location, blog_url, blog_id, last_login, friends, tags
    
    Default assignments:
    gender = female(0)
    interest = 0
    energy = 1
    meals = 0
    visible = True
    species = abandoned(0)
    """
    
    position = models.PositiveIntegerField(max_length=9, default=1)
    fname = models.CharField('First Name', max_length=35)
    lname = models.CharField('Last Name', max_length=35)
    gender = models.PositiveIntegerField(max_length=2, default=Gender.female)
    age = models.CharField(max_length=5)
    location = models.CharField(max_length=75, blank=True)
    blog_url = models.URLField(blank=True)
    blog_id = models.CharField(max_length=5, blank=True)
    last_login = models.DateField('last login', blank=True, null=True)
    friends = models.ManyToManyField('self', blank=True)
    img_number = models.PositiveIntegerField(max_length=4, default=1)
    tags = models.ManyToManyField(Tag, blank=True)
    interest = models.PositiveIntegerField(max_length=5, default=0)
    energy = models.PositiveIntegerField(max_length=4, default=1)
    meals = models.PositiveIntegerField(max_length=3, default=0)
    visible = models.BooleanField(default=True)
    species = models.PositiveIntegerField(max_length=1, default=Species.abandoned)
    
    @cached_property
    def fullName(self):
        return self.fname + ' ' + self.lname
    
    @cached_property
    def sex(self):
        if self.gender == Gender.female:
            return 'female'
        else:
            return 'male'
    
    @property
    def imageString(self):
        return str(self.img_number)
    
    @property
    def interestString(self):
        return str(self.interest)
    
    @property
    def energyString(self):
        return str(self.energy)
            
    @property
    def speciesReadable(self):
        if self.species == Species.abandoned:
            return 'abandoned'
        elif self.species == Species.system:
            return 'system'
        elif self.species == Species.visitor:
            return 'visitor'
        elif self.species == Species.predator:
            return 'predator'
        elif self.species == Species.forager:
            return 'forager'
        elif self.species == Species.dead:
            return 'dead'
        else:
            return 'unknown'
        
    @property
    def isActive(self):
        if self.species == Species.predator or self.species == Species.forager:
            return True
    
    @property
    def isPredator(self):
        if self.species == Species.predator:
            return True
    
    @property
    def isForager(self):
        if self.species == Species.forager:
            return True
    
    @property
    def isFull(self):
        if self.energy >= System.full:
            return True
    
    @property
    def isDead(self):
        if self.species == Species.dead:
            return True
    
    @cached_property
    def fitUrl(self):
        if len(self.blog_url) > System.fitUrl:
            return self.blog_url[7:]
        return self.blog_url
    
    @property
    def prettyPic(self):
        return 'media/' + self.speciesReadable + '/profilepic-' + self.imageString + '.jpg'
    
    @property
    def prettyIcon(self):
        return 'media/' + self.speciesReadable + '/icon-' + self.imageString + '.jpg'
    
    @property
    def decentFriends(self):
        return self.friends.filter(visible=True).order_by('lname')
    
    @property
    def bestFriends(self):
        return self.decentFriends[:System.bestFriends]
    
    @property
    def topTags(self):
        return self.tags.all().order_by('-interest')[:8]
    
    @property
    def recentActivity(self):
        return self.post_set.all().order_by('-date_published')[:3]
    
    def __unicode__(self):
        return self.fullName
        
    def drain(self):
        self.energy -= 1
        if self.energy <= 0:
            self.die()
        self.save()
    
    def die(self):
        self.species = Species.dead
        self.energy = 0
        self.visible = True
        self.last_login = timezone.now() 
        self.img_number = randint(1, returnCount('dead')/2)
        self.save()


class Post(models.Model):
    """Post objects contain content from recovered blogger blogs
    or activity from the active Profile types
    
    Required assignments:
    post_profile = Profile object, post_content
    
    Optional assignments:
    tags
    
    Default assignments:
    date_published = timezone.now(), interest = 0, just_posted = False
    """

    post_profile = models.ForeignKey(Profile)
    date_published = models.DateTimeField('date published',
        default=timezone.now())
    post_content = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True)
    interest = models.PositiveIntegerField(max_length=5, default=0)
    just_posted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_published']
    
    @cached_property
    def postProfileName(self):
        return self.post_profile.fullName
    
    @cached_property
    def fitContent(self):
        return self.post_content[:300]
    
    @property
    def interestString(self):
        return str(self.interest)
    
    @property
    def justPosted(self):
        if self.just_posted:
            self.just_posted = False
            self.save()
            return True
    
    def __unicode__(self):
        return str(self.post_profile) + ' / ' + self.post_content[:11]


class Comment(models.Model):
    """Comments are short content that can be created by a Profile and attached to a Post
    
    Required assignments:
    comment_profile = Profile object, comment_post = Post object, comment_content
    
    Default assignments:
    date_published = timezone.now()
    """

    comment_profile = models.ForeignKey(Profile)
    comment_post = models.ForeignKey(Post)
    date_published = models.DateTimeField('date published',
        default=timezone.now())
    comment_content = models.TextField()
    
    class Meta:
        ordering = ['-date_published']
    
    @cached_property
    def commentProfileId(self):
        return self.comment_profile_id
    
    @cached_property
    def commentPostId(self):
        return self.comment_post_id
    
    @cached_property
    def commentPostProfileId(self):
        return Post.objects.get(id=self.comment_post_id).post_profile_id
    
    def __unicode__(self):
        return str(self.comment_profile) + ' / ' + self.comment_content[:11]