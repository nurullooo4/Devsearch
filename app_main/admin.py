from django.contrib import admin
from .models import Tag, Project, Message, Comment

admin.site.register(Tag)
admin.site.register(Project)
admin.site.register(Message)
admin.site.register(Comment)
