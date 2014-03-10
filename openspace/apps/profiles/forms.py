from django import forms
from apps.profiles.models import Comment
from apps.tags.models import Tag

class CommentForm(forms.ModelForm):
    
    class Meta:
        auto_id = False
        model = Comment
        fields = ('comment_content',)
        widgets = {
            'comment_content': forms.Textarea(
                attrs = {'cols': 68, 'rows': 7, 'class': 'allRound'}),
        }
        
class PostTagForm(forms.Form):
    post_new_tags = forms.CharField(label='',
        widget = forms.TextInput(attrs={'size':'93', 'class': 'formP'}))

class ProfileTagForm(forms.Form):
    pro_new_tags = forms.CharField(label='', widget = forms.TextInput(attrs={'size': '54'}))