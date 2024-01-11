from django.contrib import admin

from .models import *

admin.site.register(Assignee)
admin.site.register(Member)
admin.site.register(Project)
admin.site.register(Sprint)
admin.site.register(Tag)
admin.site.register(Task)
admin.site.register(User)
