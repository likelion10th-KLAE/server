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


# 식물 추천
@api_view(['POST'])
def recommend(request):
    try:
        choices = UserPlant.objects.filter(data = request.data)
        result = []
        for choice in choices:
            if choice.choice_plant[0] == 1:
                if choice.choice_plant[1] == 1:
                    if choice.choice_plant[2] == 1:
                        if choice.choice_plant[3] == 1:
                            result.append('A')
                        elif choice.choice_plant[3] == 2:
                            result.append('B')
                        elif choice.choice_plant[3] == 3:
                            result.append('C')
                        else:
                            result.append('D')
                    else:
                        if choice.choice_plant[3] == 1:
                            result.append('F')
                        elif choice.choice_plant[3] == 2:
                            result.append('G')
                        elif choice.choice_plant[3] == 3:
                            result.append('H')
                        else:
                            result.append('I')
                elif choice.choice_plant[1] == 2:
                    if choice.choice_plant[2] == 1:
                        if choice.choice_plant[3] == 1:
                            result.append('J')
                        elif choice.choice_plant[3] == 2:
                            result.append('K')
                        elif choice.choice_plant[3] == 3:
                            result.append('L')
                        else:
                            result.append('M')
                    else :
                        if choice.choice_plant[3] == 1:
                            result.append('N')
                        elif choice.choice_plant[3] == 2:
                            result.append('O')
                        elif choice.choice_plant[3] == 3:
                            result.append('P')
                        else:
                            result.append('Q')
                elif choice.choice_plant[1] == 3:
                    if choice.choice_plant[2] == 1:
                        if choice.choice_plant[3] == 1:
                            result.append('R')
                        elif choice.choice_plant[3] == 2:
                            result.append('S')
                        elif choice.choice_plant[3] == 3:
                            result.append('T')
                        else:
                            result.append('U')
                    else :
                        if choice.choice_plant[3] == 1:
                            result.append('V')
                        elif choice.choice_plant[3] == 2:
                            result.append('W')
                        elif choice.choice_plant[3] == 3:
                            result.append('X')
                        else:
                            result.append('Y')
                elif choice.choice_plant[1] == 4:
                    if choice.choice_plant[2] == 1:
                        if choice.choice_plant[3] == 1:
                            result.append('Z')
                        elif choice.choice_plant[3] == 2:
                            result.append('a')
                        elif choice.choice_plant[3] == 3:
                            result.append('b')
                        else:
                            result.append('c')
                    else :
                        if choice.choice_plant[3] == 1:
                            result.append('d')
                        elif choice.choice_plant[3] == 2:
                            result.append('e')
                        elif choice.choice_plant[3] == 3:
                            result.append('f')
                        else:
                            result.append('g')
            else:
                if choice.choice_plant[1] == 1:
                    if choice.choice_plant[2] == 1:
                        if choice.choice_plant[3] == 1:
                            result.append('h')
                        elif choice.choice_plant[3] == 2:
                            result.append('i')
                        elif choice.choice_plant[3] == 3:
                            result.append('j')
                        else:
                            result.append('k')
                    else:
                        if choice.choice_plant[3] == 1:
                            result.append('l')
                        elif choice.choice_plant[3] == 2:
                            result.append('m')
                        elif choice.choice_plant[3] == 3:
                            result.append('n')
                        else:
                            result.append('o')
                elif choice.choice_plant[1] == 2:
                    if choice.choice_plant[2] == 1:
                        if choice.choice_plant[3] == 1:
                            result.append('p')
                        elif choice.choice_plant[3] == 2:
                            result.append('q')
                        elif choice.choice_plant[3] == 3:
                            result.append('r')
                        else:
                            result.append('s')
                    else :
                        if choice.choice_plant[3] == 1:
                            result.append('t')
                        elif choice.choice_plant[3] == 2:
                            result.append('u')
                        elif choice.choice_plant[3] == 3:
                            result.append('v')
                        else:
                            result.append('w')
                elif choice.choice_plant[1] == 3:
                    if choice.choice_plant[2] == 1:
                        if choice.choice_plant[3] == 1:
                            result.append('x')
                        elif choice.choice_plant[3] == 2:
                            result.append('y')
                        elif choice.choice_plant[3] == 3:
                            result.append('z')
                        else:
                            result.append('01')
                    else :
                        if choice.choice_plant[3] == 1:
                            result.append('02')
                        elif choice.choice_plant[3] == 2:
                            result.append('03')
                        elif choice.choice_plant[3] == 3:
                            result.append('04')
                        else:
                            result.append('05')
                elif choice.choice_plant[1] == 4:
                    if choice.choice_plant[2] == 1:
                        if choice.choice_plant[3] == 1:
                            result.append('06')
                        elif choice.choice_plant[3] == 2:
                            result.append('07')
                        elif choice.choice_plant[3] == 3:
                            result.append('08')
                        else:
                            result.append('09')
                    else :
                        if choice.choice_plant[3] == 1:
                            result.append('10')
                        elif choice.choice_plant[3] == 2:
                            result.append('11')
                        elif choice.choice_plant[3] == 3:
                            result.append('12')
                        else:
                            result.append('13')
    except Exception as e:
        print(e)
        return Response(status = status.HTTP_500_INTERNAL_SERVER_ERROR)




