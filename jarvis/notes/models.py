from django.conf import settings
from django.db import models
from django.utils import timezone


class Tag(models.Model):
    """
    Model to store tags for categorizing notes.

    Attributes:
        name (CharField): The name of the tag. 
            It can have a maximum length of 255 characters. 
            This field is not unique, allowing tags with the same name to be associated with different users.
        owner (ForeignKey): A foreign key to the user who owns the tag. 
            This creates a many-to-one relationship where a user can have multiple tags, 
            but each tag is associated with only one user. 
            If the user is deleted, all their associated tags are also deleted (on_delete=models.CASCADE).
            The `related_name` 'notes_tags' allows reverse querying from the user model to access their tags.
            This field is optional (`null=True`, `blank=True`), meaning a tag can exist without an associated user.

    Methods:
        __str__(): Returns the string representation of the tag, which is its name.
            This is useful for displaying the tag in admin interfaces and other representations of the model.
    """
    name = models.CharField(max_length=255, unique=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notes_tags', null=True, blank=True)


    def __str__(self):
        return self.name


class Note(models.Model):
    """
    Model to store notes for users.

    Attributes:
        owner (ForeignKey): The user to whom this note belongs.
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
        return self.title
