from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import CustomUser, File


class CustomUserCreationForm(UserCreationForm):
    """
    CustomUserCreationForm is a form for creating a new user with an additional email field.
    It inherits functionality from the standard UserCreationForm, which is part of
    django.contrib.auth.forms.

    Attributes:
    email (forms.EmailField): A required field for entering the user's email.

    Meta:
        model (CustomUser): The model used for creating the user.
        fields (tuple): The form fields that will be displayed in the template.
    """
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput())
    email = forms.CharField(max_length=100, required=True, widget=forms.TextInput())
    password1 = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput())

    class Meta:
        """
        The Meta class defines metadata for the form, such as the model to use
        and the fields to include in the form.
        """
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    """
    LoginForm is a form for logging in a user. It inherits functionality from
    django.contrib.auth.forms.AuthenticationForm.

    Meta:
        model (User): The model used for authentication.
        fields (list): The form fields that will be displayed in the template.
    """

    class Meta:
        model = User
        fields = ['username', 'password']


class FileUploadForm(forms.ModelForm):
    """
    FileUploadForm is a form for uploading a file. It uses the File model and allows
    the user to upload a file, select a category, and provide a name for the file.

    Meta:
        model (File): The model used for uploading files.
        fields (list): The form fields that will be displayed in the template.
        widgets (dict): Custom widgets for form fields.
    """

    class Meta:
        model = File
        fields = ['file', 'category', 'name']
        widgets = {
            'category': forms.Select(choices=File.CATEGORY_CHOICES),
            'name': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.file:
            self.fields['name'].initial = self.instance.file.name

    def clean_file(self):
        file = self.cleaned_data.get('file')
        user = self.instance.user

        if file.size > settings.MAX_FILE_SIZE:
            raise forms.ValidationError(f'File size must be under {settings.MAX_FILE_SIZE / (1024 * 1024)} MB. Current file size is {file.size / (1024 * 1024)} MB.')

        if user.get_used_storage() + file.size > user.storage_limit:
            raise forms.ValidationError('You have exceeded your storage limit.')

        return file

# class ProfileForm(forms.ModelForm):
#     avatar = forms.ImageField(widget=forms.FileInput())
#
#     class Meta:
#         model = Profile
#         fields = ['avatar']
