from rest_framework import serializers
from .models import User, Post, Comment
#회원가입

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'username', 'password', 'email']

#로그인

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required = True)
    password = serializers.CharField(required = True)

#마이페이지 게시물

class GetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title','body', 'image', 'like_users']
        read_only_fields = ['id']


#게시물 게시 및 수정

class PostWritePutSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'like_users']
        read_only_fields = ['id']

# 좋아요

class LikeUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'like_users']

# 댓글 조회
class CommentGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'content','created_at']
        read_only_fields = ['id']

# 댓글 작성
class CommentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content']
        read_only_fields = ['id']

