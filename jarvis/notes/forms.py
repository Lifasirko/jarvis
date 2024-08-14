from django import forms
from .models import Note, Tag
from core.models import File


class TagForm(forms.ModelForm):
    """
    Form for creating and updating Tag instances.

    This form handles the creation and updating of `Tag` instances. It includes validation logic 
    to ensure that tags with the same name cannot be created for the same owner.

    Fields:
        name (str): The name of the tag.

    Methods:
        clean(): Validates the form data before saving. It checks if a tag with the same name 
                 already exists for the same owner. If such a tag exists, a validation error 
                 is raised to prevent duplicate entries.

    Raises:
        forms.ValidationError: If a tag with the same name already exists for the specified owner.
    """

    class Meta:
        model = Tag
        fields = ['name']

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        owner = cleaned_data.get('owner')

        if Tag.objects.filter(name=name, owner=owner).exists():
            raise forms.ValidationError("Tag with this Name and Owner already exists.")

        return cleaned_data


class NoteForm(forms.ModelForm):
    """
    Form for creating and updating Note instances.

    Fields:
        title (str): The title of the note.
        content (str): The content of the note.
        tags (QuerySet[Tag]): A multiple choice field for selecting existing tags related to the note. 
            It uses a checkbox widget for multiple selections. This field is optional.
        new_tags (str): A text input field for entering new tags, separated by commas. 
            This allows users to create new tags directly while creating or editing a note. 
            This field is optional.
        search_tags (str): A text input field for searching through existing tags. 
            This helps users to easily find and select tags by entering search terms. 
            This field is optional.

    Meta:
        model (Note): The model associated with this form.
        fields (list): Specifies the fields from the Note model that should be included in the form. 
            These are 'title', 'content', 'tags', and 'new_tags'.
        widgets (dict): Customizes the widgets for 'title' and 'content' fields.
            'title' uses a TextInput widget with a placeholder for user guidance.
            'content' uses a Textarea widget with a placeholder for user guidance.

    Methods:
        clean(): Cleans and validates the data provided in the form fields.
            This method can be overridden to add custom validation logic.
            The cleaned data is returned and can be accessed through the form's `cleaned_data` attribute.
    """
    
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

