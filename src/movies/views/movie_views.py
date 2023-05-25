import logging

from django.core.paginator import Paginator
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from ..models import Movie, Genre
from ..serializers.movie_serializers import MovieSerializer
from auth_app.protection.custom_token_authentication import CustomTokenAuthentication

logger = logging.getLogger(__name__)

class MovieListApiView(APIView):
    serializer_class = MovieSerializer
    parser_classes = [JSONParser]
    authentication_classes = [CustomTokenAuthentication]

    def get(self, request, *args, **kwargs):
        movies = Movie.objects.all()
        movies_json = []
        for movie in movies:
            movies_json.append({
                'name': movie.name,
                'date_published': str(movie.date_published),
                'title': movie.title,
                'genre': movie.genre.name,
                'duration': movie.duration
            })
        return JsonResponse({'movies': movies_json}, status=200)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            logger.error(str(e))
            return JsonResponse({'message': str(e)}, status=400)
        name = request.data.get('name')
        date_published = request.data.get('date_published')
        title = request.data.get('title')
        genre = int(request.data.get('genre'))
        duration = int(request.data.get('duration'))
        if not Genre.objects.filter(id=genre).exists():
            return JsonResponse({'message': "Genre doesn't exists in database"}, status=400)
        Movie.objects.create(name=name, date_published=date_published, title=title, genre_id=genre, duration=duration)
        return JsonResponse({}, status=201)



class MovieListWithFiltering(APIView):
    def get(self, request, *args, **kwargs):
        name = request.query_params.get('name') if request.query_params.get('name') else ''
        duration = int(request.query_params.get('duration'))
        sort_by = request.query_params.get('sortBy') if request.query_params.get('sortBy') else ''
        if sort_by not in ['name', 'duration', 'title', 'date_published', 'genre']:
            sort_by = ''
        movies = Movie.objects.filter(name__icontains=name, duration__gt=duration)
        if sort_by:
            movies = movies.order_by(sort_by)
        movies_filtering_list = []
        for movie in movies:
            movies_filtering_list.append(movie.as_json())
        return JsonResponse({'movies': movies_filtering_list}, status=200)


class MoviesWithPagination(APIView):
    def get(self, request, *args, **kwargs):
        current_page_number = int(request.query_params.get('page_number')) if request.query_params.get('page_number') else 1
        number_of_movies = int(request.query_params.get('movie_number')) if request.query_params.get('movie_number') else 10

        movies = Movie.objects.all()

        paginator = Paginator(movies, number_of_movies)
        try:
            page = paginator.get_page(current_page_number)
        except:
            page = paginator.page(1)

        movies_pagination = []
        for movie in page:
            movies_pagination.append(movie.as_json())

        return JsonResponse({
            'movies': movies_pagination,
            'count_total': len(movies),
            'has_previous': page.has_previous(),
            'has_next': page.has_next()
            }, status=200)

class MoviesByGenreAPIView(APIView):
    def get(self, request, *args, **kwargs):
        genre_pk = kwargs.get('pk')
        genre = Genre.objects.filter(pk=genre_pk).prefetch_related("movies").first()
        if not genre:
            return JsonResponse({}, status=404)
        movies = genre.movies.all()
        movies_list_genre = []
        for movie in movies:
            movies_list_genre.append(movie.as_json())
        return JsonResponse({'movies': movies_list_genre}, status=200)


class MovieUpdateDestroyAPIView(APIView):
    serializer_class = MovieSerializer
    parser_classes = [JSONParser]

    def put(self, request, *args, **kwargs):
        movie_id = kwargs.get('movie_id')
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)
        name = request.data.get('name')
        date_published = request.data.get('date_published')
        title = request.data.get('title')
        genre = int(request.data.get('genre'))
        duration = int(request.data.get('duration'))
        movie = Movie.objects.filter(id=movie_id).first()
        if not movie:
            return JsonResponse({}, status=404)
        if not Genre.objects.filter(id=genre).exists():
            return JsonResponse({'message': "Genre doesn't exists in database"}, status=400)
        movie.name = name
        movie.date_published = date_published
        movie.title = title
        movie.genre_id = genre
        movie.duration = duration
        movie.save()
        return JsonResponse({}, status=204)

    def delete(self, request, *args, **kwargs):
        movie_id = kwargs.get('movie_id')
        movie = Movie.objects.filter(id=movie_id).first()
        if not movie:
            return JsonResponse({}, status=404)
        movie.delete()
        return JsonResponse({}, status=204)

