from django.urls import path

from .views import home_view, register_view, login_view, logout_view, contact_list_view, \
    file_list_view, news_view

urlpatterns = [
    path('', home_view, name='home'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    # path('dashboard/', dashboard_view, name='dashboard'),
    path('contacts/', contact_list_view, name='contact_list'),
    path('files/', file_list_view, name='file_list'),
    path('news/', news_view, name='news'),
]
