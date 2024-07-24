from django.shortcuts import render, get_object_or_404, redirect
from core.models import CustomUser, Note, Tag
from .forms import NoteForm
from django.contrib.auth.decorators import login_required


# @login_required
# def find(request, tag_name):
#     notes = list(Note.objects.filter(tags__name=tag_name).all())
#     return render(request, "notes/tags.html", context={"result": tag_name, "notes": notes})



@login_required
def note_list(request):
    notes = Note.objects.filter(user=request.user)
    context = {'notes': notes}
    return render(request, 'notes/note_list.html', context)


# @login_required
def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk)
    return render(request, 'notes/note_detail.html', {'note': note})

@login_required
def note_create(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user  # Призначаємо користувача
            note.save()
            return redirect('note_list')
    else:
        form = NoteForm()
    return render(request, 'notes/note_form.html', {'form': form})

@login_required
def note_edit(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('note_list')
    else:
        form = NoteForm(instance=note)
    return render(request, 'notes/note_form.html', {'form': form})

@login_required
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        note.delete()
        return redirect('note_list')
    return render(request, 'notes/note_confirm_delete.html', {'note': note})
