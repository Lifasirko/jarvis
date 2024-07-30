from django.contrib import admin
from .models import Task, TaskList, Tag

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'due_date', 'is_completed', 'task_list', 'owner')
    list_filter = ('is_completed', 'due_date', 'task_list', 'tags')
    search_fields = ('title', 'description', 'tags__name')
    ordering = ('due_date',)

@admin.register(TaskList)
class TaskListAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner')
    search_fields = ('name', 'owner__username')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner')
    search_fields = ('name', 'owner__username')
