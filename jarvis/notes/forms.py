from django import forms
from .models import  Note, Tag


class TagForm(forms.ModelForm):
    """
    Form for creating and updating Tag instances.

    Fields:
        name (str): The name of the tag.
    """
    class Meta:
        model = Tag
        fields = ['name']

class NoteForm(forms.ModelForm):
    """
    Form for creating and updating Note instances.

    Fields:
        title (str): The title of the note.
        content (str): The content of the note.
        tags (QuerySet): A multiple choice field for selecting related tags.
    """
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Note
        fields = ['title', 'content', 'tags']


