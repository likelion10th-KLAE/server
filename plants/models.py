from django.db import models
from accounts.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Plant(models.Model):
    plant_name = models.CharField(max_length=20, unique = True)
    description =  models.TextField()
    image = models.URLField(max_length=200)

class UserPlant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    species = models.CharField(max_length=50)
    image = models.URLField(max_length=200)
    water = models.IntegerField(default=0)
    water_amount = models.IntegerField(default=0)
    repot = models.IntegerField(default=0)
    light = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    temperature = models.CharField(max_length=7)
    start_date = models.DateTimeField(auto_now_add=True)
    last_watered = models.DateTimeField(auto_now_add=True)
    created_at= models.DateTimeField(auto_now_add=True)


