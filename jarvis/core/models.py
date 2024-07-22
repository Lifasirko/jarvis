import mimetypes

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
    """
    Model to store files uploaded by users.

    Attributes:
        user (ForeignKey): The user who uploaded the file. Links to the CustomUser model.
        file (FileField): The uploaded file.
        category (CharField): The category of the file. Choices are 'image', 'document', 'video', and 'other'.
        name (CharField): The name of the file.
        uploaded_at (DateTimeField): The date and time when the file was uploaded.
    """
    CATEGORY_CHOICES = [
        ('image', 'Image'),
        ('document', 'Document'),
        ('video', 'Video'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    file = models.FileField(upload_to=user_directory_path)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, blank=True)
    name = models.CharField(max_length=255, default="Untitled")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Custom save method to determine the file category based on the file's MIME type
        if the category is not provided by the user.
        """
        if not self.category:
            mime_type, _ = mimetypes.guess_type(self.file.name)

            if mime_type:
                if mime_type.startswith('image'):
                    self.category = 'image'
                elif mime_type.startswith('video'):
                    self.category = 'video'
                elif mime_type in ['application/pdf', 'application/msword',
                                   'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
                    self.category = 'document'
                else:
                    self.category = 'other'
            else:
                self.category = 'other'

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.file.delete(save=False)
        super().delete(*args, **kwargs)


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
