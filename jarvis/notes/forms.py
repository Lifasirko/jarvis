from django import forms
from .models import Note, Tag


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
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Tags',
        help_text='Select tags for this note'
    )

    new_tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Enter new tags, comma-separated'}),
        label='New Tags'
    )

    search_tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Search tags...'}),
        label='Search Tags'
    )

    class Meta:
        model = Note
        fields = ['title', 'content', 'tags', 'new_tags']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter the title here'}),
            'content': forms.Textarea(attrs={'placeholder': 'Enter the content here'}),
        }
