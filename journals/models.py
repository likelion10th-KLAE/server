from django.db import models
from plants.models import UserPlant

class Diary(models.Model):
    user_plant_id = models.ForeignKey(UserPlant, on_delete=models.CASCADE)
    title = models.CharField(max_length = 50)
    body = models.TextField()
    image = models.URLField(max_length=200)
    growing_record = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    grow_date_info = models.DateTimeField(auto_now_add=True)
