from __future__ import unicode_literals

from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User, Group, Permission
from django.utils import timezone
from django.template.defaultfilters import slugify
from django import forms

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    profile_pic = models.ImageField("Profile Picture", blank = True, upload_to = "profile_picture/")
    about = models.TextField("About yourself", blank = True)
    private = models.BooleanField("Keep my Profile private", default = False)

class UserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic', 'about', 'private']
