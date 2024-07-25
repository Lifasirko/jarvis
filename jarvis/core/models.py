import mimetypes

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    storage_limit = models.BigIntegerField(default=50 * 1024 * 1024)  # Ліміт за замовчуванням 50 МБ

    def get_used_storage(self):
        used_storage = sum(file.file.size for file in self.file_set.all())
        return used_storage

    def __str__(self):
        return self.username


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


# <<<<<<< note_app_two
# =======

class Tag(models.Model):
    """
    Model to store tags for categorizing notes.

    Attributes:
        name (CharField): The name of the tag. Maximum length of 255 characters.
    """
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Note(models.Model):
    """
    Model to store notes for users.

    Attributes:
        user (ForeignKey): The user to whom this note belongs. Links to the CustomUser model.
        title (CharField): The title of the note. Maximum length of 300 characters.
        content (TextField): The content of the note.
        created_at (DateTimeField): The date and time when the note was created.
        updated_at (DateTimeField): The date and time when the note was last updated.
        tags (ManyToManyField): Tags associated with the note. Links to the Tag model.
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=300, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.content



def user_directory_path(instance, filename):
    # Файли будуть завантажуватися в MEDIA_ROOT/user_<id>/<filename>
    return f'user_{instance.user.id}/{filename}'


# >>>>>>> tasks
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
