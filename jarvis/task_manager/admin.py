from django.contrib import admin
from .models import TaskList, Tag, Task

admin.site.register(TaskList)
admin.site.register(Tag)
admin.site.register(Task)
