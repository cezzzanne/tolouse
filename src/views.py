from django.shortcuts import render
from urllib.parse import urlencode
import requests
import spotipy
import spotipy.util as util
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from .models import Member, Party
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

CLIENT_ID = "ef0c4f54854c4820821a2bf2b3db6f2a"
SECRET_ID = "313915bc83844bdfaa647f8f4129dcf8"
REDIRECT_URI = "http://127.0.0.1:8000/login"


def main(request):
    if request.method == 'POST':
        username = request.POST['username']
        u = User.objects.create(username=username)
        email = request.POST['email']
        password = request.POST['password']
        u.set_password(password)
        u.save()
        party_id = request.POST['party-id']
        if Party.objects.filter(unique_id=party_id).exists():
            return
            # TODO: Return Error
        name = request.POST['party-name']
        party = Party(name=name, unique_id=party_id)
        party.save()
        new_member = Member(user=u, email=email, party=party)
        new_member.save()
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        return HttpResponseRedirect('spotify-login')

        # TODO: Render error
    return render(request, 'main.html')


@login_required()
def spotify_login(request):
    scope = "playlist-modify-public"
    cred = spotipy.util.oauth2.SpotifyOAuth(CLIENT_ID, SECRET_ID, REDIRECT_URI, scope=scope)
    return render(request, 'home.html', {'url': cred.get_authorize_url()})


@login_required()
def login(request):
    scope = "playlist-modify-public"
    code = request.GET['code']
    cred = spotipy.util.oauth2.SpotifyOAuth(CLIENT_ID, SECRET_ID, REDIRECT_URI, scope)
    full_code = cred.get_access_token(code)
    request.user.party.access_token = full_code['access_token']
    request.user.party.refresh_token = full_code['refresh_token']
    request.user.party.token_info = full_code['token_info']
    sp = spotipy.Spotify(auth=full_code['access_token'])
    request.user.party.user_id = sp.current_user()['id']
    sp.user_playlist_create(user=sp.current_user()['id'], name=request.user.party.name)
    request.user.party.playlist_id = sp.current_user_playlists()['items'][0]['id']
    return HttpResponseRedirect("/home/")


@login_required()
def home(request):
    party = request.user.party
    sp = spotipy.Spotify(auth=request.user.party.access_token)
    current_songs = sp.user_playlist_tracks(party.user_id, party.playlist_id)
    formatted_songs = get_format(current_songs['tracks']['items'])
    return render(request, 'home.html', {'songs', formatted_songs})


def login2(request):
    scope = "playlist-modify-public"
    code = request.GET['code']
    cred = spotipy.util.oauth2.SpotifyOAuth(CLIENT_ID, SECRET_ID, REDIRECT_URI, scope)
    full_code = cred.get_access_token(code)
    sp = spotipy.Spotify(auth=full_code['access_token'])
    user_id = sp.current_user()['id']
    tracks = sp.search(q="christmas ", limit=2, type='track')
    formatted = get_format(tracks['tracks']['items'])
    # Playlist ID that can after be kept in model
    play_id = sp.current_user_playlists()['items'][0]['id']
    # Keep user id in the playlist object as well
    trk = []
    trk.append(formatted[1]['add'])
    # sp.user_playlist_add_tracks(user='parellano1997', playlist_id=play_id, tracks=trk)
    return render(request, 'login.html', {'songs': full_code})


def get_format(tracks):
    songs = []
    for track in tracks:
        song = {}
        song['Name'] = track['name']
        song['Artist'] = track['artists'][0]['name']
        song['Album'] = track['album']['name']
        song['Duration (mins)'] = track['duration_ms'] / 100000
        song['Popularity'] = track['popularity']
        song['add'] = track['uri']
        songs.append(song)
    return songs
