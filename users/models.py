from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

username_validator = UnicodeUsernameValidator()


class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True, null=True)
    USER = 'user'
    MODERATOR = 'moderator'
    ADMINISTRATOR = 'admin'
    ADMINISTRATOR_DJANGO = 'django_admin'
    ROLE_CHOICES = (
        (USER, 'User'),
        (MODERATOR, 'Moderator'),
        (ADMINISTRATOR, 'Administrator'),
        (ADMINISTRATOR_DJANGO, 'Administrator Django'),
    )
    role = models.CharField(max_length=14,
                            choices=ROLE_CHOICES,
                            default=USER)
    email = models.EmailField(unique=True, blank=True, null=True)
