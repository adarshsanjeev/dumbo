from django.contrib import admin
from .models import Project, Profile, Issue, Attachment

admin.site.register(Profile)
admin.site.register(Project)
admin.site.register(Issue)
admin.site.register(Attachment)
