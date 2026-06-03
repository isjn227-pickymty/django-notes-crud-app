from django.shortcuts import render, redirect, get_object_or_404
from .models import Note
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import NoteSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

def home(request):

    if not request.user.is_authenticated:
        return redirect('/login/')

    if request.method == 'POST':

        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        
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

        note = get_object_or_404(
            Note,
            id=note_id,
            user=request.user
        )

        note.delete()

        return redirect('/')

def edit_note(request, note_id):

    if not request.user.is_authenticated:
        return redirect('/login/')
    
    note = get_object_or_404(
        Note,
        id=note_id,
        user=request.user
    )

    if request.method == 'POST':

        new_title = request.POST.get('title', '').strip()
        new_content = request.POST.get('content', '').strip()
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
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()

        if not username or not password:
            messages.error(
                request,
                "Username and Password are required"
            )
            return render(request, 'notes/register.html')

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
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
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

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def notes_api(request):

    if request.method == 'GET':
        notes = Note.objects.filter(
            user=request.user
        )

        serializer = NoteSerializer(
            notes,
            many=True
        )
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def note_detail_api(
    request,
    note_id
):
    
    note = get_object_or_404(
        Note,
        id=note_id,
        user=request.user
    )

    if request.method == 'GET':
        serializer = NoteSerializer(
            note
        )
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = NoteSerializer(
            note, data=request.data
        )
        if serializer.is_valid():
            # since we already made sure that the current note belongs to 
            # the logged in user, no need of making sure that user=request.user
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)

    if request.method == 'DELETE':
        note.delete()
        return Response(status=204)

@api_view(['POST'])
def register_api(
    request
):
    username = request.data.get('username', '').strip()
    password = request.data.get('password', '').strip()
    confirm_password = request.data.get('confirm_password', '').strip()

    if not username or not password:
        return Response(
            {"error": "Username and password are required"},
            status=400
        )
    
    if User.objects.filter(
    username=username
    ).exists():
        return Response({"error": 'User already exists'}, status=400)
        
    if password != confirm_password:
        return Response({"error": "Passwords do not match"}, status=400)
    
    User.objects.create_user(
        username=username,
        password=password
    )

    return Response(
        {"message": "User created successfully"},
        status=201
    )
    
@api_view(['POST'])
def login_api(
    request
):
    username = request.data.get('username', '').strip()
    password = request.data.get('password', '').strip()

    if not username or not password:
        return Response(
            {"error": "Username and password are required"}, 
            status=400
            )
    user = authenticate(
        username=username,
        password=password
    )

    if user:
        login(
            request,
            user
        )
        return Response(
            {"message": "User logged in successfully"},
            status=200
                )
    else:
        return Response({"error": "Invalid Username or Password"}, status=401)