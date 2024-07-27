from django.urls import path
from . import views

app_name = 'task_manager'

urlpatterns = [
    path('', views.task_list_view, name='task_list'),
    path('task/<int:task_id>/', views.task_detail_view, name='task_detail'),
    path('task/create/', views.task_create_view, name='task_create'),
    path('task/update/<int:task_id>/', views.task_update_view, name='task_update'),
    path('task/delete/<int:task_id>/', views.task_delete_view, name='task_delete'),
    path('task_list/create/', views.task_list_create_view, name='task_list_create'),
    path('task_list/update/<int:task_list_id>/', views.task_list_edit_view, name='task_list_edit'),
    path('task_list/delete/<int:task_list_id>/', views.task_list_delete_view, name='task_list_delete'),
    path('tags/manage/', views.tag_manage_view, name='tag_manage'),
    path('tags/create/', views.tag_create_view, name='tag_create'),
    path('tags/delete/<int:tag_id>/', views.tag_delete_view, name='tag_delete'),
    path('tags/edit/<int:tag_id>/', views.tag_edit_view, name='tag_edit'),
    path('task_list/manage/', views.task_list_manage_view, name='task_list_manage'),
    path('task_list/<int:task_list_id>/tasks/', views.tasks_in_list_view, name='tasks_in_list'),
    path('task_list/<int:task_list_id>/check_tasks/', views.check_tasks_in_list, name='check_tasks_in_list'),

]
