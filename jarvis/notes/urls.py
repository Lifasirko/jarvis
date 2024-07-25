from django.urls import path
from . import views

app_name = "notes"

urlpatterns = [
    path('', views.note_list, name='note_list'),
    path('<int:pk>/', views.note_detail, name='note_detail'),
    path('new/', views.note_create, name='note_create'),
    path('new_tag/', views.tag_create, name='tag_create'),
    path('<int:pk>/edit/', views.note_edit, name='note_edit'),
    path('<int:pk>/delete/', views.note_delete, name='note_delete')
]
