from django.urls import path
from . import views

app_name = "notes"

urlpatterns = [
    path('', views.note_list, name='note_list'),
    path('<int:pk>/', views.note_detail, name='note_detail'),
    path('new/', views.note_create, name='note_create'),
    path('tags/manage/', views.tag_manage, name='tag_manage'),
    path('tags/manage/delete/<int:delete_tag_id>/', views.tag_manage, name='tag_manage_with_delete'),
    path('tags/create/', views.tag_create, name='tag_create'),
    path('<int:pk>/edit/', views.note_edit, name='note_edit'),
    path('<int:pk>/delete/', views.note_delete, name='note_delete'),

    path('note/<int:note_id>/upload_file/', views.upload_file_for_note_view, name='upload_file_for_note'),
    path('note/<int:note_id>/delete_file/<int:file_id>/', views.delete_file_for_note_view, name='delete_file_for_note'),
]
