from django.db import models
from accounts.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Plant(models.Model):
    plant_name = models.CharField(max_length=20, unique = True)
    description =  models.TextField()
    image = models.URLField(max_length=200)

class UserPlant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)       # user는 사용자 이름이며, User의 외래키
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)     # plant는 식물명이며, Plant의 외래키
    species = models.CharField(max_length=50)                      # species는 식물의 종을 입력받는 속성
    image = models.URLField(max_length=200, null = True, blank = True )
    water = models.IntegerField(default=0, null = True, blank = True )
    water_amount = models.IntegerField(default=0, null = True, blank = True )
    repot = models.IntegerField(default=0, null = True, blank = True )
    light = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null = True, blank = True )
    temperature = models.CharField(max_length=7, null = True, blank = True )
    start_date = models.DateField()
    last_watered = models.DateField()
    created_at= models.DateTimeField(auto_now_add=True)


