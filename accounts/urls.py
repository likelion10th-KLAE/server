from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup.as_view()),
    path('login/', views.login.as_view()),
    path('logout/', views.logout),
    path('post/', views.get_all_posts),
    path('post/<int:pk>', views.get_one_post),
    path('write/<int:user_plant_id>', views.post_one_post),
    path('put/<int:pk>', views.put_one_post),
    path('delete/<int:pk>', views.delete_one_post),
    path('mypage_put/', views.mypage_put),
    path('mypage/', views.mypage),
    path('post/<int:pk>/likes/', views.likes),
    path('comment/<int:post_id>', views.get_comments),
    path('comment/<int:pk>/cnt/', views.get_comment_cnt),
    path('comment/post/<int:post_id>/', views.post_comment),
    path('comment/delete/<int:comment_id>', views.delete_comment),
    path('post/<int:pk>/share/', views.share),
    path('post/page=<int:page>',views.get_page_posts),
    path('new_4_posts', views.new_4_posts),
    path('likes_4_posts', views.likes_4_posts),
    path('get_userplant_post/<int:user_plant_id>', views.get_userplant_post),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify', TokenVerifyView.as_view(), name='token_verify'),
    path('post/likes_test/', views.likes_test),
]