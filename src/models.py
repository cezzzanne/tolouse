from django.db import models
import spotipy
import spotipy.util as util
from django.contrib.auth.models import User

CLIENT_ID = "ef0c4f54854c4820821a2bf2b3db6f2a"
SECRET_ID = "313915bc83844bdfaa647f8f4129dcf8"
REDIRECT_URI = "http://127.0.0.1:8000/login"


# Create your models here.
class Party(models.Model):
    name = models.CharField(max_length=200)
    unique_id = models.CharField(max_length=200)
    playlist_id = models.TextField(null=True)
    user_id = models.CharField(max_length=200, null=True)
    access_token = models.TextField(null=True)
    refresh_token = models.TextField(null=True)
    token_info = models.TextField(null=True)


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='member')
    party = models.ForeignKey(Party, on_delete=models.CASCADE, related_name='member', null=True)
    email = models.EmailField(null=True)