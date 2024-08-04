from django.urls import path
from . import views

urlpatterns = [
    path("", views.movies, name="movies"),
    path("find/", views.get_movies_by_query, name="movies_by_query"),
    path("fetch_genre/", views.get_genere_by_user_id, name="get a users genre"),
    path("movie/<str:movie_id>/", views.get_movie_by_id, name="get_movie_by_od"),
    path(
        "get_movie_by_api/<str:movie_id>/",
        views.get_current_movie_api,
        name="movie_by_api",
    ),
    path("add_genre", views.add_genre, name="add genre to the user"),
    path("add_movie_to_genre", views.add_movie_to_genre, name="add_movie_to_genre"),
    path("genre/<uuid:genre_id>/", views.movies_by_genre, name="movies_by_genre"),
]
# get_current_movie_api
