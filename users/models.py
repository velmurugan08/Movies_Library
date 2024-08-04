from django.db import models
from uuid import uuid4


class Users(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=250)

    def __str__(self):
        return self.first_name + self.last_name

    def set_password(self, password: str):
        self.password = password
