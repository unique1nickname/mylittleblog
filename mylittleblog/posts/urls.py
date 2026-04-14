from django.urls import path, include
from rest_framework import routers
from .views import PostViewSet, UserCommentsViewSet, LikeView

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
# router.register(r'comments', UserCommentsViewSet, basename='comment')

urlpatterns = [
    path(
        'posts/<int:post_id>/comments/',
        UserCommentsViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='comment'
    ),
    path(
        'comments/<int:pk>/',
        UserCommentsViewSet.as_view({
            'get': 'retrieve',
            # 'put': 'update',
            # 'patch': 'partial_update',
            'delete': 'destroy'
        }),
        name='comment-detail'
    ),
    path('', include(router.urls)),
    path('posts/<int:pk>/like/', LikeView.as_view(), name='like'),
]