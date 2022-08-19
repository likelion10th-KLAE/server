'''
from django.db import models
from plants.models import UserPlant

class Diary(models.Model):
    user_plant = models.ForeignKey(UserPlant, on_delete=models.CASCADE, null = True, blank = True )
    title = models.CharField(max_length = 50, null = True, blank = True )
    body = models.TextField(null = True, blank = True )
    image = models.URLField(max_length=200, null = True, blank = True )
    growing_record = models.TextField(null = True, blank = True )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    grow_date_info = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'journal'
'''