from django.shortcuts import render, redirect
from .models import Note
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def home(request):

    if not request.user.is_authenticated:
        return redirect('/login/')

    if request.method == 'POST':

        title = request.POST.get('title').strip()
        content = request.POST.get('content').strip()
        
        if title and content:
            Note.objects.create(user=request.user, title=title, content=content)
            messages.success (request, "Note added successfully")
        else:
             messages.error(request, "Title and content are required")
        return redirect('/')

    notes = Note.objects.filter(
        user=request.user
    )

    data = {
        'notes': notes
    }

    return render(request, 'notes/home.html', data)

def delete_note(request, note_id):

    if not request.user.is_authenticated:
        return redirect('/login/')

    if request.method == 'POST':

        note = Note.objects.get(
            id=note_id,
            user=request.user
        )

        note.delete()

        return redirect('/')

def edit_note(request, note_id):

    if not request.user.is_authenticated:
        return redirect('/login/')
    
    note = Note.objects.get(
        id=note_id,
        user=request.user
    )

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

def register(request):

    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        username = request.POST.get('username').strip()
        password = request.POST.get('password').strip()
        confirm_password = request.POST.get('confirm_password').strip()

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(
                    request,
                    "Username already exists"
                )
            else:
                User.objects.create_user(username=username, password=password)
                messages.success(
                    request,
                    "Account created successfully"
                )
                return redirect('/login/')
        else:
            messages.error(request, "Passwords do not match")
    return render(request, 'notes/register.html')

def login_user(request):

    if request.user.is_authenticated:
        return redirect('/')

    if request.method == "POST":
        username = request.POST.get('username').strip()
        password = request.POST.get('password').strip()
        user = authenticate (username=username, password=password)

        if user:
            login(request, user)
            return redirect('/')
        else:
            messages.error(
                request,
                "Invalid username or password"
            )
    return render(request, 'notes/login.html')

def logout_user(request):

    logout(request)

    messages.success(
        request,
        "Logged out successfully"
    )

    return redirect('/login/')