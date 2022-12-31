from rest_framework import serializers
from .models import *

# 식물 추천
class RecommendSerializer(serializers.ModelSerializer):
    plant_image = serializers.ImageField(use_url=True)
    class Meta:
        model = Plant
        fields = ['id', 'plant_image', 'plant_name', 'description']
        read_only_fields = ['id']


# 식물 등록 및 수정
class PlantGetPostPutSerializer(serializers.ModelSerializer):
    userplant_image = serializers.ImageField(use_url=True)
    class Meta:
        model = UserPlant
        fields = ['id', 'name','plant','userplant_image','temperature','light','water_amount','repot', 'start_date', 'tonic', 'last_watered'] # 식물 종, 식물이름, 생육온도, 일조량, 1회 급수량, 분갈이 주기
        read_only_fields = ['id']

