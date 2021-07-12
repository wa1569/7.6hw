from django import forms
from .models import Post, Comment, Hashtag
from django.contrib.auth.models import User
from .models import UserInformation

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'writer', 'body','image','hashtags']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class HashtagForm(forms.ModelForm):
    class Meta:
        model = Hashtag
        fields = ['name']

class UserInformationForm(forms.ModelForm):

    class Meta:
        model = UserInformation
        fields = ("age", "address")