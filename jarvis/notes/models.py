from django.db import models
from django.utils import timezone
from core.models import CustomUser

class Tag(models.Model):

    name = models.CharField(max_length=255, unique=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tags', null=True, blank=True)


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