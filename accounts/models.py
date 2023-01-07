from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    password = models.CharField(max_length=512)
    email = models.CharField(max_length=50,unique = True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    select = models.CharField(max_length=50, null=True)
    profile_image = models.ImageField(upload_to='profile', null=True)
    username = models.CharField(max_length=10,unique = True ,null=True)

class Post(models.Model):
    title = models.CharField(max_length=100)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    user_plant = models.IntegerField(null=True)
    user_plant_name = models.CharField(max_length=10, null=True)
    body = models.TextField(default="default")
    give_water = models.TextField(null = True, blank = True)
    change_record = models.TextField(null = True, blank = True )
    growing_tonic = models.CharField(max_length=10, null=True, blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    grow_date_info = models.DateField(null=True)
    like_users = models.ManyToManyField(User, related_name='likepost', null=True)
    share = models.BooleanField(default=False)
    like_num = models.IntegerField(null=True, default=0)
    photo = models.ImageField(upload_to='post', null=True)
    comment_cnt = models.IntegerField(null=True, default=0)
    ndate = models.IntegerField(default=0, null=True, blank=True)
    page_range = models.IntegerField(null=True)

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    post = models.ForeignKey(Post, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    content = models.CharField(null=True, max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile_comment = models.ImageField(null=True)

    def __str__(self):
        return self.content
