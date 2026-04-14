from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, filters, generics, mixins, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post, UserLikes, UserComments
from .serializers import PostSerializer, UserCommentsSerializer
from .permissions import IsOwnerOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserCommentsViewSet(viewsets.ModelViewSet):
    queryset = UserComments.objects.all()
    serializer_class = UserCommentsSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        # можно оптимизировать, чтоб не делать лишний запрос
        # у лайков тоже при одной из проверок возможна такая оптимизация
        if post_id is not None:
            get_object_or_404(Post, id=post_id) # можно вынести в диспатч
            return UserComments.objects.filter(post_id=post_id)
        else:
            return UserComments.objects.all()

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        # см. выше
        get_object_or_404(Post, id=post_id)
        serializer.save(user=self.request.user, post_id=post_id)


class LikeView(APIView):
    def post(self, request, pk):
        get_object_or_404(Post, pk=pk)
        with transaction.atomic():
            like, created = UserLikes.objects.get_or_create(
                post_id = pk, 
                user = request.user
            )
            if not created:
                return Response({"detail": "Уже лайкнуто"}, status=status.HTTP_400_BAD_REQUEST)
            Post.objects.filter(pk=pk).update(like_count=F("like_count") + 1)
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        get_object_or_404(Post, pk=pk)
        with transaction.atomic():
            is_deleted, _ = UserLikes.objects.filter(post_id=pk ,user=request.user).delete()
            if is_deleted:
                Post.objects.filter(pk=pk).update(like_count=F("like_count") - 1)
        return Response(status=status.HTTP_204_NO_CONTENT)