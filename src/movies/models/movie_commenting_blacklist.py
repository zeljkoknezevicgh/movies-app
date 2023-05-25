from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class MovieCommentingBlacklist(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
