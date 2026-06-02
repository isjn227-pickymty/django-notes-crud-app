from django.contrib import admin
from django.urls import path
from notes.views import home, delete_note, edit_note

def hello(request):
    return HttpResponse("Hello Ishita")


urlpatterns = [path('admin/', admin.site.urls), path('', home), path('delete/<int:note_id>/', delete_note), path('edit/<int:note_id>/', edit_note)]