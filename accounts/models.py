from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length = 20)
    password = models.CharField(max_length=20)
    email = models.CharField(max_length = 50, unique = True)
    uuid = models.CharField(max_length = 512)
    username = models.CharField(max_length = 20, unique = True)

class Post(models.Model):
    title = models.CharField(max_length=100)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    image = models.ImageField(null=True, blank=True)
    body = models.TextField(default="default")
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title