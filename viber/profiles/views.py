from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from album.models import AlbumCreate, SongCreate
from .models import Profile

from django.contrib.auth.decorators import login_required

# Create your views here.

User = get_user_model()


@login_required()
def main_profile(request, slug):
    q = User.objects.get(username=slug)
    query = request.GET.get('q')
    items_exists = SongCreate.objects.filter(album__user=request.user).exists()
    qs = AlbumCreate.objects.filter(user=request.user).search_album(query)

    context = {
        "user": q,
        "query": query,
        "items_exists": items_exists,
        "qs": qs
    }
    if items_exists and qs.exists():
        context['locations'] = qs
    return render(request, "profiles/main.html", context)
    #return render(request, "startbootstrap-resume-gh-pages/index.html", context)


def profileFollowToggle(request):
    username_to_toggle = request.POST.get("username")
    profile_, is_following = Profile.objects.toggle_follow(request.user, username_to_toggle)
    return redirect("/u/{num}/".format(num=profile_.user.username))

@login_required()
def user_profile(request, slug):
    q = User.objects.get(username=slug)
    count_following = len(q.profile.following.all())
    count_follower = len(q.profile.followers.all())
    query = request.GET.get('q')
    items_exists = SongCreate.objects.filter(album__user=q).exists()
    qs = AlbumCreate.objects.filter(user=q).search_album(query)

    context = {
        "user": q,
        "query": query,
        "items_exists": items_exists,
        "qs": qs,
        "count_following": count_following,
        "count_follower": count_follower
    }
    if items_exists and qs.exists():
        context['locations'] = qs
    is_following = False
    print(request.user)
    print(q.profile)
    print(type(request.user.profile.following.first()))
    if q in request.user.profile.following.all():
        print("going")
        is_following = True
    context['is_following'] = is_following
    return render(request, "profiles/user.html", context)
