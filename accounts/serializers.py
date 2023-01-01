from rest_framework import serializers
from .models import User, Post, Comment
#회원가입

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'username', 'password', 'email']


#마이페이지
class MypageSerializers(serializers.ModelSerializer):
    profile_image = serializers.ImageField(use_url=True)
    class Meta:
        model = User
        fields = ['name', 'username', 'password', 'email', 'profile_image']
        read_only_fields = ['username']

#로그인

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required = True)
    password = serializers.CharField(required = True)

#일지 게시물

class GetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'change_record', 'growing_tonic', 'like_num', 'share', 'photo']
        read_only_fields = ['id']


#일지 게시 및 수정
class PostWritePutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title','body', 'change_record', 'growing_tonic', 'like_num', 'share', 'photo']
        read_only_fields = ['id']

# 좋아요

class LikeUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'like_num']

# 댓글 조회
class CommentGetSerializer(serializers.ModelSerializer):
    profile_image = serializers.ImageField(use_url=True)
    class Meta:
        model = Comment, User
        fields = ['id', 'post', 'user', 'content','created_at', 'profile_image']
        read_only_fields = ['id']

# 댓글 작성
class CommentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment, User
        fields = ['id', 'content', 'profile_image']
        read_only_fields = ['id']

class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title','body', 'photo', 'like_num', 'share']
        read_only_fields = ['id']