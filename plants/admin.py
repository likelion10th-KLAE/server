from django.contrib import admin
from .models import Plant, UserPlant

admin.site.register(Plant)
admin.site.register(UserPlant)