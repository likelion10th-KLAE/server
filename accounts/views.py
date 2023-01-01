from .models import User, Post, Comment
from rest_framework import status, generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from .serializers import LoginSerializer, PostWritePutSerializer, SignupSerializer, MypageSerializers ,GetSerializer, LikeUsersSerializer,CommentGetSerializer, CommentPostSerializer, PageSerializer
from django.contrib import auth
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
#from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.
'''
로그인, 로그아웃, 회원가입 관련 함수
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

#메인페이지 작성된 일지 유저벌로
@api_view(['GET'])
@authentication_classes([SessionAuthentication,BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_user_post(request):
    posts = Post.objects.filter(writer=request.user.id).order_by('-created_at')
    serializer = PageSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = auth.authenticate(
            request=request,
            username=serializer.data['username'],
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

#마이페이지 수정, 완성 안됐습니다.
@api_view(['PUT'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def mypage(request):
    try:
        user = User.objects.get(pk=request.user.id)
        if user == request.user:
            serializer = MypageSerializers(user, data=request.data)
            if serializer.is_valid():
                #serializer.save(password = make_password(serializer.validated_data['password']))
                serializer.save(update_fields=['name','password', 'profile_image', 'email'])
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)

#로그아웃
@api_view(['POST'])
def logout(request):
    auth.logout(request)
    return Response(status=status.HTTP_200_OK)

'''
마이페이지 관련 함수
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
        serializer = GetSerializer(post)
        return Response(serializer.data)
    except Post.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)

#게시물 업로드
@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def post_one_post(request):
    serializer = PostWritePutSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(writer = request.user)
        return Response(serializer.data, status = status.HTTP_201_CREATED)
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


# 댓글 조회
@api_view(['GET'])
def get_comments(request, post_id):
    try:
        comments = Comment.objects.filter(post__id = post_id)
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

