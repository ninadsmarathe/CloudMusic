from django.conf import settings
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save


# Create your models here.


class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username,
            email,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


USERNAME_REGEX = '^[a-zA-Z0-9.+-]*$'


class MyUser(AbstractBaseUser):
    username = models.CharField(
        max_length=255,
        validators=[
            RegexValidator(
                regex=USERNAME_REGEX,
                message='Username must be Alpahnumeric or contain any of the following: ". @ + -" ',
                code='invalid_username'
            )],
        unique=True,
    )
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    zipcode = models.CharField(max_length=120, default="92660")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_full_name(self):
        # The user is identified by their email address
        return self.username

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):  # __unicode__ on Python 2
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True


# # Create your models here.
#
# class Profile(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#
#     city = models.CharField(max_length=250, null=True)
#
#     def __str__(self):
#         return self.user.username
#
#
# def post_save_profile_receiver(sender, instance, created, *args, **kwargs):
#     if created:
#         try:
#             Profile.objects.create(user=instance)
#         except:
#             pass
#
#
# post_save.connect(post_save_profile_receiver, sender=settings.AUTH_USER_MODEL)
