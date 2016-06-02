from django.conf.urls import url, include
from django.contrib import admin
from dumbo import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.index, name="homepage"),
    
    url(r'^accounts/login/$', auth_views.login, name='login'),
    url(r'^accounts/register/$', views.register, name='register'),
    url(r'^accounts/logout/$', auth_views.logout, name='logout'),

    url(r'^user/my_projects/$', views.my_projects, name="my_projects"),
    url(r'^project/collab/(?P<slug>[\w-]*)/$', views.manage_collab, name="manage_collab"),
#     url(r'^user/profile/$', views.profile, name="profile"),
# 
    url(r'^project/create/$', views.create_project, name="create_project"),
    url(r'^project/edit/(?P<slug>[\w-]*)/$', views.edit_project, name="edit_project"),
    url(r'^project/view/(?P<slug>[\w-]*)/$', views.view_project, name="view_project"),
    url(r'^project/delete/(?P<slug>[\w-]*)/$', views.delete_project, name="delete_project"),
# 
#     url(r'^issue/create/$', views.create_issue, name="create_issue"),
#     url(r'^issue/view/(?P<issue_id>[0-9]*)/$', views.view_issue, name="view_issue"),
]
