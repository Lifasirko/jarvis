import os
import mimetypes
from datetime import date
from django.conf import settings
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST

from .forms import (
    CustomUserCreationForm, ProfileUpdateForm, AvatarForm, ProfileForm,
    CustomPasswordChangeForm, AvatarChoiceForm, FileUploadForm
)
from .models import CustomUser, File
from .chatgpt_service import get_chatgpt_response
from .battery_utils import get_battery_info
from task_manager.models import Task
from contacts.models import Contact


@login_required
def chat_view(request):
    response = None
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        response = get_chatgpt_response(prompt)
    return render(request, 'home.html', {'response': response})


@login_required
def home_view(request):
    today = date.today()
    tasks_today = Task.objects.filter(due_date=today, owner=request.user)
    birthdays_today = Contact.objects.filter(
        birthday__month=today.month, birthday__day=today.day, user=request.user
    )

    context = {
        'tasks_today': tasks_today,
        'birthdays_today': birthdays_today,
    }
    return render(request, 'home.html', context)


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@require_POST
def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def profile_view(request):
    if request.method == 'POST':
        profile_form = ProfileForm(
            request.POST, request.FILES, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('profile')
    else:
        profile_form = ProfileForm(instance=request.user)

    password_form = CustomPasswordChangeForm(user=request.user)

    return render(request, 'profile.html', {
        'profile_form': profile_form,
        'password_form': password_form,
    })


@login_required
def change_password_view(request):
    if request.method == 'POST':
        password_form = CustomPasswordChangeForm(
            data=request.POST, user=request.user)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            return redirect('profile')
    else:
        password_form = CustomPasswordChangeForm(user=request.user)

    return render(request, 'profile.html', {
        'password_form': password_form,
        'profile_form': ProfileForm(instance=request.user),
    })


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    html_email_template_name = 'password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')
    success_message = "An email with instructions to reset your password has been sent to %(email)s."
    subject_template_name = 'password_reset_subject.txt'


@login_required
def update_profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'core/update_profile.html', {'form': form})


@login_required
def choose_avatar(request):
    user = request.user
    avatar_dir = os.path.join(settings.MEDIA_ROOT, 'avatars')
    avatar_choices = [f for f in os.listdir(
        avatar_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]

    if request.method == 'POST':
        form = AvatarChoiceForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')

    return render(request, 'choose_avatar.html', {
        'avatar_choices': avatar_choices,
        'current_avatar': user.avatar_choice
    })


@login_required
def upload_avatar(request):
    if request.method == 'POST':
        form = AvatarForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = AvatarForm(instance=request.user)
    return render(request, 'upload_avatar.html', {'form': form})


@login_required
def file_list_view(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    files = File.objects.filter(user=request.user)

    if query:
        files = files.filter(name__icontains=query)
    if category:
        files = files.filter(category=category)

    total_files = files.count()
    image_files = files.filter(category='image').count()
    document_files = files.filter(category='document').count()
    video_files = files.filter(category='video').count()
    other_files = files.filter(category='other').count()

    used_storage = request.user.get_used_storage() / (1024 * 1024)
    storage_limit = request.user.storage_limit / (1024 * 1024)  
    free_storage = storage_limit - used_storage

    context = {
        'files': files,
        'selected_category': category,
        'query': query,
        'total_files': total_files,
        'image_files': image_files,
        'document_files': document_files,
        'video_files': video_files,
        'other_files': other_files,
        'used_storage': used_storage,
        'storage_limit': storage_limit,
        'free_storage': free_storage,
    }

    return render(request, 'file_list.html', context)


@login_required
def upload_file_view(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        form.instance.user = request.user
        if form.is_valid():
            file_instance = form.save(commit=False)
            file_instance.user = request.user

            mime_type, _ = mimetypes.guess_type(file_instance.file.name)
            if not form.cleaned_data['category']:
                if mime_type:
                    if mime_type.startswith('image'):
                        file_instance.category = 'image'
                    elif mime_type.startswith('video'):
                        file_instance.category = 'video'
                    elif mime_type in ['application/pdf', 'application/msword',
                                       'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
                        file_instance.category = 'document'
                    else:
                        file_instance.category = 'other'
                else:
                    file_instance.category = 'other'

            file_instance.name = file_instance.file.name
            file_instance.save()
            return redirect('file_list')
    else:
        form = FileUploadForm()

    return render(request, 'upload_file.html', {'form': form, 'max_file_size': settings.MAX_FILE_SIZE})


@login_required
def delete_file_view(request, file_id):
    file = get_object_or_404(File, id=file_id, user=request.user)
    if request.method == 'POST':
        file.delete()
        return redirect('file_list')
    return render(request, 'confirm_delete.html', {'file': file})


@login_required
def user_list_view(request):
    users = CustomUser.objects.all()
    return render(request, 'user_list.html', {'users': users})


@login_required
def delete_user_view(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.delete()
    return redirect('user_list')


def get_battery_status(request):
    battery_level, battery_status = get_battery_info()
    return JsonResponse({
        'battery_level': battery_level,
        'battery_status': battery_status
    })


def game(request):
    return render(request, 'game.html')
