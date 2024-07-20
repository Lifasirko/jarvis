from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import CustomUser


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

    email = forms.EmailField(required=True)

    class Meta:
        """
        The Meta class defines metadata for the form, such as the model to use
        and the fields to include in the form.
        """
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')
