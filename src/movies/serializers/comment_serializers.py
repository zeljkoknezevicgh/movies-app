from rest_framework import serializers


class CommentSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=100, allow_null=False, allow_blank=False)
    movie_id = serializers.IntegerField(allow_null=True)
