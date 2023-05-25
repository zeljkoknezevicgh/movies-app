from rest_framework import serializers
from ..models import Movie, Genre

class MovieSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, allow_null=False, allow_blank=False)
    date_published = serializers.DateField(format='%Y-%m-%d')
    duration = serializers.IntegerField(allow_null=False)
    title = serializers.CharField(max_length=100)
    genre = serializers.IntegerField(allow_null=False)