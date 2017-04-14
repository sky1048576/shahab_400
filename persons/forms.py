__author__ = 'shahab'
from django import forms
from .models import Home,Picture,Comment,Member
from django.contrib.auth import get_user_model

User = get_user_model()

class HomeForm(forms.ModelForm):
    # ostan = forms.ChoiceField(choices=ostan,label="witch state",)
    class Meta:
        model = Home
        fields = ['name','address', 'about','zip_code',]
    def save(self,commit=True):
        _home= super(HomeForm,self).save(commit=False)
        if commit:
            _home.save()
        return _home

class ImageForm(forms.ModelForm):
    class Meta:
        model = Picture
        fields = ['image',]
        
class CommentForm(forms.ModelForm):
    # ostan = forms.ChoiceField(choices=ostan,label="witch state",)
    class Meta:
        model = Comment
        fields = ['text']
