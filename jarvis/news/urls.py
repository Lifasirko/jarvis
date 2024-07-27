from django.urls import path

from . import views

app_name = 'news'

urlpatterns = [
    path('news/', views.news_list, name='news_list'),
    path('news/<int:page>/', views.news_list, name='news_list'),
    path('news/<str:title>/', views.news_detail, name='news_detail'),
    path('news_update', views.news_update, name='news_update'),
]