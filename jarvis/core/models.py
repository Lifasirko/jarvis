import mimetypes

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    storage_limit = models.BigIntegerField(default=50 * 1024 * 1024)  # Ліміт за замовчуванням 50 МБ

    def get_used_storage(self):
        used_storage = sum(file.file.size for file in self.file_set.all())
        return used_storage

    def __str__(self):
        return self.username


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
