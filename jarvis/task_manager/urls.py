from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list_view, name='task_list'),
    path('task/<int:task_id>/', views.task_detail_view, name='task_detail'),
    path('task/create/', views.task_create_view, name='task_create'),
    path('task/update/<int:task_id>/', views.task_update_view, name='task_update'),
    path('task/delete/<int:task_id>/', views.task_delete_view, name='task_delete'),
    path('tasklist/create/', views.task_list_create_view, name='task_list_create'),
    path('tasklist/edit/<int:task_list_id>/', views.task_list_edit_view, name='task_list_edit'),
    path('tasklist/delete/<int:task_list_id>/', views.task_list_delete_view, name='task_list_delete'),
]
