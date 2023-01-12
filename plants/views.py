from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from datetime import datetime
from rest_framework_simplejwt.tokens import AccessToken

def get_token_user(request):
    access_token = AccessToken(request.META.get('HTTP_AUTHORIZATION'))
    user = User.objects.get(pk=access_token['user_id'])
    return user

# 등록한 식물 전체 조회
@api_view(['GET'])
#@authentication_classes([SessionAuthentication, BasicAuthentication])
#@permission_classes([IsAuthenticated])
def plant_get_all(request):
    plants = UserPlant.objects.all()
    serializer = PlantGetPostPutSerializer(plants, many=True)
    return Response(serializer.data)

# (개발용)식물데이터 전체 조회
@api_view(['GET'])
#@authentication_classes([SessionAuthentication, BasicAuthentication])
#@permission_classes([IsAuthenticated])
def plant_db(request):
    plant = Plant.objects.all()
    serializer = RecommendSerializer(plant, many=True)
    return Response(serializer.data)


# 등록 식물 조회
@api_view(['GET'])
#@authentication_classes([SessionAuthentication, BasicAuthentication])
#@permission_classes([IsAuthenticated])
def plant_get(request, pk):
    try:
        plantinfo = UserPlant.objects.get(pk=pk)
        serializer = PlantGetPostPutSerializer(plantinfo)
        return Response(serializer.data)
    except UserPlant.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)

# 식물 등록 
@api_view(['POST'])
#@authentication_classes([SessionAuthentication, BasicAuthentication])
#@permission_classes([IsAuthenticated])
def plant_post(request):
    user = get_token_user(request)
    serializer = PlantGetPostPutSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=user)
        return Response(serializer.data, status = status.HTTP_201_CREATED)
    return Response(status = status.HTTP_400_BAD_REQUEST)

# 등록 식물 수정
@api_view(['PUT'])
#@authentication_classes([SessionAuthentication, BasicAuthentication])
#@permission_classes([IsAuthenticated])
def plant_put(request, pk):
    try:
        user = get_token_user(request)
        plantinfo = UserPlant.objects.get(pk=pk)
        if plantinfo.user == user:
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
#@authentication_classes([SessionAuthentication,BasicAuthentication])
#@permission_classes([IsAuthenticated])
def delete_userplant(request, plant_id):
    try:
        user = get_token_user(request)
        plant = UserPlant.objects.get(pk = plant_id)
        if plant.user == user:
            plant.delete()
            return Response(status = status.HTTP_200_OK)
        return Response(status = status.HTTP_401_UNAUTHORIZED)
    except UserPlant.DoesNotExist:
        return Response(status = status.HTTP_500_INTERNAL_SERVER_ERROR)
# 식물 등록 
@api_view(['POST'])
#@authentication_classes([SessionAuthentication, BasicAuthentication])
#@permission_classes([IsAuthenticated])
def recommend(request):
    result_serializer = GetUserPick(data=request.data)
    if result_serializer.is_valid():
        result = result_serializer.data['result']
        result_plant = Plant.objects.get(plant_code=result)
        serializer = RecommendSerializer(result_plant)
        return Response(serializer.data)
    return Response(status=status.HTTP_400_BAD_REQUEST)


#마이페이지 사이드바 - 유저에 맞는(생성한) 식물 리스트
@api_view(['GET'])
#@authentication_classes([SessionAuthentication,BasicAuthentication])
#@permission_classes([IsAuthenticated])
def get_user_plants(request):
    user = get_token_user(request)
    plants = UserPlant.objects.filter(user=user.id).order_by('-created_at')
    serializer = UserPlantsSidebar(plants, many=True)
    return Response(serializer.data)





