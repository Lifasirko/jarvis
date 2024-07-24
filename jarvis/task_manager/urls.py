from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list_view, name='task_list'),
    path('task/<int:task_id>/', views.task_detail_view, name='task_detail'),
    path('task/new/', views.task_create_view, name='task_create'),
    path('task/<int:task_id>/edit/', views.task_update_view, name='task_edit'),
    path('task/<int:task_id>/delete/', views.task_delete_view, name='task_delete'),
    path('task_list/new/', views.task_list_create_view, name='task_list_create'),
    path('task_list/<int:task_list_id>/edit/', views.task_list_edit_view, name='task_list_edit'),
    path('task_list/<int:task_list_id>/delete/', views.task_list_delete_view, name='task_list_delete'),
]
