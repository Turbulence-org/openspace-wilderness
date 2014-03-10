from django.db import models
from django.db.models import Count

# TAG MODEL
class Tag(models.Model):
    """Tag model can be applied to Profiles and Posts.
    
    Tags consist of a Tag name and an interest value based on how many times a Tag
    had been applied. 
    Trails of similarly tagged Profiles are automatically created for navigation
    """
    
    name = models.CharField(max_length=15)
    interest = models.PositiveIntegerField(max_length=6, default=0)
    
    @property
    def interestString(self):
        return str(self.interest)
    
    def __unicode__(self):
        return self.name