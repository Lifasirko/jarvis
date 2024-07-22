from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Custom user model that extends Django's built-in AbstractUser.

    This model inherits from Django's AbstractUser and does not add any additional fields or methods.
    It is used to customize the user model if needed in the future.
    """
    pass


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
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    birthday = models.DateField()


class Note(models.Model):
    """
    Model to store notes for users.

    Attributes:
        user (ForeignKey): The user to whom this note belongs. Links to the CustomUser model.
        content (TextField): The content of the note.
        tags (CharField): Tags associated with the note. Maximum length of 255 characters.
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    tags = models.CharField(max_length=255)


def user_directory_path(instance, filename):
    # Файли будуть завантажуватися в MEDIA_ROOT/user_<id>/<filename>
    return f'user_{instance.user.id}/{filename}'


class File(models.Model):
    CATEGORY_CHOICES = [
        ('image', 'Image'),
        ('document', 'Document'),
        ('video', 'Video'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    file = models.FileField(upload_to=user_directory_path)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    name = models.CharField(max_length=255, default="Untitled")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# TODO: Давай якщо назву користувач не вказує то береться назва файлу. якщо така вже існує то до назви кріпиться (1), (2) і тд.

class News(models.Model):
    """
    Model to store news articles.

    Attributes:
        source (CharField): The source of the news article. Maximum length of 255 characters.
        title (CharField): The title of the news article. Maximum length of 255 characters.
        content (TextField): The content of the news article.
    """
    source = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    content = models.TextField()
