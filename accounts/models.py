from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length = 20)
    password = models.CharField(max_length=512)
    email = models.CharField(max_length = 50, unique = True)
    uuid = models.CharField(max_length = 512)
    username = models.CharField(max_length = 20, unique=True)

    class Meta:
        managed = False
        db_table = 'accounts'