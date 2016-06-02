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

class Project(models.Model):
    name = models.CharField("Project Name", max_length = 20)
    slug = models.SlugField(blank = True, unique = True)
    link = models.URLField(blank = True)
    details = models.TextField("About your project")
    owner = models.ForeignKey(User, on_delete = models.CASCADE)
    group = models.ForeignKey(Group, on_delete = models.CASCADE)

    def __unicode__(self):
        return "%s : %s" %(self.name, self.details)

    def save(self, *args, **kwargs):
        if self.slug == self.owner.username:
            ps = slugify(self.name)
            self.slug = ps
            counter = 1
            while Project.objects.filter(slug=self.slug).exists():
                self.slug = ps+str(counter)
                counter += 1
            self.group, c = Group.objects.get_or_create(name=self.slug)
            self.group.user_set.add(self.owner)
        super(Project, self).save(*args, **kwargs)

class ProjectForm(ModelForm):
    slug = forms.SlugField(widget=forms.HiddenInput())
    class Meta:
        model = Project
        exclude = []

class UserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic', 'about', 'private']
