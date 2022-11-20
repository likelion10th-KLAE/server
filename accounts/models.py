from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length = 20)
    password = models.CharField(max_length=512)
    email = models.CharField(max_length = 50, unique = True)
    uuid = models.CharField(max_length = 512)
    username = models.CharField(max_length = 20, unique=True)

class Post(models.Model):
    title = models.CharField(max_length=100)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    image = models.ImageField(null=True, blank=True)
    body = models.TextField(default="default")
    growing_record = models.TextField(null = True, blank = True )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    grow_date_info = models.DateField(null=True)
    like_users= models.ManyToManyField(User, related_name='like_articles')

    def __str__(self):
        return self.title

class Comment(models.Model):
    article = models.ForeignKey(Post, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    content = models.CharField(null=True, max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content