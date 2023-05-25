from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from movies.models import Movie


class Comment(models.Model):
    text = models.TextField(null=False, blank=False)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="comments")
    timestamp = models.DateTimeField(default=timezone.now)
    movie = models.ForeignKey(Movie, null=False, on_delete=models.CASCADE, related_name="comments")


    def json(self):
        formatted_time = self.timestamp.strftime("%d.%m.%Y.")
        return {
            'text': self.text,
            'user': self.user.first_name + ' ' + self.user.last_name if self.user else '',
            'timestamp': formatted_time,
            'movie': self.movie.name if self.movie else ''
        }
