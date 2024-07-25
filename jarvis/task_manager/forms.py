from django import forms

from .models import Task, TaskList, Tag


class TaskForm(forms.ModelForm):
    new_task_list = forms.CharField(required=False, label='New Task List')
    new_tags = forms.CharField(required=False, label='New Tags', help_text="Comma-separated")

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'task_list', 'tags']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def save(self, commit=True, owner=None):
        task = super().save(commit=False)
        if owner:
            task.owner = owner

        new_task_list_name = self.cleaned_data.get('new_task_list')
        selected_task_list = self.cleaned_data.get('task_list')

        if new_task_list_name:
            task_list, created = TaskList.objects.get_or_create(name=new_task_list_name, owner=task.owner)
        elif selected_task_list == 'general':
            task_list, created = TaskList.objects.get_or_create(name='General', owner=task.owner)
        else:
            task_list = selected_task_list

        task.task_list = task_list
        print("------------------------------------------------------------------------------------------------")
        print(f"task.task_list = {task.task_list}")

        if commit:
            task.save()

        new_tags = self.cleaned_data.get('new_tags')
        print("------------------------------------------------------------------------------------------------")
        print(f"new_tags = {new_tags}")
        if new_tags:
            tag_names = [name.strip() for name in new_tags.split(',')]
            tags = [Tag.objects.get_or_create(name=name, defaults={'owner': task.owner})[0] for name in tag_names]
            print(f"tags saved: {tags}")

            task.save()

            print(f"2Task saved: {task.tags}")

            task.tags.set(tags)
            print(f"3Task saved: {task.tags}")

            task.save()
            print(f"4Task saved: {task.tags}")

        print("------------------------------------------------------------------------------------------------")
        print(f"task.tags = {task.tags}")
        print(f"task.tags.set(tags) = {task.tags.set(tags)}")

        if commit:
            task.save()
            self.save_m2m()

        return task


class TaskListForm(forms.ModelForm):
    class Meta:
        model = TaskList
        fields = ['name']
