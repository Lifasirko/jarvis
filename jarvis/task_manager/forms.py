from django import forms
from .models import Task, TaskList


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'task_list', 'completed', 'tags']
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class TaskListForm(forms.ModelForm):
    class Meta:
        model = TaskList
        fields = ['name']
