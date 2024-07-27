from django.shortcuts import render, get_object_or_404, redirect
from .models import Task, TaskList, Tag
from .forms import TaskForm, TaskListForm, TagForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q


@login_required
def task_list_view(request):
    search_query = request.GET.get('q', '')
    tag_query = request.GET.get('tag', '')

    tasks = Task.objects.filter(owner=request.user)

    if search_query:
        tasks = tasks.filter(Q(title__icontains=search_query))

    if tag_query:
        tasks = tasks.filter(tags__name__icontains=tag_query).distinct()

    return render(request, 'task_list.html', {'tasks': tasks})


@login_required
def task_detail_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    return render(request, 'task_detail.html', {'task': task})


@login_required
def task_create_view(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user
            task.save()
            form.save_m2m()
            return redirect('task_manager:task_list')
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
