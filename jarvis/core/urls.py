from django.contrib.auth.views import PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path

from . import views
from .views import home_view, register_view, login_view, logout_view, file_list_view, user_list_view, \
    delete_user_view, upload_file_view, delete_file_view, profile_view, change_password_view, \
    upload_avatar, choose_avatar, update_profile_view
from notes.views import note_list
from contacts.views import contact_list_view
from news.views import news_list
from task_manager.views import task_list_view

urlpatterns = [
    path('', home_view, name='home'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('reset-password/', views.ResetPasswordView.as_view(), name='password_reset'),
    path('reset-password/done/', PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset-password/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html',
         success_url='/reset-password/complete/'), name='password_reset_confirm'),
    path('reset-password/complete/', PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html'), name='password_reset_complete'),

    path('profile/', profile_view, name='profile'),
    path('profile/update/', update_profile_view, name='update_profile'),
    path('profile/change-password/', change_password_view, name='change_password'),

    path('contacts/', contact_list_view, name='contact_list'),

    path('notes/', note_list, name='note_list'),

    path('files/', file_list_view, name='file_list'),
    path('files/upload/', upload_file_view, name='upload_file'),
    path('files/delete/<int:file_id>/', delete_file_view, name='delete_file'),

    path('news/', news_list, name='news'),

    path('tasks/', task_list_view, name='task_list'),

    path('users/', user_list_view, name='user_list'),
    path('users/delete/<int:user_id>/', delete_user_view, name='delete_user'),

    path('choose-avatar/', choose_avatar, name='choose_avatar'),
    path('upload-avatar/', upload_avatar, name='upload_avatar'),

    path('game/', views.game, name='game'),
    path('get-battery-status/', views.get_battery_status,
         name='get_battery_status'),

    path('', views.chat_view, name='home'),
]
