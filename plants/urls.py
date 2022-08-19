from django.urls import path
from .views import *

app_name = 'plants'

urlpatterns = [
    path('notice/', water_repot_notice),

]