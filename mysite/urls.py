from django.contrib import admin
from django.urls import path
from notes.views import home, delete_note, edit_note, register, login_user, logout_user, notes_api, note_detail_api, register_api, login_api
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
# def hello(request):
#     return HttpResponse("Hello Ishita")


urlpatterns = [path('admin/', admin.site.urls), 
                path('', home), 
                path('delete/<int:note_id>/', delete_note), 
                path('edit/<int:note_id>/', edit_note), 
                path('register/', register),
                path('login/', login_user ),
                path('logout/', logout_user),
                path('api/notes/', notes_api),
                path('api/notes/<int:note_id>/', note_detail_api),
                path('api/register/', register_api),
                path('api/login/', login_api),
                path('api/token/', TokenObtainPairView.as_view()),
                path('api/token/refresh/', TokenRefreshView.as_view())
                ]
