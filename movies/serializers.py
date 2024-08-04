from rest_framework import serializers
from .models import Genre, Movie


class DisplayGenreSerializers(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["id", "name", "is_public"]


class AddGenreSerializers(serializers.Serializer):
    name = serializers.CharField()
    is_public = serializers.BooleanField()


class AddMovietoGenreSerializers(serializers.Serializer):
    genre_id = serializers.UUIDField()
    movie_id = serializers.CharField()


class DisplayMoviesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = "__all__"
