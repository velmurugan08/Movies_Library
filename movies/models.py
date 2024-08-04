from django.db import models
from uuid import uuid4
from users.models import Users


class Movie(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True)
    imdb_rating = models.FloatField()
    title = models.CharField(max_length=100)
    year = models.CharField(max_length=10)
    imdb_id = models.CharField(max_length=20, unique=True)
    poster_url = models.URLField(default="https://example.com/default_poster.jpg")


class Genre(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True)
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(Users, on_delete=models.CASCADE)
    movies = models.ManyToManyField(Movie, blank=True)
    is_public = models.BooleanField(default=True)
