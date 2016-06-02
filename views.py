from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.forms.widgets import HiddenInput
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import UserForm, ProfileForm, Profile, Project, ProjectForm
from datetime import datetime

def index(request):
    return render(request, "index.html", {})

def register(request):
    if request.POST:
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            print user.password
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return HttpResponseRedirect('/')
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
    return render(request, 'registration/register.html', {'user':user_form, 'profile':profile_form})

@login_required
def create_project(request):
    if request.POST:
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.cleaned_data['owner'] = request.user
            project = form.save()
            return HttpResponseRedirect('/project/view/%s' %(project.slug))
    else:
        form = ProjectForm(initial={'owner':request.user, 'slug':request.user})
        form.fields['owner'].widget = HiddenInput()
    return render(request, "form_template.html", {'form':form})

def view_project(request, slug):
    project = get_object_or_404(Project, slug=slug)
    # issues = Issue.objects.filter(project=project)
    return render(request, "view_project.html", {'project':project})

@login_required
def edit_project(request, slug):
    project = get_object_or_404(Project, slug=slug)
    if request.method == "POST":
        form = ProjectForm(request.POST, instance = project)
        form.fields['owner'].widget = HiddenInput()
        if form.is_valid():
            form.cleaned_data['owner'] = request.user
            project.save()
            return HttpResponseRedirect('/project/view/%s' %(project.slug))        
    else:
        form = ProjectForm(instance = project)
        form.fields['owner'].widget = HiddenInput()
    return render(request, "form_template.html", {'form':form})

@login_required(login_url="/user/login/")
def delete_project(request, slug):
    get_object_or_404(Project, slug=slug, owner=request.user).delete()
    return HttpResponseRedirect("/")
