from datetime import timedelta

from django.http import JsonResponse
from django.utils import timezone
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from auth_app.protection.custom_token_authentication import CustomTokenAuthentication
from movies.models import Comment, Movie, MovieCommentingBlacklist
from movies.serializers.comment_serializers import CommentSerializer
from constance import config


class CommentAPIView(APIView):

    serializer_class = CommentSerializer
    parser_classes = [JSONParser]
    authentication_classes = [CustomTokenAuthentication]

    def check_inappropriate_words(self, text):
        inappropriate_words = ['rec1', 'rec2', 'rec3']
        words = text.lower().split()

        for word in words:
            if word in inappropriate_words:
                return True
        return False

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)
        text = request.data.get('text')
        movie_id = request.data.get('movie_id')
        user_id = request.user.id

        blacklist = MovieCommentingBlacklist.objects.filter(user=request.user).order_by('-timestamp').first()
        if blacklist and blacklist.timestamp + timedelta(days=1) > timezone.now() :
            return JsonResponse({'message': 'Your are not allowed to comment because you have entered a comments that contains inappropriate words'}, status=400)

        if self.check_inappropriate_words(text):
            MovieCommentingBlacklist.objects.create(user=request.user)
            return JsonResponse({'message': 'Your comment contains inappropriate words'}, status=400)

        try:
            movie = Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            return JsonResponse({'message': 'Movie does not exist in database'}, status=404)

        if movie.release_date and movie.release_date > timezone.now().date():
            return JsonResponse({'message': 'Movie has not been released yet'}, status=400)

        today_comments = Comment.objects.filter(timestamp__gte=timezone.now() - timedelta(days=1),
                                                user=request.user)

        if len(today_comments) >= config.MAX_COMMENTS_PER_DAY:
            return JsonResponse({
                'message': 'You have already commented max number of times today'
            }, status=409)

        Comment.objects.create(text=text, movie_id=movie_id, user_id=user_id)
        return JsonResponse({}, status=201)


class CommentByMovieAPIView(APIView):
    authentication_classes = [CustomTokenAuthentication]

    def get(self, request, *args, **kwargs):
        movie_id = kwargs.get('movie_id')

        try:
            movie = Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            return JsonResponse({'message': 'Movie does not exist in database'}, status=404)

        comments = Comment.objects.filter(movie_id=movie_id).select_related('user').order_by('-timestamp')
        comments_as_json = [comment.json() for comment in comments]
        return JsonResponse({
            'comments': comments_as_json
        }, status=200)
