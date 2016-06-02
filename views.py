
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.forms.widgets import HiddenInput
from django.contrib.auth.models import User, Group, Permission
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
        g = Group.objects.get(name=request.user.username)
        form = ProjectForm(initial={'owner':request.user, 'slug':request.user, 'group':g})
        form.fields['owner'].widget = HiddenInput()
        form.fields['group'].widget = HiddenInput()
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

@login_required
def delete_project(request, slug):
    get_object_or_404(Project, slug=slug, owner=request.user).delete()
    return HttpResponseRedirect("/")

@login_required
def my_projects(request):
    projects = Project.objects.filter(owner=request.user)
    return render(request, "my_projects.html", {"projects":projects})

@login_required
def manage_collab(request, slug):
    project = get_object_or_404(Project, slug=slug, owner=request.user)
    if request.method == "POST":
        username = request.POST.get("username")
        user = User.objects.get(username=username)
        project.group.user_set.add(user)
    collab_list = project.group.user_set.all()
    return render(request, "collab.html", {"project":project, "collab_list":collab_list})
