from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), max_length=255, unique=True, error_messages={"unique": _("A user with this email already exists."),},)
    first_name = models.CharField(_("first name"), max_length=255)
    last_name = models.CharField(_("last name"), max_length=255)
    username = models.CharField(_("username"), max_length=255, unique=True, error_messages={"unique": _("A user with this username already exists."),},)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["first_name", "last_name", "email", ]

    objects = CustomUserManager()

    def __str__(self):
        return self.username
