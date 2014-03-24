from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from apps.profiles.models import Profile, Post, Comment
from apps.tags.models import Tag
from apps.profiles.forms import CommentForm, ProfileTagForm, PostTagForm
from libs.siteEnums import System, Tags
from libs import siteHelpers, profileHelpers
import re

#/profiles/
def index(request):
    return redirect('index')

#/profiles/<profile_id>/    
def single(request, profile_id):
    """Displays a single Profile and show paginated Posts"""
    profile = get_object_or_404(Profile.objects.prefetch_related('post_set', 'tags'),
        pk=profile_id)
    request.session['nav_position'] = profile.position
    request.session['nav_id'] = profile_id
    allPosts = profile.post_set.all().prefetch_related('comment_set', 'tags')
    posts = Paginator(allPosts, System.postsPage)
    page = request.GET.get('page')
    try:
        pagedPosts = posts.page(page)
    except PageNotAnInteger:
        pagedPosts = posts.page(1)
    except EmptyPage:
        pagedPosts = posts.page(posts.num_pages)
    context = {
        'profile': profile,
        'posts': pagedPosts,
        'comment_form': CommentForm(auto_id=False),
        'profile_tag_form': ProfileTagForm(auto_id=False),
        'post_tag_form': PostTagForm(auto_id=False),
        'auto_tags': Tag.objects.filter(id__gt=System.reservedTags).order_by('-interest','name')[:30],
        'grazable': True
    }
    return render(request, 'profiles/single-profile.html', context)

#/profiles/<profile_id>/friends/
def friends(request, profile_id):
    """Displays all friends of a Profile."""
    profile = get_object_or_404(Profile.objects.select_related('friends'), pk=profile_id)
    context = {
        'profile': profile,
        'profile_tag_form': ProfileTagForm(auto_id=False),
        'auto_tags': Tag.objects.filter(id__gt=System.reservedTags).order_by('-interest','name')[:30]
    }
    return render(request, 'profiles/friends.html', context)

#/profiles/<profile_id>/makefriend/
def makeFriend(request, profile_id):
    """Adds current profile to user's friends set and returns to referrer. Makes a user post."""
    friend = get_object_or_404(Profile, pk=profile_id)
    user = Profile.objects.get(id=request.session['session_id'])
    if friend not in user.friends.all():
        request.session['notification'] = 'friends'
        user.friends.add(friend)
        user.save()
        friend.friends.add(user)
        friend.save()
        postOut = 'made friends with ' + friend.fullName
        profileHelpers.makeUserPost(request, postOut, 'friends')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

#/profiles/<profile_id>/tags/
def profileTags(request, profile_id):
    """Displays all Tags attached to a Profile."""
    profile = get_object_or_404(Profile.objects.prefetch_related('tags'), pk=profile_id)
    context = {
        'profile': profile,
        'profile_tag_form': ProfileTagForm(auto_id=False),
        'auto_tags': Tag.objects.filter(id__gt=System.reservedTags).order_by('name')[:30]
    }
    return render(request, 'profiles/tags.html', context)

#/profiles/<profile_id>/death/
def profileDeath(request, profile_id):
    """Takes a profile id makes a death post and delivers you to profile page.
    NOTE: Profile should already be dead by the time it gets here."""
    profile = get_object_or_404(Profile, pk=profile_id)
    if profile.isDead:
        profileHelpers.makeDeathPost(profile)
        request.session['notification'] = 'starvation'
        request.session['nav_position'] = profile.position
    return redirect('profiles:single', profile.id)
    
#/profiles/<profile_id>/post/<post_id>/
def singlePost(request, profile_id, post_id):
    """Displays a single Post from a Profile."""
    profile = get_object_or_404(Profile.objects.prefetch_related('post_set'), pk=profile_id)
    post = get_object_or_404(Post.objects.prefetch_related('comment_set', 'tags'), pk=post_id)
    request.session['nav_position'] = profile.position
    request.session['nav_id'] = profile_id
    request.session['is_human'] = True
    context = {
        'profile': profile,
        'post': post,
        'comment_form': CommentForm(auto_id=False),
        'profile_tag_form': ProfileTagForm(auto_id=False),
        'post_tag_form': PostTagForm(auto_id=False),
        'auto_tags': Tag.objects.filter(id__gt=System.reservedTags).order_by('name')[:30],
        'grazable': True
        }
    return render(request, 'profiles/single-post.html', context)

#/profiles/<profile_id>/post/<post_id>/addcomment/
def addComment(request, profile_id, post_id):
    """Adds a comment a Post and returns to referrer. Makes a user post."""
    profile = get_object_or_404(Profile, pk=profile_id)
    post = get_object_or_404(Post, pk=post_id)
    context = {'profile': profile, 'post': post}
    if request.POST:
        form = CommentForm(request.POST)
        if form.data['comment_content'] and form.is_valid:
            new_comment = form.save(commit=False)
            new_comment.comment_content = re.sub('<[^<]+?>', '', form.data['comment_content'])
            new_comment.comment_profile = Profile.objects.get(id=request.session['session_id'])
            new_comment.comment_post = post
            new_comment.date_published = timezone.now()
            new_comment.save()
            postOut = 'left comment: ' + new_comment.comment_content
            profileHelpers.makeUserPost(request, postOut, 'comment')
            request.session['notification'] = 'comment'
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    return redirect('profiles:singlePost', profile_id, post_id)

#/profiles/5/profileinterest/
def profileInterest(request, profile_id):
    """Adds interest to a Profile. Makes a user post."""
    profile = get_object_or_404(Profile, pk=profile_id)
    interestSet = request.session['profile_interest_collection'].split(',')
    if profile_id not in interestSet and profile_id != request.session['session_id']:
        siteHelpers.upInterest(profile)
        request.session['profile_interest_collection'] += ',' + profile_id
        postOut = 'likes ' + profile.fullName
        profileHelpers.makeUserPost(request, postOut, 'interest')
        request.session['notification'] = 'likeprofile'
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

#/profiles/post/5/postinterest/
def postInterest(request, post_id):
    """Adds interest to a Post. Makes a user post."""
    post = get_object_or_404(Post, pk=post_id)
    interestSet = request.session['post_interest_collection'].split(',')
    if post_id not in interestSet:
        siteHelpers.upInterest(post)
        request.session['post_interest_collection'] += ',' + post_id
        postOut = 'likes ' + post.postProfileName + '\'s post'
        profileHelpers.makeUserPost(request, postOut, 'interest')
        request.session['notification'] = 'likepost'
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
#/profiles/5/addtags
def addProfileTags(request, profile_id):
    """Adds Tags to a Profile. Makes a user post."""
    profile = get_object_or_404(Profile, pk=profile_id)
    context = {'profile': profile}
    if request.POST:
        form = ProfileTagForm(request.POST)
        if form.is_valid:
            new_tags = form.data['pro_new_tags']
            addedTags =  siteHelpers.addTags(profile, new_tags.split(','))
            if addedTags:
                postOut = 'added tags: ' + addedTags
                profileHelpers.makeUserPost(request, postOut, 'tag')
                request.session['notification'] = 'tagprofile'
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    return redirect('profiles:single', profile_id)

#/profiles/5/post/5/addtags
def addPostTags(request, profile_id, post_id):
    """Adds Tags to a Post. Makes a user post."""
    profile = get_object_or_404(Profile, pk=profile_id)
    post = get_object_or_404(Post, pk=post_id)
    context = {'profile': profile, 'post': post}
    if request.POST:
        form = PostTagForm(request.POST)
        if form.is_valid:
            new_tags = form.data['post_new_tags']
            addedTags = siteHelpers.addTags(post, new_tags.split(', '))
            if addedTags:
                postOut = 'added tags: ' + addedTags
                profileHelpers.makeUserPost(request, postOut, 'tag')
                request.session['notification'] = 'tagpost'
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    #TODO error massage
    return redirect('profiles:post', profile_id, post_id)

#/profiles/createprofile/2
def createProfile(request, species_id):
    """Creates a new Profile of species type species_id."""
    if not siteHelpers.isPredatorPrey(species_id):
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    if not request.session['session_lock']:
        newP = profileHelpers.makeProfile(int(species_id))
        request.session['session_id'] = newP.id
        request.session['session_species'] = newP.species
        request.session['session_lock'] = True
        request.session['notification'] = 'birth'
    return redirect('profiles:single', newP.id)
    
#/profiles/5/eatprofile
def eatProfile(request, profile_id):
    """Makes a selected Profile die and sends notice."""
    prey = get_object_or_404(Profile, pk=profile_id)
    predator = Profile.objects.get(id=request.session['session_id'])
    if profileHelpers.eatPrey(predator, prey):
        request.session['notification'] = 'predation'
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
#/profiles/5/graze
def grazeProfile(request, profile_id):
    """Consumes text from content of a randomly selected Post of current Profile."""
    profile = get_object_or_404(Profile.objects.prefetch_related('post_set'), pk=profile_id)
    targetPost = profile.post_set.exclude(tags=Tags.protected).order_by('?')
    if targetPost:
        if profileHelpers.grazePost(Profile.objects.get(id=request.session['session_id']), targetPost[0]):
            request.session['notification'] = 'grazing'
        else:
            request.session['notification'] = 'full'
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

#/profiles/5/post/5/graze
def grazePost(request, profile_id, post_id):
    """Consumes text from content of current Post."""
    targetPost = get_object_or_404(Post, pk=post_id)
    if targetPost:
        if profileHelpers.grazePost(Profile.objects.get(id=request.session['session_id']), targetPost):
            request.session['notification'] = 'grazing'
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))