from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token


# Create your models here.
class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    fullname = models.CharField(_('full name'), max_length=150, unique=False)
    phone = models.CharField(_('phone'), max_length=12)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    is_parent = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.email


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Parent(models.Model):
    user = models.OneToOneField(
        User, related_name='parent', on_delete=models.CASCADE)
    """ email = models.EmailField(
        max_length=254, unique=True, null=False, blank=False)
    fullname = models.CharField(max_length=150, null=False, blank=False)
    phone = models.CharField(max_length=12, null=False, blank=False)
 """


class Admin(models.Model):
    user = models.OneToOneField(
        User, related_name='admin', on_delete=models.CASCADE)
    """ email = models.EmailField(
        max_length=254, unique=True, null=False, blank=False)
    fullname = models.CharField(max_length=150, null=False, blank=False)
    phone = models.CharField(max_length=12, null=False, blank=False)
 """
