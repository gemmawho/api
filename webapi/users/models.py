from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.TextChoices):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class User(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(max_length=200, blank=True)
    confirmation_code = models.CharField(max_length=60, blank=True)
    description = models.TextField(max_length=200, blank=True)
    role = models.CharField(max_length=25,
                            choices=Role.choices,
                            default=Role.USER)

    class Meta:
        ordering = ('username',)

    @property
    def is_admin(self):
        return self.role == Role.ADMIN or self.is_staff

    @property
    def is_moderator(self):
        return self.role == Role.MODERATOR
