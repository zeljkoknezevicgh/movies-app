from django.db import models
from .genre import Genre


class Movie(models.Model):
    name = models.CharField(max_length=100)
    duration = models.IntegerField(null=False)
    date_published = models.DateField()
    title = models.CharField(max_length=100)
    genre = models.ForeignKey(Genre, null=True, on_delete=models.CASCADE, related_name="movies")
    release_date = models.DateField(null=True)

    def __str__(self):
        return self.name

    def as_json(self):
        return {
            'name': self.name,
            'date_published': str(self.date_published),
            'title': self.title,
            'genre': self.genre.name,
            'duration': self.duration
        }
