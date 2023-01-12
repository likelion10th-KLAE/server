from .models import User, Post, Comment
from plants.models import UserPlant
from rest_framework import status, generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from .serializers import *
from django.contrib import auth
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from datetime import datetime
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
#from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.
'''
로그인, 로그아웃, 회원가입, 마이페이지 관련 함수
'''

"""
토큰회원가입
"""

def get_token_user(request):
    access_token = AccessToken(request.META.get('HTTP_AUTHORIZATION'))
    user = User.objects.get(pk=access_token['user_id'])
    return user


class signup(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            signup_user = serializer.save(password = make_password(serializer.validated_data['password']))
            token = TokenObtainPairSerializer.get_token(signup_user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user" : serializer.data['username'],
                    "message" : "회원가입 완료!",
                    "token" : {
                        "access" : access_token,
                        "refresh" : refresh_token,
                    }
                },
                status = status.HTTP_200_OK
            )
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            auth.login(request, signup_user)
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""
토큰 로그인
"""
class login(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(email=serializer.data["email"])
            # if not check_password(request.data['password'], user.password):
            #     return Response({"msg" : "비밀번호가 틀렸습니다"}, status=status.HTTP_400_BAD_REQUEST)
        if user is not None:
            auth.login(request, user)
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            username = str(user.username)
            if user.profile_image:
                profile = str(user.profile_image.url)
                res = Response(
                    {
                        "user" : serializer.data['email'],
                        "user_id": str(user.pk),
                        "username": username,
                        "message" : "로그인 성공!",
                        "profile": profile,
                        "token" : {
                            "access" : access_token,
                            "refresh" : refresh_token,
                        },
                    },
                    status=status.HTTP_200_OK
                )
                return res
            else:
                res = Response(
                    {
                        "user" : serializer.data['email'],
                        "username": username,
                        "user_id": str(user.pk),
                        "message" : "로그인 성공!",
                        "profile": "null",
                        "token" : {
                            "access" : access_token,
                            "refresh" : refresh_token,
                        },
                    },
                    status=status.HTTP_200_OK
                )
                return res

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


#마이페이지 조회
@api_view(['GET'])
#@authentication_classes([SessionAuthentication, BasicAuthentication])
#@permission_classes([IsAuthenticated])
def mypage(request):
    try:
        user = get_token_user(request)
        serializer = MypageSerializers(user)
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)

#마이페이지 수정
@api_view(['PUT'])
#@authentication_classes([SessionAuthentication, BasicAuthentication])
#@permission_classes([IsAuthenticated])
def mypage_put(request):
    try:
        user = get_token_user(request)
        serializer = MypagePutserializers(user, data=request.data)
        if serializer.is_valid():
            serializer.save(password = make_password(serializer.validated_data['password']))
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

#로그아웃
@api_view(['POST'])
def logout(request):
    auth.logout(request)
    return Response(status=status.HTTP_200_OK)
'''
페이지네이션 관련 함수
'''
#공유게시판 16개
@api_view(['GET'])
#@authentication_classes([SessionAuthentication,BasicAuthentication])
#@permission_classes([IsAuthenticated])
def get_page_posts(request, page):
    posts = Post.objects.filter(share=True).order_by('-created_at')
    paginator = Paginator(posts, 16)
    page_obj = paginator.get_page(page)
    for post in posts:
        post.page_range = paginator.num_pages
        post.save(update_fields=['page_range'])

    serializer = PageSerializer(page_obj, many=True)
    return Response(serializer.data)

#일지공유게시판 최신 4개
@api_view(['GET'])
#@authentication_classes([SessionAuthentication,BasicAuthentication])
#@permission_classes([IsAuthenticated])
def new_4_posts(request):
    posts = Post.objects.filter(share=True).order_by('-created_at')
    paginator = Paginator(posts, 4)
    page_obj = paginator.get_page(1)
    serializer = PageSerializer(page_obj, many=True)
    return Response(serializer.data)

#일지공유게시판 공감 4개
@api_view(['GET'])
#@authentication_classes([SessionAuthentication,BasicAuthentication])
#@permission_classes([IsAuthenticated])
def likes_4_posts(request):
    posts = Post.objects.filter(share=True).order_by('-like_num')
    paginator = Paginator(posts, 4)
    page_obj = paginator.get_page(1)
    serializer = PageSerializer(page_obj, many=True)
    return Response(serializer.data)

'''
일지 관련 함수
'''

#전체 게시물 조회
@api_view(['GET'])
#@authentication_classes([SessionAuthentication,BasicAuthentication])
#@permission_classes([IsAuthenticated])
def get_all_posts(request):
    posts = Post.objects.all()
    serializer = GetSerializer(posts, many=True)
    return Response(serializer.data)

#한 게시물 조회
@api_view(['GET'])
#@authentication_classes([SessionAuthentication, BasicAuthentication])
#@permission_classes([IsAuthenticated])
def get_one_post(request, pk):
    try:
        user = get_token_user(request)
        post = Post.objects.get(pk=pk)
        comments = Comment.objects.filter(post__id = pk)

        userplant = UserPlant.objects.get(pk=post.user_plant)
        post.user_plant_name = userplant.name
        post.comment_cnt = comments.count()
        
        date = userplant.created_at.replace(tzinfo=None)
        now = datetime.now().replace(tzinfo=None)
        post.ndate = (now - date).days + 1

        post.save(update_fields=['comment_cnt', 'ndate', 'user_plant_name'])

        if post.like_users.filter(pk=user.id).exists():
            bool_like_users = True
        else:
            bool_like_users = False
        serializer = GetSerializer(post)
        res = Response(
                {
                    "bool_like_users": bool_like_users,
                    "id" : serializer.data['id'],
                    "title" : serializer.data['title'],
                    "give_water" : serializer.data['give_water'],
                    "change_record" : serializer.data['change_record'],
                    "growing_tonic" : serializer.data['growing_tonic'],
                    "like_num" : serializer.data['like_num'],
                    "share" : serializer.data['share'],
                    "photo" : serializer.data['photo'],
                    "comment_cnt" : serializer.data['comment_cnt'],
                    "ndate" : serializer.data['ndate'],
                    "user_plant_name" : serializer.data['user_plant_name'],
                    "body" : serializer.data['body']
                },
                status = status.HTTP_200_OK
            )
        return res
    except Post.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)

#게시물 업로드
@api_view(['POST'])
#@authentication_classes([SessionAuthentication, BasicAuthentication])
#@permission_classes([IsAuthenticated])
def post_one_post(request, user_plant_id):
    user = get_token_user(request)
    serializer = PostWritePutSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(writer = user, user_plant=user_plant_id) #1 = request.data, 향후 user_plant_id로 저장할지, request.data로 할지 논의 필요
        return Response(status = status.HTTP_201_CREATED)
    return Response(status = status.HTTP_400_BAD_REQUEST)

#게시물 수정
@api_view(['PUT'])
#@authentication_classes([SessionAuthentication, BasicAuthentication])
#@permission_classes([IsAuthenticated])
def put_one_post(request, pk):
    try:
        user = get_token_user(request)
        post = Post.objects.get(pk=pk)
        if post.writer == user:
            serializer = PostWritePutSerializer(post, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

#공유하기 버튼 눌렀을 때
@api_view(['GET'])
#@authentication_classes([SessionAuthentication, BasicAuthentication])
#@permission_classes([IsAuthenticated])
def share(request, pk):
    try:
        post = Post.objects.get(pk=pk) 
        if post.share == False:
            post.share = True
            post.save(update_fields=['share'])
            serializer = GetSerializer(post)
            return Response(serializer.data)
        else:
            post.share = False
            post.save(update_fields=['share'])
            serializer = GetSerializer(post)
            return Response(serializer.data)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


#게시물 삭제
@api_view(['DELETE'])
#@authentication_classes([SessionAuthentication, BasicAuthentication])
#@permission_classes([IsAuthenticated])
def delete_one_post(request, pk):
    try:
        user = get_token_user(request)
        post = Post.objects.get(pk=pk)
        if post.writer == user:
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

# 좋아요
@api_view(['GET'])
#@authentication_classes([SessionAuthentication, BasicAuthentication])
#@permission_classes([IsAuthenticated])
def likes(request, pk):
    try:
        user = get_token_user(request)
        post = Post.objects.get(pk=pk)
        if post.like_users.filter(pk=user.id).exists():
            post.like_users.remove(user)
            post.like_num = post.like_users.count()
            post.save(update_fields=['like_num'])
            serializer = LikeUsersSerializer(post)
            res = Response(
                {
                    "like_num" : serializer.data['like_num'],
                    "bool_like_users" : False
                },
                status = status.HTTP_200_OK
            )
            return res
        else:
            post.like_users.add(user)
            post.like_num = post.like_users.count()
            post.save(update_fields=['like_num'])
            serializer = LikeUsersSerializer(post)
            res = Response(
                {
                    "like_num" : serializer.data['like_num'],
                    "bool_like_users" : True
                },
                status = status.HTTP_200_OK
            )
            return res
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

#식물별 작성된 일지 모아주기
@api_view(['GET'])
#@authentication_classes([SessionAuthentication,BasicAuthentication])
#@permission_classes([IsAuthenticated])
def get_userplant_post(request, user_plant_id):
    posts = Post.objects.filter(user_plant=user_plant_id).order_by('-created_at')
    userplant = UserPlant.objects.get(pk=user_plant_id)
    date = userplant.created_at.replace(tzinfo=None)
    now = datetime.now().replace(tzinfo=None)
    posts.ndate = (now - date).days + 1
    serializer = PageSerializer(posts, many=True)
    return Response(serializer.data)

'''
댓글 관련 함수
'''

# 댓글 조회
@api_view(['GET'])
def get_comments(request, post_id):
    try:
        comments = Comment.objects.filter(post__id = post_id)
        for comment in comments:
            comment.profile_comment = comment.user.profile_image
        serializer = CommentGetSerializer(comments, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    except Post.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)

# 댓글 업로드
@api_view(['POST'])
#@authentication_classes([SessionAuthentication,BasicAuthentication])
#@permission_classes([IsAuthenticated])
def post_comment(request, post_id):
    try:
        user = get_token_user(request)
        serializer = CommentPostSerializer(data=request.data)
        if serializer.is_valid():
            if user.is_authenticated :
                serializer.save(user=user, post_id = post_id, username_comment=user.username)
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            return Response(status = status.HTTP_401_UNAUTHORIZED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(status = status.HTTP_500_INTERNAL_SERVER_ERROR)

# 댓글 삭제
@api_view(['DELETE'])
#@authentication_classes([SessionAuthentication,BasicAuthentication])
#@permission_classes([IsAuthenticated])
def delete_comment(request, comment_id):
    try:
        user = get_token_user(request)
        comment = Comment.objects.get(pk = comment_id)
        if comment.user == user:
            comment.delete()
            return Response(status = status.HTTP_200_OK)
        return Response(status = status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response(status = status.HTTP_500_INTERNAL_SERVER_ERROR)

#댓글 수만 보내주기
@api_view(['GET'])
#@authentication_classes([SessionAuthentication, BasicAuthentication])
#@permission_classes([IsAuthenticated])
def get_comment_cnt(request, pk):
    try:
        post = Post.objects.get(pk=pk)
        post.comment_cnt += 1
        post.save(update_fields=['comment_cnt'])
        serializer = CommentCntSerializer(post)
        return Response(serializer.data)
    except Post.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)

