from django.db import models
from django.contrib.auth.models import AbstractUser

COLOR_CHOICES = (
    ("pink", "Pink"),
    ("blue", "Blue"),
    ("green", "Green"),
    ("aquamarine", "Aquamarine"),
    ("coral", "Coral"),
    ("brown", "Brown"),
)


class TodoUser(AbstractUser):
    color = models.CharField(
        max_length=10,
        choices=COLOR_CHOICES,
        default='aquamarine'
    )
