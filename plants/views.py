from time import timezone
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import NoticeSeirializer
from datetime import datetime, timedelta





@api_view(['GET'])
def water_repot_notice(request):
    try:
        objects = UserPlant.objects.filter(user = request.user)
        waternotice = []
        for plant in objects:
            if plant.last_watered.day + plant.water == timezone.now().day:
                plant.last_watered = timezone.now().day
                plant.save()
                waternotice.append(plant)
        print("1")
        serializer = NoticeSeirializer(waternotice, many = True)
        print("0000")
        if serializer.is_valid():
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(status = status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response(status = status.HTTP_500_INTERNAL_SERVER_ERROR)

   
