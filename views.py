from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.forms.widgets import HiddenInput
from django.contrib.auth.models import User, Group, Permission
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import UserForm, ProfileForm, Profile, Project, ProjectForm, Issue, IssueForm, Attachment, Comment
from datetime import datetime

def index(request):
    new_projects = Project.objects.filter(private=False)
    return render(request, "index.html", {'new_projects':new_projects})

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
        g = Group.objects.get_or_create(name=request.user.username)
        form = ProjectForm(initial={'owner':request.user, 'slug':request.user, 'group':g})
        form.fields['owner'].widget = HiddenInput()
        form.fields['group'].widget = HiddenInput()
    return render(request, "form_template.html", {'form':form})

def view_project(request, slug):
    project = get_object_or_404(Project, slug=slug)
    if project.private is True and request.user not in project.group.user_set.all():
        return Http404("Page not Found")
    issues = Issue.objects.filter(project=project)
    return render(request, "view_project.html", {'project':project, 'issues':issues})

@login_required
def edit_project(request, slug):
    project = get_object_or_404(Project, slug=slug)
    if project.private is True and request.user not in project.group.user_set.all():
        return Http404("Page not Found")
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

@login_required
def delete_collab(request):
    if request.method == "POST":
        slug = request.POST.get("project")
        project = get_object_or_404(Project, slug=slug, owner=request.user)
        user = User.objects.get(username=request.POST.get("username"))
        project.group.user_set.remove(user)
        return HttpResponseRedirect("/project/collab/%s" %(project.slug))
    return Http404("No")

@login_required
def create_issue(request, slug):
    project = get_object_or_404(Project, slug=slug, owner=request.user)
    if project.private is True and request.user not in project.group.user_set.all():
        return Http404("Page not Found")
    if request.method == "POST":
        form = IssueForm(request.POST, request.FILES)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.user = request.user
            issue.tag = "UNCONFIRMED"
            issue.project = project
            issue.save()
            if request.FILES:
                attachment = Attachment(attachment=request.FILES['attachment'], issue = issue, user=request.user)
                attachment.save()
            return HttpResponseRedirect("/project/view/%s" %(project.slug))
    else:
        form = IssueForm(initial={'tag':'UNCONFIRMED', 'author':request.user, 'project':project})
    return render(request, "form_template.html", {"form":form})

@login_required
def create_comment(request, issue_id):
    if request.method =="POST":
        issue = get_object_or_404(Issue, id=issue_id)
        comment = Comment(issue=issue, author=request.user, comment=request.POST['comment'])
        comment.save()
        return HttpResponseRedirect("/issue/view/%s" %(issue_id))
    return Http404("No")

@login_required
def upload_file(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)
    if request.method =="POST":
        attachment = Attachment(attachment=request.FILES['attachment'], issue = issue, user=request.user)
        attachment.save()
        return HttpResponseRedirect("/issue/view/%s" %(issue_id))
    return Http404("No")

def view_issue(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)
    comments = Comment.objects.filter(issue=issue)
    attachments = Attachment.objects.filter(issue=issue)
    project = issue.project
    if project.private is True and request.user not in project.group.user_set.all():
        return Http404("Page not Found")
    return render(request, "view_issue.html", {"issue":issue, "attachments":attachments, "comments":comments})

@login_required
def edit_issue(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)
    project = issue.project
    if request.method == "POST":
        form = IssueForm(request.POST, request.FILES)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.user = request.user
            issue.project = project
            issue.save()
            return HttpResponseRedirect("/project/view/%s" %(project.slug))
    else:
        form = IssueForm(instance=issue)
    form.fields['attachment'].widget = HiddenInput()
    return render(request, "form_template.html", {'issue':issue, 'project':project, 'form':form})

@login_required
def profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    projects = Project.objects.filter(owner=request.user)
    return render(request, "profile.html", {"profile":profile, "projects":projects})
