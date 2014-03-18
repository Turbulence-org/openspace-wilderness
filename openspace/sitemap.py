from django.contrib import sitemaps
from apps.profiles.models import Profile
import datetime

class Sitemap(sitemaps.Sitemap):
    def __init__(self, names):
        self.names = names

    def items(self):
        return self.names

    def changefreq(self, obj):
        return 'weekly'

    def lastmod(self, obj):
        return datetime.datetime.now()

    def location(self, obj):
        return reverse(obj)


class ProfileSitemap(sitemaps.Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Profile.objects.all()

    def lastmod(self, obj):
        return obj.date