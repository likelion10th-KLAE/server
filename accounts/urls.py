from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup),
    path('login/', views.login),
    path('logout/', views.logout),
    path('post/', views.get_all_posts),
    path('post/<int:pk>', views.get_one_post),
    path('write/', views.post_one_post),
    path('put/<int:pk>', views.put_one_post),
    path('delete/<int:pk>', views.delete_one_post),
    path('post/<int:pk>/likes/', views.likes),
    path('comment/<int:post_id>', views.get_comments),
    path('comment/post/<int:post_id>/', views.post_comment),
    path('comment/delete/<int:comment_id>', views.delete_comment),
    path('post/<int:pk>/share/', views.share),
    path('post/page=<int:pk>',views.get_page_posts),
    path('new_4_posts', views.new_4_posts),
    path('likes_4_posts', views.likes_4_posts),
    path('get_user_post/<int:pk>', views.get_user_post),
]