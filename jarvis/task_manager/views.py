from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, TaskList
from .forms import TaskForm, TaskListForm


def task_list_view(request):
    task_lists = TaskList.objects.filter(owner=request.user)
    return render(request, 'task_list.html', {'task_lists': task_lists})


def task_detail_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    return render(request, 'task_detail.html', {'task': task})


def task_create_view(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user
            task.save()
            form.save_m2m()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'task_form.html', {'form': form})


def task_update_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_detail', task_id=task.id)
    else:
        form = TaskForm(instance=task)
    return render(request, 'task_form.html', {'form': form})


def task_delete_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'task_confirm_delete.html', {'task': task})


def task_list_create_view(request):
    if request.method == 'POST':
        form = TaskListForm(request.POST)
        if form.is_valid():
            task_list = form.save(commit=False)
            task_list.owner = request.user
            task_list.save()
            return redirect('task_list')
    else:
        form = TaskListForm()
    return render(request, 'task_list_form.html', {'form': form})


def task_list_edit_view(request, task_list_id):
    task_list = get_object_or_404(TaskList, id=task_list_id)
    if request.method == 'POST':
        form = TaskListForm(request.POST, instance=task_list)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskListForm(instance=task_list)
    return render(request, 'task_list_form.html', {'form': form})


def task_list_delete_view(request, task_list_id):
    task_list = get_object_or_404(TaskList, id=task_list_id)
    if request.method == 'POST':
        task_list.delete()
        return redirect('task_list')
    return render(request, 'task_list_confirm_delete.html', {'task_list': task_list})
