from django.shortcuts import render, redirect
from .models import Note
from django.contrib import messages

def home(request):

    if request.method == 'POST':

        title = request.POST.get('title').strip()
        content = request.POST.get('content').strip()
        

        if title and content:
            Note.objects.create(title=title, content=content)
            messages.success (request, "Note added successfully")
        else:
             messages.error(request, "Title and content are required")
        return redirect('/')

    notes = Note.objects.all()

    data = {
        'notes': notes
    }

    return render(request, 'notes/home.html', data)

def delete_note(request, note_id):

    if request.method == 'POST':

        note = Note.objects.get(id=note_id)

        note.delete()

        return redirect('/')

def edit_note(request, note_id):

        note = Note.objects.get(id=note_id)

        if request.method == 'POST':

            new_title = request.POST.get('title').strip()
            new_content = request.POST.get('content').strip()
            if new_title and new_content:
                note.title = new_title
                note.content = new_content
                note.save()
                messages.success (request, "Note modified successfully")
                return redirect('/')
            else:
                messages.error(request, "Title and content are required")

        data = {
            'note': note
        }

        return render(request, 'notes/edit.html', data)