from django.contrib import admin
from django.urls import path, include
from .views import login, main, spotify_login, home


urlpatterns = [
    path('', main),
    path('login', login),
    path('spotify-login', spotify_login),
    path('home', home)
    # path('add-song/<sid>', add_song)
]
