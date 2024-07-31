import mimetypes
import os
from datetime import date, timedelta

from contacts.models import Contact
# from .rss_feed import fetch_rss_feed
# import feedparser
from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from task_manager.models import Task

from .battery_utils import get_battery_info
from .chatgpt_service import get_chatgpt_response
from .forms import CustomUserCreationForm, AvatarForm, AvatarChoiceForm, ProfileUpdateForm
from .forms import FileUploadForm
from .forms import ProfileForm, CustomPasswordChangeForm
from .models import CustomUser
from .models import File


# def news_view(request):
#     rss_url = 'https://www.liga.net/news/all/rss.xml'
#     news_items = fetch_rss_feed(rss_url)
#     return render(request, 'news.html', {'news_items': news_items})
#

def chat_view(request):
    response = None
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        response = get_chatgpt_response(prompt)
    return render(request, 'home.html', {'response': response})


@login_required
def home_view(request):
    """
    Renders the home page with tasks due today and birthdays today.
    """
    today = date.today()
    tasks_today = Task.objects.filter(due_date=today, owner=request.user)

    next_week = today + timedelta(days=7)
    contacts = Contact.objects.filter(user=request.user).order_by('name')
    upcoming_birthdays = []
    for contact in contacts:
        if contact.birthday:
            birthday_this_year = contact.birthday.replace(year=today.year)
            if today <= birthday_this_year <= next_week:
                upcoming_birthdays.append(contact)

    response = None
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        response = get_chatgpt_response(prompt)
    context = {
        'tasks_today': tasks_today,
        'birthdays_today': upcoming_birthdays,
        'response': response,
    }
    return render(request, 'home.html', context)


def register_view(request):
    """
    Handles the user registration process. If the request method is POST, it will
    validate the form and create a new user. If the form is valid, the user is logged
    in and redirected to the home page. If the request method is GET, it will render
    an empty registration form.

    Args:
        request (HttpRequest): The request object used to generate this response.

    Returns:
        HttpResponse: The rendered registration page with the form.
    """
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
    """
    Handles the user login process. If the request method is POST, it will validate
    the form and authenticate the user. If the credentials are valid, the user is logged
    in and redirected to the home page. If the request method is GET, it will render
    an empty login form.

    Args:
        request (HttpRequest): The request object used to generate this response.

    Returns:
        HttpResponse: The rendered login page with the form.
    """
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
    """
    Handles the user logout process. This view requires a POST request for security
    reasons. Upon logging out, the user is redirected to the home page.

    Args:
        request (HttpRequest): The request object used to generate this response.

    Returns:
        HttpResponse: A redirect to the home page.
    """
    logout(request)
    return redirect('home')


@login_required
def profile_view(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user)
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
        password_form = CustomPasswordChangeForm(data=request.POST, user=request.user)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Important!
            return redirect('profile')
    else:
        password_form = CustomPasswordChangeForm(user=request.user)

    return render(request, 'profile.html', {
        'password_form': password_form,
        'profile_form': ProfileForm(instance=request.user),
    })


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    """
    Handles the password reset process. This view sends an email to the user with instructions
    to reset their password.

    Attributes:
        template_name (str): The template to render for the password reset form.
        email_template_name (str): The template to use for the password reset email.
        html_email_template_name (str): The HTML template to use for the password reset email.
        success_url (str): The URL to redirect to after successfully sending the password reset email.
        success_message (str): The message to display upon successful email sending.
        subject_template_name (str): The template for the email subject.
    """
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    html_email_template_name = 'password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')
    success_message = "An email with instructions to reset your password has been sent to %(email)s."
    subject_template_name = 'password_reset_subject.txt'


# @login_required
# def contact_list_view(request):
#     """
#     Renders the contact list page. This view requires the user to be logged in.
#
#     Args:
#         request (HttpRequest): The request object used to generate this response.
#
#     Returns:
#         HttpResponse: The rendered contact list page.
#     """
#     return render(request, 'contact_list.html')

@login_required
def file_list_view(request):
    """
    Renders the file list page with the ability to filter files by name and category.
    This view requires the user to be logged in.

    Args:
        request (HttpRequest): The request object used to generate this response.

    Returns:
        HttpResponse: The rendered file list page with the files and statistics.
    """
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    files = File.objects.filter(user=request.user)

    if query:
        files = files.filter(name__icontains=query)
    if category:
        files = files.filter(category=category)

    # Count files by categories
    total_files = files.count()
    image_files = files.filter(category='image').count()
    document_files = files.filter(category='document').count()
    video_files = files.filter(category='video').count()
    other_files = files.filter(category='other').count()

    # Storage statistics
    used_storage = request.user.get_used_storage() / (1024 * 1024)  # Convert to MB
    storage_limit = request.user.storage_limit / (1024 * 1024)  # Convert to MB
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
    """
    Handles the file upload process. If the request method is POST, it will validate
    the form and save the uploaded file. If the form is valid, the file is saved and
    the user is redirected to the file list page. If the request method is GET, it will
    render an empty file upload form.

    Args:
        request (HttpRequest): The request object used to generate this response.

    Returns:
        HttpResponse: The rendered file upload page with the form.
    """
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
    """
    Handles the file deletion process. This view requires the user to be logged in.
    If the request method is POST, it will delete the specified file.

    Args:
        request (HttpRequest): The request object used to generate this response.
        file_id (int): The ID of the file to be deleted.

    Returns:
        HttpResponse: A redirect to the file list page after successful deletion.
    """
    file = get_object_or_404(File, id=file_id, user=request.user)
    if request.method == 'POST':
        file.delete()
        return redirect('file_list')
    return render(request, 'confirm_delete.html', {'file': file})


# @login_required
# def news_view(request):
#     """
#     Renders the news page. This view requires the user to be logged in.

#     Args:
#         request (HttpRequest): The request object used to generate this response.

#     Returns:
#         HttpResponse: The rendered news page.
#     """
#     return render(request, 'news.html')


@login_required
def user_list_view(request):
    """
    Renders the user list page. This view requires the user to be logged in.

    Args:
        request (HttpRequest): The request object used to generate this response.

    Returns:
        HttpResponse: The rendered user list page with the list of users.
    """
    users = CustomUser.objects.all()
    return render(request, 'user_list.html', {'users': users})


@login_required
def delete_user_view(request, user_id):
    """
    Handles the user deletion process. This view requires the user to be logged in.
    If the request method is POST, it will delete the specified user.

    Args:
        request (HttpRequest): The request object used to generate this response.
        user_id (int): The ID of the user to be deleted.

    Returns:
        HttpResponse: A redirect to the user list page after successful deletion.
    """
    user = get_object_or_404(CustomUser, id=user_id)
    user.delete()
    return redirect('user_list')


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


def get_battery_status(request):
    battery_level, battery_status = get_battery_info()
    return JsonResponse({
        'battery_level': battery_level,
        'battery_status': battery_status
    })


def game(request):
    return render(request, 'game.html')
