from django.urls import path

from .views import (
    BlogPostList,
    BlogPostDetail,
)


app_name='blog'

urlpatterns = [
    path('', BlogPostList.as_view(), name='home'),
    path('<str:slug>/', BlogPostDetail.as_view(), name='post'),
]
