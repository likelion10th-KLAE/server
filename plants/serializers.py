from rest_framework import serializers
from .models import *

# 식물 추천
class RecommendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = ['id', 'plant_image', 'plant_name', 'description', 'difficulty', 'plant_function', 'hydroponics']
        read_only_fields = ['id']


# 식물 등록 및 수정
class PlantGetPostPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPlant
        fields = ['id', 'plant', 'name','userplant_image', 'temperature', 'light', 'water_amount', 'last_watered', 'tonic','repot', 'start_date', 'extra1', 'extra2'] # 식물 종, 식물이름, 생육온도, 일조량, 1회 급수량, 분갈이 주기
        read_only_fields = ['id']
#사이드바
class UserPlantsSidebar(serializers.ModelSerializer):
    class Meta:
        model = UserPlant
        fields = ['id', 'name']
        read_only_fields = ['id']

class GetUserPick(serializers.ModelSerializer):
    class Meta:
        model = UserPick
        fields = ['id', 'result']
        read_only_fields = ['id']