from django.urls import path
from . import views

app_name = 'task_manager'

urlpatterns = [
    path('', views.task_list_view, name='task_list'),
    path('task/<int:task_id>/', views.task_detail_view, name='task_detail'),
    path('task/create/', views.task_create_view, name='task_create'),
    path('task/<int:task_id>/edit/', views.task_update_view, name='task_update'),
    path('task/<int:task_id>/delete/', views.task_delete_view, name='task_delete'),
    path('task_list/create/', views.task_list_create_view, name='task_list_create'),
    path('task_list/<int:task_list_id>/edit/', views.task_list_edit_view, name='task_list_edit'),
    path('task_list/<int:task_list_id>/delete/', views.task_list_delete_view, name='task_list_delete'),
    path('tags/manage/', views.tag_manage_view, name='tag_manage'),
    path('tag/create/', views.tag_create_view, name='tag_create'),
    path('tag/<int:tag_id>/delete/', views.tag_delete_view, name='tag_delete'),
    path('task_lists/manage/', views.task_list_manage_view, name='task_list_manage'),
    path('tag/<int:tag_id>/edit/', views.tag_edit_view, name='tag_edit'),
    path('task_list/<int:task_list_id>/tasks/', views.tasks_in_list_view, name='tasks_in_list'),
    path('task_list/<int:task_list_id>/check_tasks/', views.check_tasks_in_list, name='check_tasks_in_list'),
    path('task/<int:task_id>/upload_file/', views.upload_file_for_task_view, name='upload_file_for_task'),
    path('task/<int:task_id>/delete_file/<int:file_id>/', views.delete_file_for_task_view, name='delete_file_for_task'),
    path('completed_tasks/', views.completed_task_list, name='completed_task_list'),
    path('mark_completed/<int:task_id>/', views.mark_task_as_completed, name='mark_task_as_completed'),
]
