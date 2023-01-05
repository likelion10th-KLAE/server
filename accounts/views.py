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
#from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.
'''
로그인, 로그아웃, 회원가입, 마이페이지 관련 함수
'''

@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = auth.authenticate(
            request=request,
            email=serializer.data['email'],
            password=serializer.data['password']
        )
        if user is not None:
            auth.login(request, user)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_400_BAD_REQUEST)

#회원가입
@api_view(['POST'])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        new_user = serializer.save(password = make_password(serializer.validated_data['password']))
        auth.login(request, new_user)
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)

#마이페이지 조회
@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def mypage(request):
    try:
        user = User.objects.get(pk=request.user.id)
        serializer = MypageSerializers(user)
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)

#마이페이지 수정
@api_view(['PUT'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def mypage_put(request):
    try:
        user = User.objects.get(pk=request.user.id)
        if user == request.user:
            serializer = MypagePutserializers(user, data=request.data)
            if serializer.is_valid():
                serializer.save(password = make_password(serializer.validated_data['password']))
                return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
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
@authentication_classes([SessionAuthentication,BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_page_posts(request, page):
    posts = Post.objects.filter(share=True)
    paginator = Paginator(posts, 5)
    page_obj = paginator.get_page(page)
    serializer = PageSerializer(page_obj, many=True)
    return Response(serializer.data)

#일지공유게시판 최신 4개
@api_view(['GET'])
@authentication_classes([SessionAuthentication,BasicAuthentication])
@permission_classes([IsAuthenticated])
def new_4_posts(request):
    posts = Post.objects.filter(share=True).order_by('-created_at')
    paginator = Paginator(posts, 4)
    page_obj = paginator.get_page(1)
    serializer = PageSerializer(page_obj, many=True)
    return Response(serializer.data)

#일지공유게시판 공감 4개
@api_view(['GET'])
@authentication_classes([SessionAuthentication,BasicAuthentication])
@permission_classes([IsAuthenticated])
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
@authentication_classes([SessionAuthentication,BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_all_posts(request):
    posts = Post.objects.all()
    serializer = GetSerializer(posts, many=True)
    return Response(serializer.data)

#한 게시물 조회
@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_one_post(request, pk):
    try:
        post = Post.objects.get(pk=pk)
        comments = Comment.objects.filter(post__id = pk)
        userplant = UserPlant.objects.get(pk=post.user_plant)
        post.comment_cnt = comments.count()
        
        date = userplant.created_at.replace(tzinfo=None)
        now = datetime.now().replace(tzinfo=None)
        post.ndate = (now - date).days + 1

        post.save(update_fields=['comment_cnt', 'ndate'])
        serializer = GetSerializer(post)
        return Response(serializer.data)
    except Post.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)

#게시물 업로드
@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def post_one_post(request, user_plant_id):
    serializer = PostWritePutSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(writer = request.user, user_plant=user_plant_id) #1 = request.data
        return Response(status = status.HTTP_201_CREATED)
    return Response(status = status.HTTP_400_BAD_REQUEST)

#게시물 수정
@api_view(['PUT'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def put_one_post(request, pk):
    try:
        post = Post.objects.get(pk=pk)
        if post.writer == request.user:
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
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
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
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def delete_one_post(request, pk):
    try:
        post = Post.objects.get(pk=pk)
        if post.writer == request.user:
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

# 좋아요
@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def likes(request, pk):
    try:
        post = Post.objects.get(pk=pk)
        if post.like_users.filter(pk=request.user.id).exists():
            post.like_users.remove(request.user)
            post.like_num = post.like_users.count()
            post.save(update_fields=['like_num'])
            serializer = LikeUsersSerializer(post)
            return Response(serializer.data)
        else:
            post.like_users.add(request.user)
            post.like_num = post.like_users.count()
            post.save(update_fields=['like_num'])
            serializer = LikeUsersSerializer(post)
            return Response(serializer.data)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

#식물별 작성된 일지 모아주기
@api_view(['GET'])
@authentication_classes([SessionAuthentication,BasicAuthentication])
@permission_classes([IsAuthenticated])
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
@authentication_classes([SessionAuthentication,BasicAuthentication])
@permission_classes([IsAuthenticated])
def post_comment(request, post_id):
    try:
        serializer = CommentPostSerializer(data=request.data)
        if serializer.is_valid():
            if request.user.is_authenticated :
                serializer.save(user=request.user, post_id = post_id)
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            return Response(status = status.HTTP_401_UNAUTHORIZED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(status = status.HTTP_500_INTERNAL_SERVER_ERROR)

# 댓글 삭제
@api_view(['DELETE'])
@authentication_classes([SessionAuthentication,BasicAuthentication])
@permission_classes([IsAuthenticated])
def delete_comment(request, comment_id):
    try:
        comment = Comment.objects.get(pk = comment_id)
        if comment.user == request.user:
            comment.delete()
            return Response(status = status.HTTP_200_OK)
        return Response(status = status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response(status = status.HTTP_500_INTERNAL_SERVER_ERROR)

#댓글 수만 보내주기
@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_comment_cnt(request, pk):
    try:
        post = Post.objects.get(pk=pk)
        post.comment_cnt += 1
        post.save(update_fields=['comment_cnt'])
        serializer = CommentCntSerializer(post)
        return Response(serializer.data)
    except Post.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)