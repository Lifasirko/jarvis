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
        title (str): The title of the note, entered through a text input field.
        content (str): The content of the note, entered through a textarea.
        tags (QuerySet): A multiple choice field for selecting related tags,
                         displayed as checkboxes.
        search_tags (str): A text input field for searching tags.
    """
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Tags',  # Optional: Label for the field
        help_text='Select tags for this note'  # Optional: Help text
    )

    search_tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Search tags...'})
    )

    class Meta:
        model = Note
        fields = ['title', 'content', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter the title here'}),
            'content': forms.Textarea(attrs={'placeholder': 'Enter the content here'}),
        }


