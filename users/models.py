from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator

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
    # username = models.CharField(
    #     _('username'),
    #     blank=True,
    #     null = True,
    #     max_length=150,
    #     unique=True,
    #     help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
    #     validators=[username_validator],
    #     error_messages={
    #         'unique': _("A user with that username already exists."),
    #     },
    # )
