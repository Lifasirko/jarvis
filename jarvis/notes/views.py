from django.shortcuts import render, get_object_or_404, redirect
from .models import Note, Tag
from core.models import CustomUser
from .forms import NoteForm, TagForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q




@login_required
def note_list(request):
    """
    Renders a list of notes, optionally filtered by a search query.
    This view requires the user to be logged in.

    Args:
        request (HttpRequest): The request object used to generate this response.

    Returns:
        HttpResponse: The rendered note list page, with optional search results.
    
    The function checks for a 'search' parameter in the GET request. If a search query is provided,
    it filters the notes by title or tags, displaying only the notes that match the search criteria.
    If no search query is provided, it displays all notes.

    Context:
        notes (QuerySet): The queryset of notes to be displayed, either filtered by the search query
                          or all notes if no search query is provided.
    """
    search_query = request.GET.get('search', '')
    if search_query:
        notes = Note.objects.filter(
            Q(title__icontains=search_query) | Q(tags__name__icontains=search_query)
        ).distinct()
    else:
        notes = Note.objects.all()
    context = {
        'notes': notes
    }
    return render(request, 'notes/note_list.html', context)


# @login_required
def note_detail(request, pk):
    """
    Renders the detail page for a single note.
    This view requires the user to be logged in.

    Args:
        request (HttpRequest): The request object used to generate this response.
        pk (int): The primary key of the note to be displayed.

    Returns:
        HttpResponse: The rendered note detail page.
    """
    note = get_object_or_404(Note, pk=pk)
    return render(request, 'notes/note_detail.html', {'note': note})


@login_required
def note_create(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            form.save_m2m()

            # Handle new tags
            new_tags = form.cleaned_data.get('new_tags')
            if new_tags:
                tag_names = [name.strip() for name in new_tags.split(',')]
                new_tags_objects = [Tag.objects.get_or_create(name=name)[0] for name in tag_names]
                note.tags.add(*new_tags_objects)

            return redirect('notes:note_list')
    else:
        form = NoteForm()

    search_query = request.GET.get('search', '')
    tags = Tag.objects.filter(name__icontains=search_query)

    return render(request, 'notes/note_form.html', {
        'form': form,
        'note': None,
        'tags': tags,
        'search_query': search_query,
        'selected_tags': []
    })

@login_required
def note_edit(request, pk):
    note = get_object_or_404(Note, pk=pk)

    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()

            # Handle new tags
            new_tags = form.cleaned_data.get('new_tags')
            if new_tags:
                tag_names = [name.strip() for name in new_tags.split(',')]
                new_tags_objects = [Tag.objects.get_or_create(name=name)[0] for name in tag_names]
                note.tags.add(*new_tags_objects)

            return redirect('notes:note_list')
    else:
        form = NoteForm(instance=note)

    search_query = request.GET.get('search', '')
    tags = Tag.objects.filter(name__icontains=search_query)
    note_tags = note.tags.values_list('id', flat=True)

    return render(request, 'notes/note_form.html', {
        'form': form,
        'note': note,
        'tags': tags,
        'search_query': search_query,
        'selected_tags': note_tags
    })




@login_required
def tag_manage(request, delete_tag_id=None):
    """
    Manages tags, including creation, deletion, and searching.
    This view requires the user to be logged in.

    Args:
        request (HttpRequest): The request object used to generate this response.
        delete_tag_id (int, optional): The ID of the tag to be deleted.

    Returns:
        HttpResponse: The rendered tag management page or confirmation page for deletion.

    On POST request with delete_tag_id:
        - Deletes the specified tag and redirects to the tag management page.

    On POST request without delete_tag_id:
        - Creates a new tag with the submitted form data and redirects to the tag management page.

    On GET request with delete_tag_id:
        - Renders a confirmation page for deleting the specified tag.

    On GET request without delete_tag_id:
        - Renders the tag management page with a search functionality.

    Context:
        form (TagForm): The form for creating or updating tags.
        tags (QuerySet): Tags filtered by the search query.
        search_query (str): The search query for filtering tags.
        tag (Tag, optional): The tag to be deleted (for confirmation page).
    """
    if request.method == 'POST':
        if delete_tag_id:
            tag = get_object_or_404(Tag, pk=delete_tag_id)
            tag.delete()
            return redirect('notes:tag_manage')
        else:
            form = TagForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('notes:tag_manage')
    else:
        form = TagForm()
        
        if delete_tag_id:
            tag = get_object_or_404(Tag, pk=delete_tag_id)
            return render(request, 'notes/tag_confirm_delete.html', {'tag': tag})

        search_query = request.GET.get('search', '')
        tags = Tag.objects.filter(name__icontains=search_query)

    return render(request, 'notes/tag_manage.html', {'form': form, 'tags': tags, 'search_query': search_query})


@login_required
def note_delete(request, pk):
    """
    Renders the note deletion confirmation page and handles the deletion of a note.
    This view requires the user to be logged in.

    Args:
        request (HttpRequest): The request object used to generate this response.
        pk (int): The primary key of the note to be deleted.

    Returns:
        HttpResponse: Redirects to the note list page after successful deletion.
        HttpResponse: The rendered note deletion confirmation page.
    """
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        note.delete()
        return redirect('notes:note_list')
    return render(request, 'notes/note_confirm_delete.html', {'note': note})