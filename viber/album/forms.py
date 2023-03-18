from django import forms
from .models import AlbumCreate,SongCreate


class AlbumCreateForm(forms.ModelForm):
    class Meta:
        model = AlbumCreate
        fields = ['artist', 'album_title', 'genre','album_logo']


class SongCreateForm(forms.ModelForm):

    class Meta:
        model = SongCreate
        fields = ['song_title','audio_file','is_favorite']