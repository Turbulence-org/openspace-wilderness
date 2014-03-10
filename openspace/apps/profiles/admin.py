from django.contrib import admin
from apps.profiles.models import *

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1

class PostInline(admin.TabularInline):
    model = Post
    extra = 0

class ProfileAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Personal Information', {'fields': ['fname', 'lname', 'age', 'gender', 'location', 'tags', 'interest', 'position', 'species', 'img_number', 'energy', 'visible']}),
        ('Blog Info', {'fields': ['blog_id', 'blog_url', 'last_login'], 'classes': ['collapse']}),
        ('Network', {'fields': ['friends'], 'classes': ['collapse']})
    ]
    inlines = [PostInline]
    list_display = ('id', 'species', 'fname', 'lname', 'location', 'visible', 'last_login')
    search_fields = ['id', 'fname', 'lname', 'species']

class PostAdmin(admin.ModelAdmin):
    inlines = [CommentInline]
    list_display = ('post_profile', 'date_published', 'post_content')
    
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Post, PostAdmin)
