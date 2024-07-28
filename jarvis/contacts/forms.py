from django import forms
from phonenumber_field.formfields import PhoneNumberField
import datetime

from .models import Contact


class ContactForm(forms.ModelForm):
    name = forms.CharField(
        required=True,
        min_length=1,
        max_length=255
    )
    address = forms.CharField(
        required=True,
        max_length=255
    )
    phone_number = PhoneNumberField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=True
    )
    birthday = forms.DateField(
        required=False
    )

    class Meta:
        model = Contact
        fields = ['name', 'address', 'phone_number', 'email', 'birthday']
        exclude = ['user']

    # def clean_name(self):
    #     name = self.cleaned_data.get('name')
    #     if not name.isalpha():
    #         raise forms.ValidationError("Name should only contain alphabetic characters.")
    #     return name

    def clean_birthday(self):
        birthday = self.cleaned_data.get('birthday')
        if birthday and birthday > datetime.date.today():
            raise forms.ValidationError("Birthday cannot be in the future.")
        return birthday
