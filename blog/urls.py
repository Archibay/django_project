from django.urls import path
from django.shortcuts import render
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.index_view, name='index'),
    # path('detail/', views.detail_view, name='detail'),
    path('post-add/', views.post_new, name='add_post'),
    path('post-detail/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('posts-all/', views.PostsListView.as_view(), name='posts_all'),
    path('user-posts-all/', views.PostDetailView.as_view(), name='user_posts_all'),
    path('post/<int:pk>/comments', views.CommentAddView.as_view(), name='comment_add'),
    # path('comment-add/', views.comment_add, name='comment_add'),
    path('post-update/<int:pk>/', views.PostUpdateView.as_view(), name='post_update'),
]
