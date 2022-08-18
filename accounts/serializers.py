from rest_framework import serializers
from .models import User

#회원가입

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

#로그인

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required = True)
    password = serializers.CharField(required = True)



