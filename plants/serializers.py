from rest_framework import serializers
from .models import *

# 식물 추천
class RecommendSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPlant
        fields = ['id', 'chocie_plant']
        read_only_fields = ['id']


# 식물 등록 및 수정
class PlantGetPostPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPlant
        fields = ['id', 'name','plant','temperature','light','water_amount','repot'] # 식물 종, 식물이름, 생육온도, 일조량, 1회 급수량, 분갈이 주기
        read_only_fields = ['id']

