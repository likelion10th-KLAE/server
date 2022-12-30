from django.urls import path
from .views import *

app_name = 'plants'

urlpatterns = [
    path('info/', plant_get_all),
    path('oneplant/<int:pk>', plant_get),
    path('post/', plant_post),
    path('put/<int:pk>', plant_put),
    path('delete/<int:plant_id',delete_userplant),
    path('recommend/<int:pk>',recommend),
]

