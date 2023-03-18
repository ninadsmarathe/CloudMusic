from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import AlbumCreate, SongCreate
from .forms import AlbumCreateForm, SongCreateForm
from django.db.models import Q
from django.contrib.auth import get_user_model
from profiles.models import Profile
ABC = get_user_model()


# Create your views here.
def full_start(request):
    return render(request, "startbootstrap-creative-gh-pages/index.html", {})


@login_required()
def home(request):
    user = request.user
    # query = request.GET.get('q')
    # if query is not None:
    #     user = AlbumCreate.objects.search_album(query)
    user_exist=user.profile.following.all()

    context = {"user": user,
               "is_existing":user_exist}

    return render(request, "home.html", context)
    # return render(request, "startbootstrap-creative-gh-pages/index.html", {})


def about(request):
    return render(request, "about.html", {"name": request.user})


def contact(request):
    return render(request, "contact.html", {"name": request.user})


@login_required()
def allusers(request):
    abc = ABC.objects.all()
    count_following = len(request.user.profile.following.all())
    count_follower = len(request.user.profile.followers.all())
    context = {
        "user_model": abc,
        "user": request.user,
        "count_following":count_following,
        "count_follower":count_follower,
        "count_all":len(abc)-1

    }
    return render(request, "users.html", context)


@login_required()
def album_list(request):
    user = request.user
    qs = AlbumCreate.objects.all()
    # qs = user.albumcreate_set.all()
    query = request.GET.get('q')
    # albums = AlbumCreate.objects.filter(user=request.user)
    # for i in albums:
    #     if not i.songcreate_set.exists():
    #         i.delete()
    #         break
    if query is not None:
        qs = AlbumCreate.objects.search_album(query)
    context = {
        "object_list": qs
    }
    return render(request, "album/list-view.html", context)


@login_required()
def album_create(request):
    form = AlbumCreateForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.album_logo = form.cleaned_data['album_logo']
        instance.save()
        return redirect("/albums/{num}/".format(num=instance.slug))

    context = {
        "form": form,
    }

    return render(request, "album/create-form.html", context)


@login_required()
def album_detail(request, slug):
    qs = AlbumCreate.objects.get(slug=slug)
    query = qs.songcreate_set.all()
    abc = request.GET.get('q')
    if abc is not None:
        query = SongCreate.objects.filter(album__user=request.user).search_song(abc)
    context = {
        "object": qs,
        "object_list": query
    }
    return render(request, "album/detail-view.html", context)


@login_required()
def album_update(request, slug):
    qs = get_object_or_404(AlbumCreate, slug=slug)
    form = AlbumCreateForm(request.POST or None, request.FILES or None, instance=qs)
    context = {
        "form": form,
    }

    if form.is_valid():
        obj = form.save(commit=False)
        context["obj"] = obj
        obj.User = request.user
        obj.album_logo = form.cleaned_data['album_logo']
        obj.save()
        return redirect("/albums/{num}/".format(num=obj.slug))

    return render(request, "album/update-form.html", context)


@login_required()
def album_delete(request, slug):
    qs = get_object_or_404(AlbumCreate, slug=slug)
    qs.delete()
    return HttpResponseRedirect('/albums/')


@login_required()
def song_list(request):
    qs = SongCreate.objects.all()
    query = request.GET.get('q')
    if query is not None:
        qs = SongCreate.objects.search_song(query)
    context = {
        "object_list": qs
    }
    return render(request, "song/list-view.html", context)


@login_required()
def song_create(request, slug):
    data = ""
    qs = get_object_or_404(AlbumCreate, slug=slug)
    form = SongCreateForm(request.POST or None, request.FILES or None)
    list_ = []

    if qs.user != request.user:

        # if qs.album_title not in list_:
        if qs not in request.user.albumcreate_set.all():

            qs1 = AlbumCreate.objects.create(user=request.user, album_title=qs.album_title, album_logo=qs.album_logo,
                                             artist=qs.artist, genre=qs.genre)

            if form.is_valid():
                instance = form.save(commit=False)
                instance.album = qs1
                instance.audio_file = form.cleaned_data['audio_file']
                instance.save()

                albums = AlbumCreate.objects.filter(user=request.user)
                for i in albums:
                    if not i.songcreate_set.exists():
                        i.delete()
                        break
                return redirect("/albums/{num}/".format(num=qs1.slug))

        elif qs.album_title in list_:
            print("Add this song in ur account")
            data = "Add this song in ur account"
        # album = get_object_or_404(AlbumCreate, slug=request.user.albumcreate_set.get(album_title=qs.album_title))
        # if form.is_valid():
        #     instance = form.save(commit=False)
        #     instance.album = album
        #     instance.audio_file = form.cleaned_data['audio_file']
        #     instance.save()
        #
        #     return redirect("/albums/{num}/".format(num=album.slug))


    else:
        # form = SongCreateForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.album = qs
            instance.audio_file = form.cleaned_data['audio_file']
            instance.save()

            return redirect("/albums/{num}/".format(num=qs.slug))

    context = {
        "data": data,
        "form": form
    }

    return render(request, "song/create-form.html", context)


@login_required()
def song_delete(request, slug, id):
    album = get_object_or_404(AlbumCreate, slug=slug)
    qs = get_object_or_404(SongCreate, id=id)
    qs.delete()
    return HttpResponseRedirect("/albums/{num}/".format(num=slug))


def music_play(request, slug, id):
    album = get_object_or_404(AlbumCreate, slug=slug)
    qs = get_object_or_404(SongCreate, id=id)
    context = {
        "object": qs
    }
    return render(request, "song/music-play.html", context)

# @login_required()
# def song_create(request, slug):
#     qs = get_object_or_404(AlbumCreate, slug=slug)
#     form = SongCreateForm(request.POST or None, request.FILES or None)
#     list_ = []
#     for i in request.user.albumcreate_set.all():
#         list_.append(i.album_title)
#     if qs.user != request.user:
#
#         if qs.album_title not in list_:
#             qs1 = AlbumCreate.objects.create(user=request.user, album_title=qs.album_title, album_logo=qs.album_logo,
#                                              artist=qs.artist, genre=qs.genre)
#
#             if form.is_valid():
#                 instance = form.save(commit=False)
#                 instance.album = qs1
#                 instance.audio_file = form.cleaned_data['audio_file']
#                 instance.save()
#
#                 albums = AlbumCreate.objects.filter(user=request.user)
#                 for i in albums:
#                     if not i.songcreate_set.exists():
#                         i.delete()
#                         break
#                 return redirect("/albums/{num}/".format(num=qs1.slug))
#
#         elif qs.album_title in list_:
#             print("going")
#             album = get_object_or_404(AlbumCreate, slug=request.user.albumcreate_set.get(album_title=qs.album_title))
#             if form.is_valid():
#                 instance = form.save(commit=False)
#                 instance.album = album
#                 instance.audio_file = form.cleaned_data['audio_file']
#                 instance.save()
#
#                 return redirect("/albums/{num}/".format(num=album.slug))
#
#
#     else:
#         # form = SongCreateForm(request.POST or None, request.FILES or None)
#         if form.is_valid():
#             instance = form.save(commit=False)
#             instance.album = qs
#             instance.audio_file = form.cleaned_data['audio_file']
#             instance.save()
#
#             return redirect("/albums/{num}/".format(num=qs.slug))
#
#     context = {
#         "form": form
#     }
#
#     return render(request, "song/create-form.html", context)
