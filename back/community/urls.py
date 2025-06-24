from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CommunityPostViewSet, CommentViewSet
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register(r'posts', CommunityPostViewSet, basename='posts')

# 댓글을 게시글에 nested로 연결
post_router = routers.NestedDefaultRouter(router, r'posts', lookup='post')
post_router.register(r'comments', CommentViewSet, basename='post-comments')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(post_router.urls)),
]
