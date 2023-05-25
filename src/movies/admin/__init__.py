from ..models import Movie, Genre, Comment, MovieCommentingBlacklist
from django.contrib import admin

admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(Comment)
admin.site.register(MovieCommentingBlacklist)

