from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from .forms import TaskForm, TaskListForm, TagForm
from .models import Task, TaskList, Tag
from core.forms import FileUploadForm
from core.models import File


@login_required
def task_list_view(request):
    search_query = request.GET.get('q', '')
    tag_query = request.GET.get('tag', '')
    task_list_id = request.GET.get('task_list_id', None)

    tasks = Task.objects.filter(owner=request.user, is_completed=False)

    if search_query:
        tasks = tasks.filter(Q(title__icontains=search_query))

    if tag_query:
        tasks = tasks.filter(tags__name__icontains=tag_query).distinct()

    if task_list_id:
        tasks = tasks.filter(task_list_id=task_list_id)

    task_lists = TaskList.objects.filter(owner=request.user)

    return render(request, 'task_list.html',
                  {'tasks': tasks, 'task_lists': task_lists, 'selected_task_list': task_list_id})


@login_required
def task_detail_view(request, task_id):
    task = get_object_or_404(Task, id=task_id, owner=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_detail', task_id=task.id)
    else:
        form = TaskForm(instance=task)
    files = task.files.all()
    return render(request, 'task_detail.html', {'form': form, 'task': task, 'files': files})


@login_required
def task_create_view(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False, owner=request.user)
            task.owner = request.user
            task.save()

            new_tags = form.cleaned_data.get('new_tags')
            selected_tags = form.cleaned_data.get('tags')

            tags = list(selected_tags)
            if new_tags:
                tag_names = [name.strip() for name in new_tags.split(',')]
                new_tags = [Tag.objects.get_or_create(name=name, defaults={'owner': task.owner})[0] for name in
                            tag_names]
                tags.extend(new_tags)

            task.tags.set(tags)
            return redirect('task_list')
    else:
        form = TaskForm()

    return render(request, 'task_form.html', {'form': form})


@login_required
def task_update_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_manager:task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'task_form.html', {'form': form})


@login_required
def task_delete_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.delete()
        return redirect('task_manager:task_list')
    return render(request, 'task_confirm_delete.html', {'task': task})


@login_required
def task_list_create_view(request):
    if request.method == 'POST':
        form = TaskListForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_manager:task_list_manage')
    else:
        form = TaskListForm()
    return render(request, 'task_list_form.html', {'form': form})


@login_required
def task_list_edit_view(request, task_list_id):
    task_list = get_object_or_404(TaskList, id=task_list_id)
    if request.method == 'POST':
        form = TaskListForm(request.POST, instance=task_list)
        if form.is_valid():
            form.save()
            return redirect('task_manager:task_list_manage')
    else:
        form = TaskListForm(instance=task_list)
    return render(request, 'task_list_form.html', {'form': form})


@login_required
def task_list_delete_view(request, task_list_id):
    task_list = get_object_or_404(TaskList, id=task_list_id)
    if request.method == 'POST':
        if not Task.objects.filter(task_list=task_list).exists():
            task_list.delete()
            return redirect('task_manager:task_list_manage')
    return render(request, 'task_list_confirm_delete.html', {'task_list': task_list})


@login_required
def tag_manage_view(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_manager:tag_manage')
    else:
        form = TagForm()

    search_query = request.GET.get('search', '')
    tags = Tag.objects.filter(name__icontains=search_query)

    return render(request, 'tag_manage.html', {'form': form, 'tags': tags, 'search_query': search_query})


@login_required
def tag_create_view(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_manager:tag_manage')
    else:
        form = TagForm()
    return render(request, 'tag_form.html', {'form': form})


@login_required
def tag_delete_view(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    if request.method == 'POST':
        tag.delete()
        return redirect('task_manager:tag_manage')
    return render(request, 'tag_confirm_delete.html', {'tag': tag})


@login_required
def task_list_manage_view(request):
    if request.method == 'POST':
        form = TaskListForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_manager:task_list_manage')
    else:
        form = TaskListForm()

    search_query = request.GET.get('search', '')
    task_lists = TaskList.objects.filter(name__icontains=search_query)

    return render(request, 'task_list_manage.html',
                  {'form': form, 'task_lists': task_lists, 'search_query': search_query})


@login_required
def tag_edit_view(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    if request.method == 'POST':
        form = TagForm(request.POST, instance=tag)
        if form.is_valid():
            form.save()
            return redirect('task_manager:tag_manage')
    else:
        form = TagForm(instance=tag)
    return render(request, 'tag_form.html', {'form': form})


@login_required
def tasks_in_list_view(request, task_list_id):
    task_list = get_object_or_404(TaskList, id=task_list_id)
    tasks = Task.objects.filter(task_list=task_list, owner=request.user)
    return render(request, 'tasks_in_list.html', {'task_list': task_list, 'tasks': tasks})


@login_required
def check_tasks_in_list(request, task_list_id):
    task_list = get_object_or_404(TaskList, id=task_list_id, owner=request.user)
    has_tasks = Task.objects.filter(task_list=task_list).exists()
    return JsonResponse({'has_tasks': has_tasks})


@login_required
def upload_file_for_task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id, owner=request.user)
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        form.instance.user = request.user
        if form.is_valid():
            file_instance = form.save(commit=False)
            file_instance.user = request.user
            file_instance.task = task
            file_instance.save()
            return redirect('task_manager:task_detail', task_id=task.id)
    else:
        form = FileUploadForm()

    return render(request, 'upload_file.html', {'form': form, 'task': task})


@login_required
def delete_file_for_task_view(request, file_id, task_id):
    file = get_object_or_404(File, id=file_id, user=request.user, task_id=task_id)
    if request.method == 'POST':
        file.delete()
        return redirect('task_detail', task_id=task_id)
    return render(request, 'confirm_delete.html', {'file': file})


@login_required
def completed_task_list(request):
    tasks = Task.objects.filter(owner=request.user, is_completed=True)
    return render(request, 'completed_task_list.html', {'tasks': tasks})


@login_required
def mark_task_as_completed(request, task_id):
    task = get_object_or_404(Task, id=task_id, owner=request.user)
    task.is_completed = True
    task.save()
    return redirect('task_list')
