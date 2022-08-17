from django.db import models

class User(models.Model):
    name = models.CharField(max_length = 20)
    email = models.CharField(max_length = 50, unique = True)
    uuid = models.CharField(max_length = 512)
    username = models.CharField(max_length = 20)