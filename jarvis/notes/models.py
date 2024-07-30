from django.conf import settings
from django.db import models
from django.utils import timezone


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
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=300, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.content
