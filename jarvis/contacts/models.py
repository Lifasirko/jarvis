from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from core.models import CustomUser


# Create your models here.

class Contact(models.Model):
    """
    Model to store contact information for users.

    Attributes:
        user (ForeignKey): The user to whom this contact belongs. Links to the CustomUser model.
        name (CharField): The name of the contact. Maximum length of 255 characters.
        address (CharField): The address of the contact. Maximum length of 255 characters.
        phone_number (CharField): The phone number of the contact. Maximum length of 15 characters.
        email (EmailField): The email address of the contact.
        birthday (DateField): The birthday of the contact.
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='contacts_from_contacts')
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    email = models.EmailField()
    birthday = models.DateField(blank=True, null=True)
