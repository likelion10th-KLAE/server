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

class Post(models.Model):
    title = models.CharField(max_length=100)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    image = models.CharField(max_length=512, null=True, blank=True)
    body = models.TextField(default="default")
    growing_record = models.TextField(null = True, blank = True )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    grow_date_info = models.DateField()

    class Meta:
        managed = False
        db_table = 'journal'


    def __str__(self):
        return self.title