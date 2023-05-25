from django.urls import path

from .views.comment_views import CommentAPIView, CommentByMovieAPIView
from .views.movie_views import MovieListApiView, MovieListWithFiltering, MoviesWithPagination, MoviesByGenreAPIView,MovieUpdateDestroyAPIView



urlpatterns = [

    path('list/', MovieListApiView.as_view(), name='movies_list'),
    path('filtered-list/', MovieListWithFiltering.as_view(), name='movies_filtering'),
    path('page-list/', MoviesWithPagination.as_view(), name='movies_pagination'),
    path('genre/<int:pk>/', MoviesByGenreAPIView.as_view(), name='movies_by_genre'),
    path('<int:movie_id>/', MovieUpdateDestroyAPIView.as_view(), name='movies_update_destroy'),
    path('comment/<int:movie_id>/', CommentByMovieAPIView.as_view(), name='comments_by_movie'),
    path('comment/', CommentAPIView.as_view(), name='comment'),
]
