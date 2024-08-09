from django import forms
from .models import Post, Comment
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth.models import User
from taggit.forms import TagWidget


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'description', 'category', 'image', 'price']


    def save(self, commit=True):
        post = super(PostForm, self).save(commit=False)
        if commit:
            post.save()
        return post


class EditPostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'description', 'category', 'price']

    def save(self, commit=True):
        post = super(EditPostForm, self).save(commit=False)
        if commit:
            post.save()



class CommentForm(forms.ModelForm):
    class Meta: 
        model = Comment
        fields = ['name', 'email', 'body']


