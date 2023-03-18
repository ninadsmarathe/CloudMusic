import os
import random
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save, post_save
from django.db.models import Q
from .utils import unique_slug_generator
from profiles.models import Profile

# Create your models here.

User = get_user_model()


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    # print(instance)
    # print(filename)
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "album/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )


class AlbumSongQuerySet(models.query.QuerySet):
    def search_song(self,
                    query):  # RestaurantLocation.objects.all().search(query) #RestaurantLocation.objects.filter(something).search()
        if query:
            query = query.strip()
            return self.filter(

                Q(album__user__username__icontains=query)|
                Q(album__artist__icontains=query) |
                Q(album__artist__exact=query) |
                Q(album__album_title__icontains=query) |
                Q(album__album_title__iexact=query) |
                Q(album__genre__icontains=query) |
                Q(album__genre__iexact=query) |
                Q(song_title__icontains=query) |
                Q(song_title__iexact=query)).distinct()
        return self

    def search_album(self,
                     query):  # RestaurantLocation.objects.all().search(query) #RestaurantLocation.objects.filter(something).search()
        if query:
            query = query.strip()
            return self.filter(
                Q(user__username__icontains=query) |
                Q(user__username__icontains=query) |
                Q(artist__icontains=query) |
                Q(artist__exact=query) |
                Q(album_title__icontains=query) |
                Q(album_title__iexact=query) |
                Q(genre__icontains=query) |
                Q(genre__iexact=query) |
                Q(songcreate__song_title__icontains=query) |
                Q(songcreate__song_title__iexact=query)).distinct()
        return self


class AlbumCreateManager(models.Manager):
    def get_queryset(self):
        return AlbumSongQuerySet(self.model, using=self._db)

    def search_song(self, query):  # RestaurantLocation.objects.search()
        return self.get_queryset().search_song(query)

    def search_album(self, query):  # RestaurantLocation.objects.search()
        return self.get_queryset().search_album(query)


class AlbumCreate(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    artist = models.CharField(max_length=250)
    album_title = models.CharField(max_length=500)
    genre = models.CharField(max_length=100)
    album_logo = models.ImageField(upload_to=upload_image_path,default="/media/xyz.jpg")
    is_favorite = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(blank=True, null=True)

    objects = AlbumCreateManager()

    def __str__(self):
        return self.album_title + ' - ' + self.artist + ' - ' + str(self.user)


class SongCreate(models.Model):
    album = models.ForeignKey(AlbumCreate, on_delete=models.CASCADE)
    song_title = models.CharField(max_length=250)
    audio_file = models.FileField(upload_to=upload_image_path,default='')
    is_favorite = models.BooleanField(default=False)

    objects = AlbumCreateManager()

    def __str__(self):
        return self.song_title + ' - ' + self.album.album_title + ' - ' + str(self.album.user)


def rl_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(rl_pre_save_receiver, sender=AlbumCreate)
