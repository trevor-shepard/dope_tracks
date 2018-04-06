from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    last_track_pull = models.DateTimeField(default=timezone.now)
    