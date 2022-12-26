from django.urls import path
from .views import *

app_name = 'plants'

urlpatterns = [
    path('info/', plant_get_all),
    path('info/<int:pk>', plant_get),
    path('infopo/', plant_post),
    path('infoput/<int:pk>', plant_put),
    path('recommend/', recommend),
]
