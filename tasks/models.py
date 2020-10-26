from django.db import models
from django.conf import settings


class Task(models.Model):
    """Tasks for TodoApp"""
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.CharField(max_length=250)
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.content
