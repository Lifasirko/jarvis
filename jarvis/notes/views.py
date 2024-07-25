from django.shortcuts import render, get_object_or_404, redirect
from .models import Note, Tag
from core.models import CustomUser
from .forms import NoteForm, TagForm
from django.contrib.auth.decorators import login_required


@login_required
def note_list(request):
    """
    Renders the note list page with the ability to filter notes by title and tags.
    This view requires the user to be logged in.

    Args:
        request (HttpRequest): The request object used to generate this response.
    Returns:
        HttpResponse: The rendered note list page with the notes.
    """
    query = request.GET.get('q', '')
    tag = request.GET.get('tag', '')
    notes = Note.objects.filter(user=request.user)

    if query:
        notes = notes.filter(title__icontains=query)
    if tag:
        notes = notes.filter(tags__name__icontains=tag)

    context = {
        'notes': notes,
        'query': query,
        'selected_tag': tag,
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
    """
    Renders the note creation form and handles the creation of a new note.
    This view requires the user to be logged in.

    Args:
        request (HttpRequest): The request object used to generate this response.

    Returns:
        HttpResponse: Redirects to the note list page after successful creation.
        HttpResponse: The rendered note creation form page if the form is invalid.
    """
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            tags = form.cleaned_data['tags']
            note.tags.set(tags)
            return redirect('notes:note_list')
    else:
        form = NoteForm()
    return render(request, 'notes/note_form.html', {'form': form})


@login_required
def tag_create(request):
    """
    Renders the tag creation form and handles the creation of a new tag.
    This view requires the user to be logged in.

    Args:
        request (HttpRequest): The request object used to generate this response.

    Returns:
        HttpResponse: Redirects to the note list page after successful creation.
        HttpResponse: The rendered tag creation form page if the form is invalid.
    """
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('notes:note_list')
    else:
        form = TagForm()
    return render(request, 'notes/tag_form.html', {'form': form})


@login_required
def note_edit(request, pk):
    """
    Renders the note edit form and handles the update of an existing note.
    This view requires the user to be logged in.

    Args:
        request (HttpRequest): The request object used to generate this response.
        pk (int): The primary key of the note to be edited.

    Returns:
        HttpResponse: Redirects to the note list page after successful update.
        HttpResponse: The rendered note edit form page if the form is invalid.
    """
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('notes:note_list')
    else:
        form = NoteForm(instance=note)
    return render(request, 'notes/note_form.html', {'form': form})


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
