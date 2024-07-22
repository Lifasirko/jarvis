from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST

from .forms import CustomUserCreationForm
from .forms import FileUploadForm
from .models import CustomUser
from .models import File


def home_view(request):
    """
    Renders the home page.

    Args:
        request (HttpRequest): The request object used to generate this response.

    Returns:
        HttpResponse: The rendered home page.
    """
    return render(request, 'home.html')


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


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    html_email_template_name = 'password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')
    success_message = "An email with instructions to reset your password has been sent to %(email)s."
    subject_template_name = 'password_reset_subject.txt'


# @login_required
# def dashboard_view(request):
#     """
#     Renders the dashboard page. This view requires the user to be logged in.
#
#     Args:
#         request (HttpRequest): The request object used to generate this response.
#
#     Returns:
#         HttpResponse: The rendered dashboard page.
#     """
#     return render(request, 'dashboard.html')


@login_required
def contact_list_view(request):
    """
    Renders the contact list page. This view requires the user to be logged in.

    Args:
        request (HttpRequest): The request object used to generate this response.

    Returns:
        HttpResponse: The rendered contact list page.
    """
    return render(request, 'contact_list.html')


@login_required
def note_list_view(request):
    """
    Renders the note list page. This view requires the user to be logged in.

    Args:
        request (HttpRequest): The request object used to generate this response.

    Returns:
        HttpResponse: The rendered note list page.
    """
    return render(request, 'note_list.html')


@login_required
def file_list_view(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    files = File.objects.filter(user=request.user)

    if query:
        files = files.filter(name__icontains=query)
    if category:
        files = files.filter(category=category)

    context = {
        'files': files,
        'selected_category': category,
        'query': query,
    }

    return render(request, 'file_list.html', context)


@login_required
def upload_file_view(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file_instance = form.save(commit=False)
            file_instance.user = request.user
            file_instance.save()
            return redirect('file_list')
    else:
        form = FileUploadForm()
    return render(request, 'upload_file.html', {'form': form})


@login_required
def news_view(request):
    """
    Renders the news page. This view requires the user to be logged in.

    Args:
        request (HttpRequest): The request object used to generate this response.

    Returns:
        HttpResponse: The rendered news page.
    """
    return render(request, 'news.html')


@login_required
def user_list_view(request):
    users = CustomUser.objects.all()
    return render(request, 'user_list.html', {'users': users})


@login_required
def delete_user_view(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.delete()
    return redirect('user_list')
