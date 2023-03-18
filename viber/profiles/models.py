from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model

User = get_user_model()


class ProfileManager(models.Manager):

    def toggle_follow(self, request_user, username_to_toggle):
        profile_ = Profile.objects.get(user__username__iexact=username_to_toggle)
        user = request_user
        is_following = False
        if user in profile_.followers.all():
            profile_.followers.remove(user)
            user.profile.following.remove(profile_.user)
        else:
            user.profile.following.add(profile_.user)
            profile_.followers.add(user)
            is_following = True
        return profile_, is_following


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # user.profile
    # followers = models.ManyToManyField(User, related_name='is_following', blank=True)
    followers = models.ManyToManyField(User, related_name='followers', blank=True)  # user.is_following.all()
    following = models.ManyToManyField(User, related_name='following', blank=True)  # user.following.all()
    activated = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    objects = ProfileManager()


def post_save_user_receiver(sender, instance, created, *args, **kwargs):
    if created:
        profile, is_created = Profile.objects.get_or_create(user=instance)
        # default_user_profile = Profile.objects.get_or_create(user__id=1)[0]  # user__username=
        # default_user_profile.followers.add(instance)
        # profile.followers.add(default_user_profile.user)
        # profile.followers.add(2)


post_save.connect(post_save_user_receiver, sender=User)
