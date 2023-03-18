"""viber URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from accounts.views import loginForm, logoutUser, registrationForm
from album.views import home, about, contact, album_list, album_create, album_detail, album_update, album_delete, \
    song_list, song_create, song_delete, music_play, allusers, full_start
from profiles.views import main_profile, user_profile, profileFollowToggle
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home, name='home'),
    path('introduction/', full_start, name='into'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('users/', allusers, name='user'),

    path('albums/', album_list, name='album-list'),
    path('albums/add/', album_create, name='album-add'),
    path('albums/<slug:slug>/', album_detail, name='album-detail'),
    path('albums/<slug:slug>/edit/', album_update, name='album-update'),
    path('albums/<slug:slug>/delete/', album_delete, name='album-delete'),

    path('registration/', registrationForm, name='register'),
    path('login/', loginForm, name='login'),
    path('logout/', logoutUser, name='logout'),

    path('songs/', song_list, name='song-list'),
    path('albums/<slug:slug>/song-add/', song_create, name='song-add'),
    path('albums/<slug:slug>/song/<int:id>/delete/', song_delete, name='song-delete'),
    path('albums/<slug:slug>/song/<int:id>/play/', music_play, name='play-music'),

    path('u/<slug:slug>/profile/', main_profile, name='profile-user'),
    path('u/<slug:slug>/', user_profile, name='profile'),
    path('profile-follow/', profileFollowToggle, name='follow')

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
