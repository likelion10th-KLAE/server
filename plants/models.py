from django.db import models
from accounts.models import User


class Plant(models.Model):
    plant_name = models.CharField(max_length=20, unique = True)
    description =  models.TextField()
    plant_image = models.ImageField(upload_to='plant', null=True)
    plant_code = models.CharField(max_length=4, unique = True, null=True)


class UserPlant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)       # user는 사용자 이름이며, User의 외래키
    plant = models.CharField(max_length=50)                      # plant는 식물의 종이며, Plant의 외래키
    name = models.CharField(max_length=50)                      # name은 식물의 이름을 입력받는 속성
    userplant_image = models.ImageField(upload_to='userplant_image', null=True)
    water = models.IntegerField(default=0, null = True, blank = True )
    water_amount = models.IntegerField(default=0, null = True, blank = True )
    repot = models.IntegerField(default=0, null = True, blank = True )
    light = models.IntegerField(default=0, null = True, blank = True )
    temperature = models.CharField(max_length=7, null = True, blank = True )
    start_date = models.IntegerField(default=0, null = True, blank = True )
    last_watered = models.IntegerField(default=0, null = True, blank = True )
    created_at= models.DateTimeField(auto_now_add=True)
    choice_plant = models.IntegerField(default=0, null = True, blank = True )
    tonic = models.IntegerField(default=0, null = True, blank = True )

