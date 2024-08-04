from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse, HttpRequest
import requests
from movie_library.settings import OMDBAPIKEY
from movie_library.utils import auth_required
from .models import Genre, Users, Movie
from .serializers import (
    DisplayGenreSerializers,
    AddGenreSerializers,
    AddMovietoGenreSerializers,
    DisplayMoviesSerializers,
)


# To get the movies page with search bar
def movies(request):
    return render(request, "movies/movies.html")


# To get the movies by the name
@auth_required
def get_movies_by_query(request: HttpRequest):
    query = request.GET.get("query")
    movies_resp = requests.get(
        f"http://www.omdbapi.com/?s=${query}&apikey={OMDBAPIKEY}"
    )
    return JsonResponse(data=movies_resp.json())


# To get the particular movie details
def get_movie_by_id(request: HttpRequest, movie_id: str):
    return render(request, "movies/curr_movie.html", {"movie_id": movie_id})


@auth_required
def get_current_movie_api(request: HttpRequest, movie_id: str):
    movie_resp = requests.get(
        f"http://www.omdbapi.com/?i={movie_id}&apikey={OMDBAPIKEY}"
    )
    json_data = movie_resp.json()
    if json_data["Response"] == "True":
        return JsonResponse(json_data)
    else:
        return render(request, "movies/404.html")


@auth_required
def get_genere_by_user_id(request):
    genre = Genre.objects.filter(created_by=request.jwt_payload["sub"]).all()
    serilizer = DisplayGenreSerializers(genre, many=True)
    return JsonResponse({"genre": serilizer.data})


from rest_framework.decorators import api_view


@api_view(["POST"])
@auth_required
def add_genre(request: HttpRequest):
    genre_details = AddGenreSerializers(data=request.data)
    user_id = request.jwt_payload["sub"]
    if genre_details.is_valid():
        genre, status = Genre.objects.get_or_create(
            name=genre_details.validated_data.get("name"),
            created_by=Users.objects.filter(id=user_id).first(),
            is_public=genre_details.validated_data.get("is_public", True),
        )
        if status == False:
            return JsonResponse({"message": "Genre Already existed"}, status=400)
        return JsonResponse(
            {"message": "Genre created", "genre": DisplayGenreSerializers(genre).data},
            status=201,
        )
    return JsonResponse({"message": genre_details.errors}, status=400)


@api_view(["POST"])
@auth_required
def add_movie_to_genre(request: HttpRequest):
    adding_movie_details = AddMovietoGenreSerializers(data=request.data)
    user_id = request.jwt_payload["sub"]
    if adding_movie_details.is_valid():
        genre_id = adding_movie_details.validated_data.get("genre_id")
        movie_id = adding_movie_details.validated_data.get("movie_id")

        # Fetch the genre
        curr_genre = (
            Genre.objects.filter(id=genre_id)
            .filter(created_by=Users.objects.filter(id=user_id).first())
            .first()
        )
        if curr_genre is None:
            return JsonResponse({"message": "Genre Not found"}, status=404)

        # Fetch the movie
        movie_exist_status = Movie.objects.filter(imdb_id=movie_id).first()
        if not movie_exist_status:
            movie_detail = requests.get(
                f"http://www.omdbapi.com/?i={movie_id}&apikey={OMDBAPIKEY}"
            )
            json_data = movie_detail.json()
            if json_data["Response"] != "True":
                return JsonResponse({"message": "Movie with id not found"}, status=404)

            new_movie = Movie.objects.create(
                imdb_rating=json_data["imdbRating"],
                title=json_data["Title"],
                year=json_data["Year"],
                imdb_id=movie_id,
                poster_url=json_data["Poster"],
            )
        else:
            new_movie = movie_exist_status

        # Add the new movie to the genre
        curr_genre.movies.add(new_movie)

        return JsonResponse(
            {"message": "Movie added to genre successfully"}, status=200
        )

    return JsonResponse({"message": "Invalid data"}, status=400)


# geting the movies of Genre
@api_view(["GET"])
# @auth_required
def movies_by_genre(request, genre_id):
    genre = Genre.objects.filter(id=genre_id).first()
    movies = genre.movies.all()
    serializers = DisplayMoviesSerializers(movies, many=True)
    return render(
        request, "movies/curr_genre.html", {"movies": serializers.data, "genre": genre}
    )
