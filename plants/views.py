from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import RecommendSerializer,PlantGetPostPutSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, authentication_classes, permission_classes

# 등록한 식물 전체 조회
@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def plant_get_all(request):
    plants = UserPlant.objects.all()
    serializer = PlantGetPostPutSerializer(plants, many=True)
    return Response(serializer.data)

# (개발용)식물데이터 전체 조회
@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def plant_db(request):
    plant = Plant.objects.all()
    serializer = RecommendSerializer(plant, many=True)
    return Response(serializer.data)


# 등록 식물 조회
@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def plant_get(request, pk):
    try:
        plantinfo = UserPlant.objects.get(pk=pk)
        serializer = PlantGetPostPutSerializer(plantinfo)
        return Response(serializer.data)
    except UserPlant.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)

# 식물 등록 
@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def plant_post(request):
    serializer = PlantGetPostPutSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user= request.user)
        return Response(serializer.data, status = status.HTTP_201_CREATED)
    return Response(status = status.HTTP_400_BAD_REQUEST)

# 등록 식물 수정
@api_view(['PUT'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def plant_put(request, pk):
    try:
        plantinfo = UserPlant.objects.get(pk=pk)
        if plantinfo.user == request.user:
            serializer = PlantGetPostPutSerializer(plantinfo, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    except UserPlant.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

# 식물 삭제
@api_view(['DELETE'])
@authentication_classes([SessionAuthentication,BasicAuthentication])
@permission_classes([IsAuthenticated])
def delete_userplant(request, plant_id):
    try:
        plant = UserPlant.objects.get(pk = plant_id)
        if plant.user == request.user:
            plant.delete()
            return Response(status = status.HTTP_200_OK)
        return Response(status = status.HTTP_401_UNAUTHORIZED)
    except UserPlant.DoesNotExist:
        return Response(status = status.HTTP_500_INTERNAL_SERVER_ERROR)

#식물추천
@api_view(['GET'])
def recommend(request):
    user = User.objects.get(pk=request.user.id)
    result = map(str, request.data)
    result = "".join(result)
    result_plant = Plant.objects.get(plant_code=result)
    user.select = result_plant.id
    user.save(update_fields=['select'])
    serializer = RecommendSerializer(result_plant)
    return Response(serializer.data)





