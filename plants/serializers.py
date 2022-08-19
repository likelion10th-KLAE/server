from rest_framework import serializers
from .models import *

class NoticeSeirializer(serializers.ModelSerializer):
    class Meta:
        model = UserPlant
        fields = ['id', 'plant','water', 'last_watered', 'repot', 'last_repot' ]
        read_only_fields = ['id']


# class RepotNoticeSeirializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserPlant
#         fields = ['id', 'user', 'plant','repot', 'start_date', 'last_repot' ]
#         read_only_fields = ['id']